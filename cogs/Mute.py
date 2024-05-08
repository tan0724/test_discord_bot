import discord
from discord import app_commands
from discord.ext import commands
import asyncio


class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mute",description="禁言使用者")
    async def mute(self,interaction: discord.Interaction, user: discord.Member, duration: int):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id) # type: ignore
        if member is not None:
            if member.guild_permissions.administrator:
                await user.edit(mute=True)
                await interaction.response.send_message(f"{user.mention} 已被禁言 {duration} 秒")
                await asyncio.sleep(duration)
                await user.edit(mute=False)
                await interaction.response.send_message(f"{user.mention} 禁言已解除")
            else:
                await interaction.response.send_message("你沒有權限進行這個操作")
        else:
            await interaction.response.send_message("找不到使用者或使用者不在伺服器中")

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))
