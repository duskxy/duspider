# -*- coding: utf-8 -*-
import datetime
import re
import requests
import jsbeautifier
from lxml import etree
import sys
import time

i = 1
pset = set()

#start = datetime.datetime.now()
while True:
    query = str(i).zfill(2) if i <10 else i
    headers = {"Host": "premproxy.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
               "Referer": "https://premproxy.com"
               }
    try:
        cent = requests.get("https://premproxy.com/list/{}.htm".format(query),headers=headers, timeout=10)
        if cent.status_code == 404:
            print("proxy404")
            break
    except Exception as e:
        print(e)
        sys.exit()
    v = cent.content.decode('utf-8')
    jquery = "https://premproxy.com" + re.findall(r'<script src="(.*?)"></script>',v)[1]
    jqcont = requests.get(jquery)
    if jqcont.status_code == 404:
        print("js404")
        break
    beau = jsbeautifier.beautify(jqcont.content.decode("utf-8"))
    p = etree.HTML(cent.content)
    print("第{}页".format(query))
    ipp = p.xpath('//*[@class="anon" or @class="transp"]/td[1]/text()')
    for ipc in ipp:
        ip = ipc.replace(":","")
        po = re.findall('value=\"'+ip+'\|(.*?)\"',v)[0]
        pot =  re.findall('\.'+po+'\\\\\'\)\.html\((.*?)\)',beau)[0]
        print(ipc + pot)
    i += 1
#stop = datetime.datetime.now()
#totime = (stop - start).seconds
#print(totime)
