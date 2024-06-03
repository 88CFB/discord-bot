import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
import crawler
import pymongo
import MongoDB

# 连接到MongoDB数据库
myClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myClient['discordbot']


# 从 .env 文件加载环境变量
load_dotenv(dotenv_path='secret.env')
discord_key = os.getenv('DISCORD_KEY')

# 创建 Bot 对象
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# 定义命令事件
@bot.event
async def on_ready():
    print(f"Logged in as --> {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, how can I help you {ctx.author.display_name}?")

@bot.command()
async def search_news(ctx, *, query: str):
    collist = mydb.list_collection_names()
    await ctx.send(f"正在搜尋有關( {query} )的相關新聞")

    if query in collist:  # 判断 sites 集合是否存在
        results = MongoDB.find_site(query)
        if results:
            color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for result in results:
                embed = discord.Embed(
                    title=result['title'],
                    url=result['link'],
                    description=result['outline'],
                    color=color
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send("No results found in the database.")
    else:
        try:
            await ctx.send(f"第一次搜尋需要時間...")
            news_list = await crawler.crawl_news(query)  # 使用异步调用方式调用 crawler.py 中的 crawl_news 函数
            # await ctx.send("finish")
            if news_list:
                # await ctx.send("finish2")
                color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for news in news_list:
                    embed = discord.Embed(
                        title=news['title'],
                        url=news['link'],
                        description=news['outline'],
                        color=color
                    )
                    # Add an image if available
                    '''
                    if news['img_url']:
                        embed.set_image(url=news['img_url'])  # 这里应替换为实际的图片链接
                    print(news['img_url'])
                    '''
                    MongoDB.add_site(news['title'], news['link'], news['outline'], query)
                    await ctx.send(embed=embed)



            else:
                await ctx.send("No news found or an error occurred during the search.")
        except Exception as e:
            await ctx.send(f"Error occurred: {e}")
    await ctx.send(f"以上是搜尋結果!")
# 启动 Bot
bot.run(discord_key)
