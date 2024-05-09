import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands, tasks

channel_creators = {}

class Voiceinout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入voice")

    @app_commands.command(name="設定動態語音頻道",description="設定動態語音頻道入口")
    async def newvoicechannel(self, interaction: discord.Interaction,voice:discord.VoiceClient):
        global target_channel_name
        target_channel_name = voice
        await interaction.response.send_message(f"已設定動態語音入口為{voice}")


    @tasks.loop(minutes=5)  #隔5秒運行
    async def check_channel_status(self):
        for channel_id, creator_id in list(channel_creators.items()):
           
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                
                del channel_creators[channel_id]
            else:
             
                if len(channel.members) == 0:
                    
                    await channel.delete()
                    print(f'频道 {channel.name} 已被删除')

    @commands.Cog.listener()
    async def on_voice_state_update(self,member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None and after.channel is not None:
            nickname = member.nick if member.nick else member.name
            channel = after.channel
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="成員加入", description=f"{nickname} 加入 {after.channel.name}", color= emb_color)
            await channel.send(embed=embed)
        elif after.channel is None and before.channel is not None:
            nickname = member.nick if member.nick else member.name
            channel = before.channel
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="成員離開", description=f"{nickname} 離開 {before.channel.name}", color= emb_color)
            await channel.send(embed=embed)


        if after.channel and after.channel.name == target_channel_name:
            # 獲取要同步的類別名稱
            category_name = "Category Name"

            # 尋找伺服器中指定名稱的類別
            category = discord.utils.get(member.guild.categories, name=category_name)

            if category is None:
                print(f'找不到名稱為 "{category_name}" 的類別！')
                return

            # 創建新的語音頻道並設定類別
            new_channel = await member.guild.create_voice_channel('New Voice Channel', category=category)

            # 給予進入者管理新頻道的權限
            await new_channel.set_permissions(member, manage_channels=True)

            print(f'已在類別 "{category_name}" 中新增語音頻道 "{new_channel.name}"，給予 {member.display_name} 管理權限！')
            await member.move_to(new_channel)
            print(f'{member.display_name} 被移动到新频道 {new_channel.name}')

async def setup(bot: commands.Bot):
    await bot.add_cog(Voiceinout(bot))