# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
import os
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv(dotenv_path='secret.env')

discord_key = os.getenv('DISCORD_KEY')

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")

@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    # 新訊息包含Hello，回覆Hello, world!
    if message.content == "hello":
        await message.channel.send(f"Hello how can I help you {message.author.display_name}")

    if message.content == "bye":
        await message.channel.send("goodbye")
        await client.close()

client.run(discord_key)