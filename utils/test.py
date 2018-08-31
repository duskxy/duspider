import requests
import hashlib
import datetime
from threading import Thread
import multiprocessing
import aiohttp
import asyncio


async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            page = await res.content()
            print(dir(res))
            print(res.status)
        

url = "https://www.2345.com"

def mget(_):
    p = requests.get(url).content
    print(hashlib.md5(p).hexdigest())


def tget():

    theads_list = []

    for _ in range(500):
        v = Thread(target=mget,args=(url,))
        theads_list.append(v)

    for t in theads_list:
        t.start()

    for t in theads_list:
        t.join()



start = datetime.datetime.now()
#[mget("https://www.2345.com") for _ in range(500)]
#tget()


tasks = [asyncio.ensure_future(fetch()) for _ in range(1)]
ev = asyncio.get_event_loop()
ev.run_until_complete(asyncio.wait(tasks))




stop = datetime.datetime.now()
total = (stop-start).seconds
print("时间总计: {}".format(total))
