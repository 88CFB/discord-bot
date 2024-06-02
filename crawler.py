import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def crawl_news(query):
    try:

        # 构建URL
        url = f"https://www.google.com/search?q={query}&sca_esv=ba58e664356714d5&biw=982&bih=750&tbm=nws&sxsrf=ADLYWILV081ZgTffE8cAWaDCd6sJQ84KWQ%3A1717213098595&ei=qpdaZuP-I8Ts1e8PmL6qmAY&ved=0ahUKEwjj-_qlvbmGAxVEdvUHHRifCmMQ4dUDCA0&uact=5&oq={query}&gs_lp=Egxnd3Mtd2l6LW5ld3MiBumBiuaIsjILEAAYgAQYsQMYgwEyCxAAGIAEGLEDGIMBMggQABiABBixAzIIEAAYgAQYsQMyCBAAGIAEGLEDMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgUQABiABDIFEAAYgARIyhFQAFiqDHAAeACQAQCYAUSgAc0CqgEBNrgBA8gBAPgBAZgCBqAC8gLCAg4QABiABBixAxiDARiKBcICBBAAGB7CAggQABiiBBiJBcICCBAAGIAEGKIEmAMAkgcBNqAH8A8&sclient=gws-wiz-news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html = await response.text()

        # 解析HTML内容
        soup = BeautifulSoup(html, "html.parser")

        # 查找包含新闻条目的div元素
        news_items = soup.select('div[class*="SoaBEf"]')

        # 提取并返回新闻标题、链接和摘要的列表
        news_list = []
        for item in news_items:
            delay = random.uniform(4, 7)
            await asyncio.sleep(delay)
            title = item.select_one('div[class="n0jPhd ynAwRc MBeuO nDgy9d"]')
            outline = item.select_one('div[class="GI74Re nDgy9d"]')
            link = item.find("a", class_="WlydOe")["href"]
            '''
            img = item.select_one('img[id*="dimg"]')
            image_url = img['src'] if img else None
            if image_url:
                image_url = urljoin(url, image_url)  # 构建完整的图片 URL
                '''
            if title:
                only_title = title.get_text()
                only_outline = outline.get_text()
                news_list.append({
                    "title": only_title,
                    "link": link,
                    "outline": only_outline,
                    #"img_url": image_url
                })
        return news_list
    except Exception as e:
        print(f"Error in crawl_news: {e}")
        return []
