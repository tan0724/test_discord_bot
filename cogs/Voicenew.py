import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands, tasks
import json
from json import load
channel_creators = {}

class Voicenew(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入voicenew")
    

    @app_commands.command(name="設定動態語音頻道", description="設定動態語音頻道入口")
    async def newvoicechannel(self, interaction: discord.Interaction, category: discord.CategoryChannel, voice: discord.VoiceChannel): 
        await interaction.response.send_message(f"已設定動態語音入口為 {voice.name}")
        print(voice)
        print(category)
        jsonFile = open('demo\\demo.json','a')
        channel_creators[category.name] = voice.name
        json.dump(channel_creators, jsonFile,indent=2)
        jsonFile.close()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        jsonFile = open('demo\\demo.json','r')
        data = jsonFile.read()
        target_channel_name_date = json.JSONDecoder().decode(data)
        jsonFile.close()
        target_channel_name = target_channel_name_date[after.channel.category]
        if after.channel.name == target_channel_name:
            guild = member.guild
            category = discord.utils.get(guild.categories, name=after.channel.category)
            if category is None:
                print(f'找不到名稱為 "{after.channel.category}" 的類別！')
                return

            # 创建新的语音频道并设置类别
            new_channel = await guild.create_voice_channel(name=f"{member} 的房間", category=category)

            # 给进入者管理新频道的权限
            await new_channel.set_permissions(member, manage_channels=True)

            print(f'已在 "{after.channel.category}" 中新增語音頻道 "{new_channel.name}"，给予 {member.display_name} 管理權限！')
            await member.move_to(new_channel)
            print(f'{member.display_name} 被移動到 {new_channel.name}')
            channel_creators1 = {}
            channel_creators1[new_channel.id] = member.id
            jsonFile = open('demo\\demo.json','a')
            json.dump(channel_creators1, jsonFile,indent=2)
            jsonFile.close()

    @tasks.loop(minutes=1)  # 每隔 5 分钟运行一次
    async def check_channel_status(self):
        jsonFile = open('demo\\demo.json','r')
        data = jsonFile.read()
        channel_creators2 = json.JSONDecoder().decode(data)
        jsonFile.close()
        for channel_id in list(channel_creators2.items()):
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                del channel_creators2[channel_id]
            else:
                if len(channel.members) == 0:
                    await channel.delete()
                    print(f'頻道 {channel.name} 已被刪除')


async def setup(bot: commands.Bot):
    await bot.add_cog(Voicenew(bot))