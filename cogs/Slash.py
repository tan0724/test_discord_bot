import subprocess
from typing import Optional
import discord
import random
import requests
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("錯誤：找不到 API 令牌。請設置 API 環境變數。")
    exit()

ffmpeg_process = None  # 將ffmpeg_process定義為全局變量

def check_if_guild_is_me(interaction: discord.Interaction) -> bool:
    return interaction.guild.id == 1238133524662325351

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "提問", description = "讓機器人回答你的問題")
    async def 提問(self, interaction: discord.Interaction, 問題: str):
        # 生成一個 1 到 10 之間的隨機整數（包含 1 和 10）
        random2_int = random.randint(1, 99) 
        my_list = ['不是', '是']
        random_element = random.choice(my_list)
        sentence = "{} % {}".format(random2_int, random_element)
        replies2 = [
                    ('就是了拉', 0.2),
                    (sentence, 0.6),
                    ('或許大概應該不是', 0.2)
                ]
        random3_int = random.randint(0, 255)
        random4_int = random.randint(0, 255)
        random5_int = random.randint(0, 255)
        reply = random.choices([reply[0] for reply in replies2], weights=[reply[1] for reply in replies2], k=1)[0]
        sentence1 ="我覺得 {} <:986296828322525224:1026433054958440508>".format(reply)
        emb_color = discord.Color.from_rgb(random3_int, random4_int , random5_int)
        embed = discord.Embed(title='<:74277272:1209520682728427551> | '+ 問題 , description = sentence1 , color = emb_color)
        await interaction.response.send_message(embed = embed)

    @app_commands.command(name = "匯率", description = "查看匯率")
    @app_commands.choices(
        iso = [
            Choice(name = "澳幣", value = "AUD"),
            Choice(name = "加幣", value = "CAD" ),
            Choice(name = "人民幣", value = "CNY"),
            Choice(name = "歐元", value = "EUR"),
            Choice(name = "港幣", value = "HKD"),
            Choice(name = "日圓", value = "JPY"),
            Choice(name = "澳門幣", value = "MOP"),
            Choice(name = "新臺幣", value = "TWD"),
            Choice(name = "英鎊", value = "GBP"),
            Choice(name = "韓圜", value = "KRW"),
            Choice(name = "美元", value = "USD"),
            Choice(name = "越南盾", value = "VND"),
        ]
)
    async def 匯率(self,interaction: discord.Interaction, iso:Choice[str]):
            # 發送請求到 Open Exchange Rates API 以獲取匯率
            iso = iso.value # type: ignore
            response = requests.get(f'https://open.er-api.com/v6/latest/TWD', params={'app_id': API_KEY})
            data = response.json()
            # 檢查是否成功取得匯率數據
            if response.status_code == 200:
                # 檢查貨幣是否有效
                if iso in data['rates']:
                    exchange_rate = data['rates'][iso]
                    await interaction.response.send_message(f'1 TWD = {exchange_rate} {iso} ')
                else:
                    await interaction.response.send_message('無效的貨幣代碼')
            else:
                await interaction.response.send_message('無法獲取匯率數據')
    
    @app_commands.command(name = "upfile", description = "讓機器人幫你傳送訊息並提及全部人")
    async def upfile(self,interaction: discord.Interaction,file: Optional[discord.Attachment],file2:Optional[discord.Attachment] ,say:str):
        await interaction.response.send_message(f"@everyone {say} {file} {file2}")


    @app_commands.command(name="新增動態文字_and_語音頻道",description="新增屬於你的頻道組合")
    async def newchannelyou(self,interaction:discord.Interaction,channelname:str):
        guild = interaction.guild
        newcategory = await guild.create_category(name=channelname,position=0)
        newchannel = await guild.create_text_channel(name=channelname,category=newcategory,topic=f"屬於 {interaction.user.name} 與他的朋友們的專屬文字頻道,使用完畢記得刪除!請注意!扳手還是看的到此頻道")
        newvoicechannel = await guild.create_voice_channel(name=channelname,category=newcategory,rtc_region="japan")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        await newcategory.edit(overwrites=overwrites)
        await newcategory.set_permissions(interaction.user, manage_channels=True,read_messages=True)
        try:
            # 同步頻道權限
            await newchannel.edit(sync_permissions=True)
            await newvoicechannel.edit(sync_permissions=True)
            print(f'頻道 {newchannel.name} 的權限已同步至分類 {newchannel.category.name}。')
        except Exception as e:
            print(f'同步頻道權限時發生錯誤：{e}')

        await interaction.user.send(f"""已創建專屬於你的文字頻道在: {interaction.guild.name} \n現在快使用/給予你的朋友觀看頻道的權利吧! \n頻道使用完畢請記得刪除 /刪除文字頻道""")
        await newchannel.send(f"""{interaction.user.mention}已創建專屬於你的文字頻道在: {interaction.guild.name} 
現在快使用/給予你的朋友觀看頻道的權利吧!
頻道使用完畢請記得刪除 /刪除文字頻道""")

    @app_commands.command(name="給予專屬頻道加入權限",description="給予專屬頻道加入權限")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def giveglass(self,interaction:discord.Interaction,username:discord.Member,username1:Optional[discord.Member],category:discord.CategoryChannel,give_or_out:bool):
        if give_or_out == True:
            await category.set_permissions(username, read_messages=True)
            channels = category.channels
        if give_or_out == True:
            if username1 is not None:
                await category.set_permissions(username1, read_messages=True)
        if not channels:
            print(f'分類 {category.name} 中沒有頻道。')
            return
        try:
            # 同步每個頻道的權限
            for channel in channels:
                await channel.edit(sync_permissions=True)
            print(f'分類 {category.name} 中的所有頻道權限已同步。')
            await interaction.response.send_message(f"已給予{username} 頻道 {category.name} 觀看權限")
        except Exception as e:
            print(f'同步分類內頻道權限時發生錯誤：{e}')
        if give_or_out == False:
            await category.set_permissions(username, read_messages=False)
        if not channels:
            print(f'分類 {category.name} 中沒有頻道。')
            return
        try:
            # 同步每個頻道的權限
            for channel in channels:
                await channel.edit(sync_permissions=True)
            print(f'分類 {category.name} 中的所有頻道權限已同步。')
            await interaction.response.send_message(f"已剝奪{username} 頻道 {category.name} 觀看權限")
        except Exception as e:
            print(f'同步分類內頻道權限時發生錯誤：{e}')

    @app_commands.command(name="help", description="列出所有斜杠指令")
    async def help_command(self, interaction: discord.Interaction):
        try:
            commands = self.bot.tree.walk_commands()
            help_message = ""
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            for command in commands:
                if isinstance(command, app_commands.Command):
                    if command.description:
                        help_message += f"/{command.name} - {command.description}\n"
                    else:
                        help_message += f"/{command.name}\n"
            embed = discord.Embed(title="# help", color= emb_color)
            embed.add_field(name="以下是所有可用的斜杠命令：\n\n",value=help_message,inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f'發送訊息時發生錯誤：{e}',ephemeral=True)

    @app_commands.command(name="new_role",description="創建新的身分組")
    @app_commands.checks.has_permissions(administrator=True)
    async def newrole(self,interaction:discord.Interaction,new_role_name:str):
        try:
            guild = interaction.guild
            newrloe = await guild.create_role(name=new_role_name)
            await interaction.response.send_message(f"已新增{newrloe.name}",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
    
    @app_commands.command(name="give_or_out_user_new_role",description="給予或移除伺服器成員新的身分組")
    @app_commands.checks.has_permissions(administrator=True)
    async def usernewrole(self,interaction:discord.Interaction,role:discord.Role,member:discord.Member,out_give:bool):
        try:
            if out_give == True:
                await member.add_roles(role)
                await interaction.response.send_message(f"已給予{member.nick} {role.name} 身分組")
            else:
                await member.remove_roles(role)
                await interaction.response.send_message(f"已刪除{member.nick} 的 {role} 身分組")
        except Exception as e:
            await interaction.response.send_message(f"報錯:{e}",ephemeral=True)

    @app_commands.command(name="say",description="讓機器人幫你說話")
    async def say(self,interaction:discord.Interaction,話:str):
        try:
            channel = interaction.channel
            await channel.send(f"# {話}")
            await interaction.response.send_message("已執行指令",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤:{e}")

    @app_commands.command(name="join_in_voicechannel_record",description="讓機器人進入語音頻道錄音")
    async def record(self,interaction:discord.Interaction,channel:discord.VoiceChannel):
        try:
            guild = interaction.guild
            await channel.connect()
            vc = guild.voice_client
            # 使用 FFmpeg 進行錄音
            ffmpeg_process = subprocess.Popen([
                'ffmpeg', 
                '-y',  # 覆蓋輸出文件
                '-f', 's16le', 
                '-ar', '44100', 
                '-ac', '2', 
                '-i', 'pipe:0',
                f'{channel.name}.wav'
            ], stdin=subprocess.PIPE)

            def audio_callback(data):
                ffmpeg_process.stdin.write(data)

            vc.listen(discord.PCMAudio(audio_callback))
            await interaction.response.send_message("已開始錄音")
        
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="stop_record",description="讓機器人停止錄音並離開語音")
    async def stoprecord(self,interaction:discord.Interaction):
        try:
            guild = interaction.guild
            vc = guild.voice_client
            if ffmpeg_process is not None:
                ffmpeg_process.stdin.close()
                ffmpeg_process.wait()
            await guild.voice_client.disconnect()
            await interaction.response.send_message("結束錄音")
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="ban",description="停權使用者")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self,interaction:discord.Interaction,member:discord.Member):
        try:
            await member.ban()
            await interaction.response.send_message(f"已封鎖{member.name}")
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="ὀστρακισμός",description="放逐指定成員")
    @app_commands.checks.has_permissions(administrator=True)
    async def ὀστρακισμός(self,interaction:discord.Interaction,member:discord.Member):
        try:
            await member.kick()
            await interaction.response.send_message(f"已放逐指定成員{member.name}")
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="複製伺服器頻道",description="複製所選的伺服器所有頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def copychannel(self,interaction:discord.Interaction,guildid1:str,guildid2:str):
        try:
            guild = self.bot.get_guild(int(guildid1))
            guild2 = self.bot.get_guild(int(guildid2))
            try:
                for category in guild.categories:
                    await guild2.create_category(name=category.name)
            except Exception as e:
                await interaction.response.send_message(f"錯誤:{e}")
            try:
                for channel in guild.text_channels:
                    await guild2.create_text_channel(name=channel.name, category=channel.category)
            except Exception as e:
                await interaction.response.send_message(f"錯誤:{e}")
            try:
                for channel in guild.voice_channels:
                    await guild2.create_voice_channel(name=channel.name, category=channel.category)
            except Exception as e:
                await interaction.response.send_message(f"錯誤:{e}")
            await interaction.response.send_message("執行",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="新增文字_and_語音頻道",description="新增頻道組合")
    @app_commands.checks.has_permissions(administrator=True)
    async def newcategory(self,interaction:discord.Interaction,channelname:str,categoryname:str,):
        guild = interaction.guild
        newcategory = await guild.create_category(name=categoryname,position=2)
        await guild.create_text_channel(name=channelname,category=newcategory)
        await guild.create_voice_channel(name=channelname,category=newcategory,rtc_region="japan")
        await interaction.response.send_message("執行",ephemeral=True)

    @app_commands.command(name="新增文字頻道",description="新增文字頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def newchannel(self,interaction:discord.Interaction,channelname:str,category:discord.CategoryChannel):
        try:
            guild = interaction.guild
            await guild.create_text_channel(name=channelname,category=category)
            await interaction.response.send_message("執行",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="新的表情符號",description="新增表情符號")
    async def newemoji(self,interaction:discord.Interaction,newemoji:discord.Attachment):
        if interaction.guild.id == 1238133524662325351:
            try:
                image_data = await newemoji.read()
                emoji = await interaction.guild.create_custom_emoji(name=newemoji.filename.split('.')[0], image=image_data)
                await interaction.response.send_message(f"成功新增表情符號: <:{emoji.name}:{emoji.id}>")
            except Exception as e:
                await interaction.response.send_message(f"錯誤:{e}")
                
    @app_commands.command(name="隱藏語音頻道",description="隱藏語音頻道並只讓當前在於頻道內的人可見該頻道")
    async def hide_voice_channel(self,interaction:discord.Interaction,channel:discord.VoiceChannel):
        try:
            guildmembers = interaction.guild.members
            for guildmember in guildmembers:
                await channel.set_permissions(guildmember, read_messages=False)
            channelmembers = channel.members
            membername = "已給予:"
            for member in channelmembers:
                await channel.set_permissions(member, read_messages=True)
                membername += f"{member.name},"
            await interaction.response.send_message(f"{membername}觀看權限",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))