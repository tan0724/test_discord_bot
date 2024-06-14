import discord
from discord import app_commands
from discord.ext import commands


class Sever(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sever_list",description = "列出機器人所在伺服器")
    async def sever_list(self, interaction: discord.Interaction,):
        try:
            if interaction.user.name == "tan_07_24":
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
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="sever_channel",description="列出伺服器頻道")
    async def sever_channel(self,interaction:discord.Interaction,guildid:str):
        try:
            if interaction.user.name == "tan_07_24":
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

    @app_commands.command(name="指定sever邀請",description="指定一個頻道並獲取該頻道的邀請連結")
    async def channelurl(self,interaction:discord.Interaction,guildid:str):
        try:
            if interaction.user.name == "tan_07_24":
                guild = self.bot.get_guild(int(guildid))
                guildurl = await guild.invites()
                await interaction.response.send_message(f"{guild.name} | {guildurl}",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @commands.Cog.listener()
    async def on_guild_join(self,guild: discord.Guild):
        channel = self.bot.get_channel(1243941520793407559)
        try:
            guildurl = await guild.invites()
        except Exception as e:
            guildurl = f"No invite found:{e}"
        await channel.send(f"```\n機器人進入伺服器:{guild.name} {guild.id}\n{guildurl}\n```")

    @commands.Cog.listener()
    async def on_guild_remove(self,guild: discord.Guild):
        channel = self.bot.get_channel(1243941520793407559)
        try:
            guildurl = await guild.invites()
        except Exception as e:
            guildurl = f"No invite found:{e}"
        await channel.send(f"```\n機器人離開伺服器:{guild.name} {guild.id}\n{guildurl}\n``` ")

async def setup(bot: commands.Bot):
    await bot.add_cog(Sever(bot))