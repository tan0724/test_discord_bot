import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Union

class Channelname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @app_commands.command(name = "更改文字頻道名稱", description = "更改文字頻道名稱")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def changetextchannelname(self,interaction: discord.Interaction, channel: discord.TextChannel, new_name: str):
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"{interaction.user.nick or interaction.user.name}已將此頻道名稱更改為 {new_name}")

    @app_commands.command(name = "更改語音頻道名稱", description = "更改語音頻道名稱")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def change_voicechannel_name(self,interaction: discord.Interaction, channel: discord.VoiceChannel, new_name: str):
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"{interaction.user.nick or interaction.user.name}已將此頻道名稱更改為 {new_name}")

    @app_commands.command(name = "刪除文字頻道", description = "刪除文字頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def deletetextchannel(self,interaction: discord.Interaction, channel: discord.TextChannel):
            await interaction.response.send_message(f"已刪除{channel.name}頻道")
            await channel.delete()

    @app_commands.command(name = "刪除類別", description = "刪除類別")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def delecategorychannel(self,interaction: discord.Interaction, category: discord.CategoryChannel):
            channels = category.channels
            for channel in channels:
                print(f"已刪除{channel.name}頻道")
                await channel.delete()
            await interaction.response.send_message(f"已刪除{category.name}")
            await category.delete()
            

    @app_commands.command(name = "刪除語音頻道", description = "刪除語音頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def deletevoicechannel(self,interaction: discord.Interaction, channel: discord.VoiceChannel):
            await interaction.response.send_message(f"已刪除{channel.name}頻道")
            await channel.delete()

    @app_commands.command(name="更改語音頻道位元率", description="更改語音頻道位元率")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setstatus(self,interaction:discord.Interaction,channel:discord.VoiceChannel,bitrate1:int):
        try:
            await channel.edit(bitrate=bitrate1)
            await interaction.response.send_message(f"已將位元率改成{bitrate1}")
        except Exception as e:
                await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="更改語音頻道限制人數", description="更改語音頻道限制人數")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def user_limitVoiceChannel(self,interaction:discord.Interaction,channel:discord.VoiceChannel,user_limit:int):
            await channel.edit(user_limit=user_limit)
            await interaction.response.send_message(f"已限制頻道人數為: {user_limit}")
            
    @app_commands.command(name="更改文字頻道說名", description="更改文字頻道說名")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def topicTextChannel(self,interaction:discord.Interaction,channel:discord.TextChannel,topic:str):
            await channel.edit(topic=topic)
            await interaction.response.send_message(f"已將頻道說明設為: {topic}")
          

async def setup(bot: commands.Bot):
    await bot.add_cog(Channelname(bot))