import random
import discord
from discord import app_commands
from discord.ext import commands

class Channelname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "更改文字頻道名稱", description = "更改文字頻道名稱")
    @commands.has_permissions(manage_channels=True)
    async def changetextchannelname(self,interaction: discord.Interaction, channel: discord.TextChannel, new_name: str):
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"已將頻道名稱更改為 {new_name}")

    @app_commands.command(name = "更改語音頻道名稱", description = "更改語音頻道名稱")
    @commands.has_permissions(manage_channels=True)
    async def change_textchannel_name(self,interaction: discord.Interaction, channel: discord.VoiceChannel, new_name: str):
        if channel.id != 1224990808315400254:
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"已將頻道名稱更改為 {new_name}")
        elif channel.id == 1224990808315400254:
            await interaction.response.send_message('此頻道不能更改')
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Channelname(bot))