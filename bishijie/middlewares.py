# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware as _RetryMiddleware
from scrapy.utils.response import response_status_message
import re
import base64

logger = logging.getLogger(__name__)

class RetryMiddleware(_RetryMiddleware):

    def __init__(self, settings):
        super(RetryMiddleware, self).__init__(settings)
        self.proxies = {}
        self.proxy_list = settings.get('PROXY_LIST')
        if not self.proxy_list:
            return

        try:
            with open(self.proxy_list) as f:
                lines = f.readlines()
        except (IOError, EOFError):
            return

        for line in lines:
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes or 'acw_sc__v3' in response.body.decode("utf-8"):
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        last_proxy = request.meta.get('proxy')
        remove_failed_proxy = spider.settings.get('REMOVE_FAILED_PROXY', False)
        if remove_failed_proxy and last_proxy and self.proxies:
            self.proxies.pop(last_proxy, None)
            logging.debug('Removing failed proxy <%s>, %d proxies left' % (
                last_proxy, len(self.proxies))
            )
        elif isinstance(reason, self.EXCEPTIONS_TO_RETRY):
            self.proxies.pop(last_proxy, None)
            logging.debug('Removing useless proxy <%s>, %d proxies left' % (
                last_proxy, len(self.proxies))
            )

        if self.proxies or retries <= self.max_retry_times:
            logging.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if self.proxies:
                proxy_address = random.choice(list(self.proxies.keys()))
                proxy_user_pass = self.proxies[proxy_address]
                logging.debug('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))
                retryreq.meta['proxy'] = proxy_address
                if proxy_user_pass:
                    basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
                    retryreq.headers['Proxy-Authorization'] = basic_auth

            return retryreq
        else:
            logging.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
