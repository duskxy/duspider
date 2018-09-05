import aiohttp
import asyncio
from lxml import etree
import jsbeautifier
import re
import requests
import sys
import queue
import threading
import os
import time

if os.path.exists("proxyver.txt"):
    os.remove("proxyver.txt")



headers = {"Host": "premproxy.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
               "Referer": "https://premproxy.com"
               }
   
lock = threading.Lock()

q = queue.Queue()


def verpro(q):
    vc = q.get(timeout=0.2)
    proxies = {"http":vc}
    try:
        tv = requests.get("http://www.freebuf.com",proxies=proxies,timeout=6)
        if tv.status_code == 200:
            with lock:
                with open("proxyver.txt","a+") as ww:
                    ww.write(vc + '\n')
                    ww.flush()
    except Exception as e:
        pass



async def get(url,call_parse=None):
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            txt = await resp.text()
            p = etree.HTML(txt)
            ipp = p.xpath('//*[@class="anon" or @class="transp"]/td[1]/text()')
            jquery = "https://premproxy.com" + re.findall(r'<script src="(.*?)"></script>',txt)[1]
            async with session.get(jquery) as rejq:
                jqcont = await rejq.text()
                beau = jsbeautifier.beautify(jqcont)
                for i in ipp:
                    ip = i.replace(":","").strip()
                    po = re.findall('value=\"'+ip+'\|(.*?)\"',txt)[0]
                    try:
                        pot =  re.findall('\.'+po+'\\\\\'\)\.html\((.*?)\)',beau)[0].strip()
                    except Exception as e:
                        pot  = "8080"
                    v = i + pot
                    q.put(v)
       

def parse_url():
    pass


if __name__ == "__main__":
    tstart = time.time()
    i = 1
    qmax = []
    u = "https://premproxy.com/list/{}.htm"
    print("开始爬取页数")
    while True:
        query = str(i).zfill(2) if i <10 else i
        url = u.format(query)
        if requests.head(u.format(query)).status_code == 404:
            break
        else:
            qmax.append(u.format(query))
        i += 1
    print("爬取页数为: {}".format(len(qmax)))
    print("开始爬取代理")
    result = [ asyncio.ensure_future(get(u)) for u in qmax ] 
    ev = asyncio.get_event_loop()
    ev.run_until_complete(asyncio.gather(*result))
    ev.close()
    print("爬取代理数为: {}".format(q.qsize()))
    print("开始检测可用代理")
    while not q.empty():
        th = []
        for i in range(q.qsize()):
            thd = threading.Thread(target=verpro,args=(q,))
            th.append(thd)
        for i in th:
            i.start()
        for h in th:
            h.join()
    print("检测可用代理完成!")
    tend = time.time()
    print("共计花费时间: {}",format(tend-tstart))
