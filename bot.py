import discord
import asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='%', intents=intents)
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("錯誤：找不到 Discord 令牌。請設置 TOKEN 環境變數。")
    exit()

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")
    slash = await bot.tree.sync()
    print(f"載入 {len(slash)} 個斜線指令")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")
    slash = await bot.tree.sync()
    print(f"載入 {len(slash)} 個斜線指令")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")
    slash = await bot.tree.sync()
    print(f"載入 {len(slash)} 個斜線指令")
    
# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
