import aiohttp
import asyncio
from lxml import etree
import jsbeautifier
import re
import sys
import queue


headers = {"Host": "premproxy.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
               "Referer": "https://premproxy.com"
               }
   
q = queue.Queue()


async def ver(q):
    while not q.empty():
        print(q.qsize())

async def get(url,call_parse=None):
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            txt = await resp.text()
            stu = resp.status
            if stu == 404:
                print(q.qsize())
                sys.exit()
            p = etree.HTML(txt)
            ipp = p.xpath('//*[@class="anon" or @class="transp"]/td[1]/text()')
            jquery = "https://premproxy.com" + re.findall(r'<script src="(.*?)"></script>',txt)[1]
            async with session.get(jquery) as rejq:
                jqcont = await rejq.text()
                jstu = rejq.status
                if jstu == 404:
                    print("js404")
                    while not q.empty():
                        pp = q.get()
                        try:
                            async with session.get("http://www.proxy.com",proxy = "http://{}".format(pp),timeout=5) as repr:
                                if repr.status == 200:
                                    print("代理可用:{}".format(pp))
                        except Exception as e:
                            print("代理不可用:{}".format(pp))
                            continue
                beau = jsbeautifier.beautify(jqcont)
                for i in ipp:
                    ip = i.replace(":","").strip()
                    po = re.findall('value=\"'+ip+'\|(.*?)\"',txt)[0]
                    try:
                        pot =  re.findall('\.'+po+'\\\\\'\)\.html\((.*?)\)',beau)[0].strip()
                    except Exception as e:
                        print(e)
                        pot  = ""
                    v = i + pot
                    print(v)
                    q.put(v)
       

def parse_url():
    pass


if __name__ == "__main__":
    i = 1
    u = "https://premproxy.com/list/{}.htm"
    while True:
        query = str(i).zfill(2) if i <10 else i
        url = u.format(query)
        print("第{}页".format(query))
        result = asyncio.ensure_future(get(url)) 
        ev = asyncio.get_event_loop()
        ev.run_until_complete(result)
        i += 1
