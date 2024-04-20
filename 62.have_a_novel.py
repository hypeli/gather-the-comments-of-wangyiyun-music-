"""抓取百度小说 西游记的所有章节

1.同步拿到章节的url
2.协程下载各章节
"""
import requests
import asyncio
import aiohttp
import aiofiles
from lxml import etree
import json
def getCatalog(url):
    domain = 'https://www.360wxwxs.com/'
    urls = []
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
    except Exception as e:
        print('爬取错误', e)
    else:
        tree = etree.HTML(res.text)
        catalog_list = tree.xpath('//*[@id="list"]/dl[2]/dd')
        for catalog in catalog_list:
            title = catalog.xpath('./a/@title')[0]
            href = domain + catalog.xpath('./a/@href')[0]
            urls.append([title, href])

        return urls

# 准备异步任务
async def aiodownload(url):
    # aiohttp.ClientSession(url) 相当于 requests.session
    name = ''.join(url[0].split(' '))
    async with aiohttp.ClientSession() as session:
        async with session.get(url[1]) as res:
            content = await res.text()
            tree = etree.HTML(content)
            data = tree.xpath('//*[@id="content"]/p/text()')
            async with aiofiles.open(f'd:\\novel\\{name}.txt', 'a', encoding='utf-8') as f:
                await f.write('\t\n'.join(data))





async def main():
    url1 = 'https://www.360wxwxs.com/3412/'
    urls = getCatalog(url1)
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(aiodownload(url)))

    await asyncio.wait(tasks)


# 对于这种异步操作来说，url越多，效率越高
if __name__ == "__main__":
     asyncio.run(main())
