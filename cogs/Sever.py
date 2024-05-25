import discord
from discord import app_commands
from discord.ext import commands


class Sever(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sever_list",description = "列出機器人所在伺服器")
    async def sever_list(self, interaction: discord.Interaction,):
        if interaction.user.id == 710128890240041091 or 1022588836032806993 or 906188519083491359 or 1158951186452451440 or 988145093334696046:
            guilds = self.bot.guilds
            lite = "機器人加入伺服器連結：\n\n"
            for guild in guilds: 
                invites = await guild.invites()
                if invites:
                    invite_url = invites[0].url
                    lite += f"Invite for {guild.name} {guild.id}: {invite_url}\n"
                else:
                    lite += f"No invite found for {guild.name} {guild.id}\n"
            await interaction.response.send_message(lite,ephemeral=True)

    @app_commands.command(name="sever_channel",description="列出伺服器頻道")
    async def sever_channel(self,interaction:discord.Interaction,guildid:str):
        try:
            guild = self.bot.get_guild(int(guildid))
            if guild is not None:
                channels = guild.channels
                channel1 = f"以下為{guild.name}所有頻道\n\n"
                for channel in channels:
                    channel1 += f"{channel.name} id:{channel.id}\n"
                await interaction.response.send_message(channel1,ephemeral=True)
            else:
                await interaction.response.send_message("錯誤guild為None",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Sever(bot))