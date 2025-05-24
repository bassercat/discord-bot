# 安裝需要的套件 RANDER取消
!pip install -q discord.py nest_asyncio
#####
#!pip install pynacl
#####

# 匯入模組
import nest_asyncio
import discord
from discord.ext import commands, tasks
import asyncio
import time
import os
import random
from datetime import datetime
import pytz
from collections import Counter
from discord.ui import Button, View
from discord.ext.commands import CommandOnCooldown



# 修補 Colab 的 asyncio loop 問題
nest_asyncio.apply()
# 禁用語音套件警告
discord.VoiceClient.warn_nacl = False

#==========擋RANDER========== aiohttp 網頁伺服器
#from aiohttp import web
#==========擋RANDER========== aiohttp 網頁伺服器

# 設定 Intents（允許讀取訊息內容）
intents = discord.Intents.default()
intents.message_content = True

# 工具函式：支援頻道 ID（int 或 str）或頻道名稱（str）
def get_channel_by_name_or_id(guild, identifier):
    if isinstance(identifier, int):
        return guild.get_channel(identifier)
    elif isinstance(identifier, str) and identifier.isdigit():
        return guild.get_channel(int(identifier))
    else:
        return discord.utils.get(guild.text_channels, name=identifier)

# 白名單
def is_allowed_user():
    async def predicate(ctx):
        return ctx.author.id in ALLOWED_USER_IDS
    return commands.check(predicate)



#============================== 🛠️ 自訂設定區 ==============================
# 取得台灣時間
tz = pytz.timezone('Asia/Taipei')

T = True
F = False

# 允許使用指令的成員ID清單
ALLOWED_USER_IDS = [
    358124858552614912
]

# BOT狀態
CUSTOM_ACTIVITY_TEXT = "跟塔羅有關的問題麻煩請傳私訊～"

# /s/e鍵入頻道
COMMAND_CHANNELS = 1372864336376365099
# /s/e每日定時輸出之頻道 N
S_COMMAND_CHANNELS = 1333115184981479456


# 簽到網址
link = "https://discord.com/channels/946719263866101821/1300742310186975232"

# 每日定時訊息文字（台北時間）可用:EMOJI:
DAILY_MESSAGE_TEXT = "寶子們簽到了\n{link}"

# 每日定時訊息發送時間（24小時制）
DAILY_MESSAGE_HOUR = 23   # 預設晚上11點
DAILY_MESSAGE_MINUTE = 0  # 預設0分

# 是否啟用定時訊息功能（預設為 False）
ENABLE_DAILY_MESSAGE = F

# ============================== 🛠️ 自訂設定區 ==============================

DRAW_CHANNELS = 1372912206127169596
MANY_DRAW = 10
CD = 60

ssr_pickup = ["阿爾卡娜"]
ssr_pilgrims = [
    "哈蘭", "白雪公主", "諾雅", "紅蓮", "伊莎貝爾", "長髮公主", "神罰",
    "桃樂絲", "小紅帽", "紅蓮：暗影", "皇冠", "小美人魚",
    "灰姑娘", "格拉維", "拉毗：小紅帽"
]
ssr_others = [
    "麥斯威爾", "舒格", "艾可希雅", "愛麗絲", "艾瑪", "尤妮", "普麗瓦蒂", "尤莉亞", "普琳瑪",
    "西格娜", "波莉", "米蘭達", "布麗德", "索林", "迪賽爾", "桑迪", "銀華", "德雷克",
    "克拉烏", "梅里", "艾德米", "吉蘿婷", "魯德米拉", "楊", "艾菲涅爾", "阿莉亞", "沃綸姆",
    "諾伊斯", "富克旺", "梅登", "麗塔", "諾薇兒", "朵拉", "露菲", "尤爾夏", "米爾克", "佩珀",
    "貝斯蒂", "海倫", "拉普拉斯", "豺狼", "毒蛇", "可可", "索達", "餅乾", "櫻花", "D",
    "布蘭兒", "諾亞爾", "羅珊娜", "尼羅", "馬斯特", "馬律哈那", "娜嘉", "蒂亞", "基里",
    "托比", "萊昂納", "牡丹", "普麗瓦蒂：不友善的女僕", "愛德", "伊萊格", "D：殺手妻子",
    "貝伊", "特羅尼", "索達：閃亮兔女郎", "愛麗絲：仙境兔女郎", "克雷伊", "愛因", "茨瓦伊",
    "露姬", "坎西：逃生女王", "潘托姆", "魯瑪妮", "芙蘿拉", "瑪娜", "瑪斯特：浪漫的女僕",
    "安克：天真的女僕", "特蕾娜", "布蕾德", "克勞斯特"
]

#SSR總數
total_ssr_pilgrims=len(ssr_pilgrims)
total_ssr_others=len(ssr_others)

prob_R = 0.53
prob_SR = 0.43
prob_SSR = 0.04

ssr_pickup_prob = 0.02
ssr_pilgrims_prob = 0.005
ssr_others_prob = 0.015

pic_doro_gold="https://cdn.discordapp.com/attachments/1374057184622542978/1374067299241427094/fd758e70-7514-4208-9e4a-ffcf8a7f9237.png?ex=682cb365&is=682b61e5&hm=b446fc8b6917362149dacfa5487780ef530bc3ef31e2f08d2ff8dfe260c5c70d&"
pic_doro_blue="https://cdn.discordapp.com/attachments/1374057184622542978/1374067298515685396/doro_trophy_blue.png?ex=682cb364&is=682b61e4&hm=678fbc0a02ba570f4b68b57e3d87ff4d8f6a850d22d85229d6c29c37cc28402b&"
pic_draw_r="https://cdn.discordapp.com/attachments/1374057184622542978/1374067166000971857/A3.jpg?ex=682cb345&is=682b61c5&hm=bdfaec7d9f16d69e7609bc21c49dddfd575a1cfdf0ff4669095b2eb285cdfd12&"
pic_draw_sr="https://cdn.discordapp.com/attachments/1374057184622542978/1374067166663676024/A2.png?ex=682cb345&is=682b61c5&hm=dcb271086d41b26823ed9429ff84674b194bec4412c7220208f755abbabe9054&"
pic_draw_ssr="https://cdn.discordapp.com/attachments/1374057184622542978/1374067166382395392/2025-05-20_002311.jpg?ex=682cb345&is=682b61c5&hm=ffffc9445ce24a0d3de243e446969a4820cfa98de4f4ddfb500bff545d6c1a50&"
pic_wawa_0="https://cdn.discordapp.com/attachments/1374057184622542978/1374075575718641674/WAWAWA_-_.png?ex=682cbb1a&is=682b699a&hm=791c83ed571e557f6c39470078cd37a2642357e11d00b41d26e7321019e6bd97&"
pic_wawa_1="https://cdn.discordapp.com/attachments/1374057184622542978/1374070504121700463/WAWAWA.png?ex=682cb661&is=682b64e1&hm=136ff29078ec23a6a91f30bfdd5aa69c8ae1297fa9d73a97f4c05be35bfb1cdc&"
pic_wawa_2="https://cdn.discordapp.com/attachments/1374057184622542978/1374070504549384252/WAWA_-_2.png?ex=682cb661&is=682b64e1&hm=f6d4a1d0220a6b965b4ba5d7eaeace5f05377e9320e0c341d5cb0e842a0e6276&"
pic_wawa_3="https://cdn.discordapp.com/attachments/1374057184622542978/1374070503660191916/WAWA_-_.png?ex=682cb661&is=682b64e1&hm=6c5a67434d8baf73348bac016fa41c1c22c2ad676ff0af608170b81263727aa7&"


# ============================== 🛠️ 自訂設定區 ==============================



# 建立機器人
bot = commands.Bot(command_prefix='!', intents=intents)



#==========擋RANDER========== aiohttp  xranderB
#async def xranderA(request):
#    return web.Response(text="dorororo")
#
#async def xranderB():
#    app = web.Application()
#    app.router.add_get('/', xranderA)
#    runner = web.AppRunner(app)
#    await runner.setup()
#    site = web.TCPSite(runner, '0.0.0.0', 8080)  # 監聽0.0.0.0，端口8080（Render要求）
#    await site.start()
#    print("Web server started on port 8080")
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB



#==========擋RANDER========== xranderC 10min ping

#async def xranderC():
#    await bot.wait_until_ready()
#    while not bot.is_closed():
#        try:
#            channel = bot.get_channel(S_COMMAND_CHANNELS)
#            if channel:
#                async for _ in channel.history(limit=1):
#                    pass  # fake request
#            print("10min ping")
#        except Exception as e:
#            pfcio.sleep(600)  # 每 10 分鐘

#==========擋RANDER========== xranderC



# 靜默處理沒有權限 冷卻中 錯誤
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        # 沒權限就不回應任何訊息
        return
    elif isinstance(error, commands.CommandOnCooldown):
        # 冷卻中也不回應任何訊息
        return
    else:
        raise error



# 每日定時任務，每分鐘檢查一次
@tasks.loop(minutes=1)
async def daily_message_task():
    if not ENABLE_DAILY_MESSAGE:
        return
    # 取得台灣時間
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)

    if now.hour == DAILY_MESSAGE_HOUR and now.minute == DAILY_MESSAGE_MINUTE:
        channel = bot.get_channel(S_COMMAND_CHANNELS)
        if channel:
            try:
                # 嘗試將 :emoji_name: 自動轉為 <:{name}:{id}>
                content = DAILY_MESSAGE_TEXT
                # 若頻道有對應的伺服器（大多情況會有）
                if channel.guild:
                    for emoji in channel.guild.emojis:
                        tag = f":{emoji.name}:"
                        code = str(emoji)
                        content = content.replace(tag, code)
                await channel.send(content)
            except Exception as e:
                print(f"{e}")



# 指令：/s
@bot.command()
async def s(ctx, *args):
    # 不在允許頻道，沒打字 不做任何回應
    if ctx.channel.id != COMMAND_CHANNELS or not args:
        return
    # 找出對應伺服器要發送的頻道ID
    target_channel = get_channel_by_name_or_id(ctx.guild, S_COMMAND_CHANNELS)
    if not target_channel:
        return

    # 判斷是否為回覆訊息
    first = args[0]
    # 如果第一個參數是超過10位數的純數字，視為訊息 ID
    if first.isdigit() and len(first) >= 10:
        message_id = int(first)
        reply_content = ' '.join(args[1:]).strip()
        if not reply_content:
            return
        try:
            target_message = await target_channel.fetch_message(message_id)
            await target_channel.send(reply_content, reference=target_message)
        except Exception as e:
            print(f"{e}")
        return

    # 如果不是回覆模式，就正常送出訊息
    await target_channel.send(' '.join(args).strip())



# 指令：/e <訊息ID> 😀❤️，幫目標頻道內的訊息加上表情
@bot.command()
async def e(ctx, message_id: int, *emojis):
    # 不在允許頻道，沒打字 不做任何回應
    if ctx.channel.id != COMMAND_CHANNELS or not emojis:
        return
    # 找出對應伺服器要發送的頻道ID
    target_channel = get_channel_by_name_or_id(ctx.guild, S_COMMAND_CHANNELS)
    if not target_channel:
        return

    # 建立名稱對應 emoji 物件字典，方便查找
    emoji_map = {emoji.name: emoji for emoji in ctx.guild.emojis}

    try:
        target_msg = await target_channel.fetch_message(message_id)
        for em in emojis:
            em_name = em.strip(':')
            emoji_obj = emoji_map.get(em_name)
            emoji_to_use = emoji_obj or em  # 使用自訂 emoji 物件或原始字串

            already_reacted = False
            for reaction in target_msg.reactions:
                # reaction.emoji 是 Emoji 物件或字串
                if (emoji_obj and isinstance(reaction.emoji, discord.Emoji) and reaction.emoji.id == emoji_obj.id) or \
                   (not emoji_obj and str(reaction.emoji) == em_name):
                    async for user in reaction.users():
                        if user == bot.user:
                            already_reacted = True
                            break
                if already_reacted:
                    break

            # 移除/加反應
            if already_reacted:
                try:
                    await target_msg.remove_reaction(emoji_to_use, bot.user)
                except Exception as e:
                    print(f"{e}")
            else:
                try:
                    await target_msg.add_reaction(emoji_to_use)
                except Exception as e:
                    print(f"{e}")
    except Exception as e:
        print(f"{e}")



# 輸入取代指令===========================================================================***

# 設為 False 可以關閉自動 emoji 反應功能
ENABLE_AUTO_EMOJI_REACT = T
# 挑訊息反應EMOJI的預設反應
BOT_EMOJIS = ["z_arcane_angry","z_arcane_lol","z_arcane_ori","z_arcane_shy","z_arcane_sleep","z_arcane_smile","z_arcane_surprise"]  # 改成你的emoji名字

# 檢測
@bot.event
async def on_message(message):
    # 忽略自己
    if message.author.bot:
      return



# 挑訊息反應EMOJI================================

    # 挑訊息反應EMOJI
    if message.channel.id == S_COMMAND_CHANNELS and ENABLE_AUTO_EMOJI_REACT:



      if random.random() < 0.01: # % 機率反應

        typing_context = message.channel.typing()
        await typing_context.__aenter__()
        await asyncio.sleep(3)
        await typing_context.__aexit__(None, None, None)
        # 顯示打字中...
        await asyncio.sleep(5)  # 可調整的後延遲，讓輸入狀態自然消失





        # 建立名稱對應 emoji 物件字典，方便查找
        emoji_map = {emoji.name: emoji for emoji in message.guild.emojis}

        # 隨機選擇一個 emoji 名稱
        chosen_name = random.choice(BOT_EMOJIS)
        emoji_obj = emoji_map.get(chosen_name)
        emoji_to_use = emoji_obj or chosen_name  # 自訂 emoji 或 Unicode 字串

        # 檢查是否已經加過這個表情
        already_reacted = False
        for reaction in message.reactions:
            if (emoji_obj and isinstance(reaction.emoji, discord.Emoji) and reaction.emoji.id == emoji_obj.id) or \
               (not emoji_obj and str(reaction.emoji) == chosen_name):
                async for user in reaction.users():
                    if user == bot.user:
                        already_reacted = True
                        break
            if already_reacted:
                break

        # 加反應（如果尚未加過）
        if not already_reacted:
            try:
                await message.add_reaction(emoji_to_use)
            except Exception:
                pass



# 挑訊息反應EMOJI================================





    # 只有特定頻道才觸發
    if message.channel.id == DRAW_CHANNELS and message.content.strip() == "抽":
        ctx = await bot.get_context(message)
        try:
            await draw_card.invoke(ctx)  # 呼叫指令，會自動處理 cooldown
        except CommandOnCooldown as e:
            pass
        return
    if message.channel.id == DRAW_CHANNELS and message.content.strip() == "玩":
        ctx = await bot.get_context(message)
        try:
            await find_doro.invoke(ctx)  # 呼叫指令，會自動處理 cooldown
        except CommandOnCooldown as e:
            pass
        return
    if message.channel.id == DRAW_CHANNELS and message.content.strip() == "擦":
        ctx = await bot.get_context(message)
        try:
            await rub_doll.invoke(ctx)  # 呼叫指令，會自動處理 cooldown
        except CommandOnCooldown as e:
            pass
        return
    if message.channel.id == DRAW_CHANNELS and message.content.strip() == "洗":
        ctx = await bot.get_context(message)
        try:
            await random_entries.invoke(ctx)  # 呼叫指令，會自動處理 cooldown
        except CommandOnCooldown as e:
            pass
        return
    await bot.process_commands(message)  # 其他指令照常處理





    # 判斷是否在目標頻道，且訊息中包含「誰的問題」
    if message.channel.id == S_COMMAND_CHANNELS and "抽一個" in message.content:
        channel = message.channel

        # 取得最近50條訊息（排除bot訊息，也可以排除自己）
        messages = await channel.history(limit=50).flatten()
        authors = set()

        for msg in messages:
            if msg.author.bot:
                continue  # 跳過機器人訊息
            authors.add(msg.author)

        if not authors:
            return

        typing_context = message.channel.typing()
        await typing_context.__aenter__()
        await asyncio.sleep(3)



        chosen = random.choice(list(authors))
        await channel.send(f"幫你抽一個 抽到的人是{chosen.mention}！")









# 抽卡功能===========================================================================***



#模擬「抽卡」一張卡牌
def draw_one_card():
    r = random.random() # 產生一個0~1之間的隨機浮點數
    if r < prob_R:
        return "R" # 如果r小於R卡機率，回傳"R"
    elif r < prob_R + prob_SR:
        return "SR" # 如果r介於R卡機率與R+SR機率之間，回傳"SR"
    else:
        r2 = random.random() # 如果都不符合R或SR，表示是SSR，開始第二次抽SSR內部分類
        # 判斷是否是SSR裡的Pickup角色（按比例判斷）
        if r2 < ssr_pickup_prob / prob_SSR:
            return f"SSR (PICKUP) {random.choice(ssr_pickup)}"
        # 判斷是否是SSR裡的Pilgrims角色
        elif r2 < (ssr_pickup_prob + ssr_pilgrims_prob) / prob_SSR:
            return f"SSR (Pilgrims) {random.choice(ssr_pilgrims)}"
        # 剩下的SSR (Others) 角色隨機抽一個
        else:
            return f"SSR (Others) {random.choice(ssr_others)}"

# 使用commands.cooldown裝飾器
# rate=1 : 1次
# per=CD 秒冷卻 (你可以改成你想的秒數)
# BucketType.user member

@bot.command(name="抽", aliases=["d"])
@commands.cooldown(rate=1, per=CD, type=commands.BucketType.member) # 每位使用者冷卻CD秒只能執行1次
async def draw_card(ctx):
    #判斷訊息是否來自特定允許的頻道
    if ctx.channel.id != DRAW_CHANNELS:
        return

    results = [draw_one_card() for _ in range(MANY_DRAW)] #一次抽MANY_DRAW張卡

    count_R = sum(1 for c in results if c == "R") #計算幾張R
    count_SR = sum(1 for c in results if c == "SR") #計算幾張SR

    ssr_cards = [] #存放所有 SSR 卡的名稱
    for c in results:
        if c.startswith("SSR"):
            name = c.split()[-1]
            ssr_cards.append(name)

    ssr_counter = Counter(ssr_cards) #計算每張SSR總數







    #嵌入訊息

    #整理訊息
    draw_lines=[]

    if count_R != 0:
      draw_lines.append(f"R 共{count_R}隻\n")
    if count_SR != 0:
      draw_lines.append(f"SR 共{count_SR}隻\n")

    pickup_name = ssr_pickup[0]


    ####################################
    draw_embed = discord.Embed(
        title="10抽結果",
        description="",
        color=discord.Color.gold()
    )
    ####################################

    if pickup_name in ssr_counter:
        draw_lines.append(f"{pickup_name} 共{ssr_counter[pickup_name]}隻\n")
        del ssr_counter[pickup_name]

    for name in sorted(ssr_counter):
        draw_lines.append(f"{name} 共{ssr_counter[name]}隻\n")

    draw_lines.append("\n") #先空一行

    # 顯示詳細結果，輸出前移除 SSR 前綴
    cleaned_results = [
    card.split()[-1] if card.startswith("SSR") else card
    for card in results
    ]

    # 用 spoiler 標籤隱藏詳細抽卡結果
    spoiler_line = f"||{', '.join(cleaned_results)}||"
    draw_lines.append(f"{spoiler_line}")

    draw_text="".join(draw_lines)


    draw_embed.description = draw_text

    #決定圖片
    if ssr_counter or any(pickup_name in line for line in draw_lines):
      draw_embed.set_thumbnail(url=pic_draw_ssr)
    elif count_SR != 0:
      draw_embed.set_thumbnail(url=pic_draw_sr)
    elif count_R != 0:
      draw_embed.set_thumbnail(url=pic_draw_r)

    # 取得台灣時間
    draw_embed.timestamp = datetime.now(tz)

    draw_embed.set_footer(text=str(ctx.author.display_name),icon_url=ctx.author.display_avatar.url)

    #送出
    await ctx.send(embed=draw_embed)

    # 加入 Bonus 抽卡判定邏輯
    if random.random() < 0.01:  # 1% 機率觸發
        bonus_results = [draw_one_card() for _ in range(MANY_DRAW*10)]

        count_R = sum(1 for c in bonus_results if c == "R")
        count_SR = sum(1 for c in bonus_results if c == "SR")

        ssr_cards = []
        for c in bonus_results:
            if c.startswith("SSR"):
                name = c.split()[-1]
                ssr_cards.append(name)

        ssr_counter = Counter(ssr_cards)

        draw_lines = []

        ####################################
        bonus_embed = discord.Embed(
            title="🎉Bonus額外100抽結果",
            description="",
            color=discord.Color.purple()
        )
        ####################################

        if count_R != 0:
            draw_lines.append(f"R 共{count_R}隻\n")
        if count_SR != 0:
            draw_lines.append(f"SR 共{count_SR}隻\n")

        if pickup_name in ssr_counter:
            draw_lines.append(f"{pickup_name} 共{ssr_counter[pickup_name]}隻\n")
            del ssr_counter[pickup_name]

        for name in sorted(ssr_counter):
            draw_lines.append(f"{name} 共{ssr_counter[name]}隻\n")

        draw_lines.append("\n")

        cleaned_results = [
            card.split()[-1] if card.startswith("SSR") else card
            for card in bonus_results
        ]

        spoiler_line = f"||{', '.join(cleaned_results)}||"
        draw_lines.append(f"{spoiler_line}")

        bonus_text = "".join(draw_lines)

        bonus_embed.description = bonus_text


        bonus_embed.timestamp = datetime.now(tz)
        bonus_embed.set_footer(text=str(ctx.author.display_name), icon_url=ctx.author.display_avatar.url)

        if ssr_counter or any(pickup_name in line for line in draw_lines):
            bonus_embed.set_thumbnail(url=pic_draw_ssr)
        elif count_SR != 0:
          bonus_embed.set_thumbnail(url=pic_draw_sr)
        elif count_R != 0:
          bonus_embed.set_thumbnail(url=pic_draw_r)

        await ctx.send(embed=bonus_embed)
    # Bonus 抽卡邏輯結束





#機率檢測 /prob
@bot.command(name="prob")
@is_allowed_user()
async def show_prob(ctx):
    if ctx.channel.id != DRAW_CHANNELS:
        return
    #嵌入訊息
    prob_check_embed = discord.Embed(
        title="抽卡機率設定",
        color=discord.Color.red()
    )

    prob_check_embed.add_field(name="本期Pick up", value=", ".join(ssr_pickup), inline=False)
    prob_check_embed.add_field(name="抽卡次數 冷卻時間", value=f"{MANY_DRAW} 次 CD {CD} 秒", inline=False)
    prob_check_embed.add_field(name="基本機率", value=f"R:{prob_R*100:.0f}%  SR:{prob_SR*100:.0f}%  SSR:{prob_SSR*100:.0f}%", inline=False)
    prob_check_embed.add_field(name="SSR個別機率", value=(
                          f"Pickup:{ssr_pickup_prob*100:.0f}%\n"
                          f"朝聖超標準:{ssr_pilgrims_prob*100:.1f}%\n"
                          f"剩餘SSR:{ssr_others_prob*100:.1f}%"
                          ),
                          inline=False)
    prob_check_embed.add_field(name="SSR數量",
                    value=(
                        f"朝聖超標準共{total_ssr_pilgrims}隻\n"
                        f"剩餘SSR共{total_ssr_others}隻"
                    ),
                    inline=False)
    prob_check_embed.add_field(name="SSR平均機率",
                    value=(
                        f"每隻朝聖超標準機率為{ssr_pilgrims_prob/total_ssr_pilgrims*100:.4f}%\n"
                        f"每隻剩餘SSR機率為{ssr_others_prob/total_ssr_others*100:.4f}%"
                    ),
                    inline=False)

    await ctx.send(embed=prob_check_embed)



# 金doro=======================================================================



# 建立按鈕類別，每個按鈕對應 grid 中的一個位置
class GridButton(Button):
    def __init__(self, row, col, true_value, author_id, parent_view):  # 【修改】新增 parent_view 參數
        # 初始為 "❓"，位置為 row，col
        super().__init__(style=discord.ButtonStyle.secondary, label="❓", row=row,
                 disabled=(author_id != parent_view.author_id))
        # 只有指令者能點 # 檢查是不是指令發出者在點按鈕
        self.row = row
        self.col = col
        self.true_value = true_value  # 真正的內容
        self.revealed = False         # 是否已被點擊過
        self.author_id = author_id    # 發出指令者的 ID，用來限制互動權限
        self.parent_view = parent_view  # 【修改】儲存父 View 以便修改計數和更新 embed

    async def callback(self, interaction: discord.Interaction):
        # 檢查是不是指令發出者在點按鈕 callback 檢查：嚴格權限控管，防止不合法操作
        if interaction.user.id != self.author_id:
            return

        # 如果已揭示過，忽略
        if self.revealed:
            await interaction.response.defer()
            return

        # ✅ 防洗點 — 點擊後先 disable 所有按鈕
        for child in self.parent_view.children:
            if isinstance(child, Button):
                child.disabled = True


        # 揭示正確內容並更換樣式 # 揭示 emoji（顯示 emoji 本體）
        self.label = None         # label 設為 None（清空）
        self.emoji = self.true_value  # 揭示 emoji
        self.style = discord.ButtonStyle.secondary
        self.revealed = True
        self.disabled = True  # 禁用按鈕

        # 【修改】點擊計數 +1
        self.parent_view.flipped_count += 1



        # 【修改】如果是金 Doro，就停用所有按鈕
        if self.true_value.name == "doro_trophy":
            for child in self.parent_view.children:
                if isinstance(child, Button):
                    child.disabled = True
            # 更新 embed 內容為最終狀態
            embed = interaction.message.embeds[0]
            embed.description = f"{self.parent_view.flipped_count}/25"
            embed.set_thumbnail(url=pic_doro_gold)
            await interaction.response.edit_message(embed=embed, view=self.parent_view)
            return

        # 【修改】不是金 Doro，更新 embed 描述，顯示目前翻開數
        embed = interaction.message.embeds[0]
        embed.description = f"{self.parent_view.flipped_count}/25"
        embed.set_thumbnail(url=pic_doro_blue)

        # ✅ 重新啟用未翻過的按鈕
        for child in self.parent_view.children:
            if isinstance(child, Button) and not getattr(child, "revealed", False):
                child.disabled = False

        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# 按鈕 View，控制整個 5x5 按鈕盤
class GridView(View):
    def __init__(self, author_id, emoji_map, ctx):  # 【修改】新增 ctx 參數
        super().__init__(timeout=None)  # 不自動過期
        self.author_id = author_id
        self.ctx = ctx                  # 【修改】保留 ctx 以便未來需要使用（目前沒用也可以移除）
        self.flipped_count = 0          # 【修改】新增已翻開按鈕計數

        # 產生 1 個 A、24 個 B
        items = [emoji_map.get("doro_trophy")] + [emoji_map.get("doro_trophy_blue")] * 24
        random.shuffle(items)
        self.grid = [items[i * 5:(i + 1) * 5] for i in range(5)]  # 分成 5x5 的列表

        # 為每個位置建立一個按鈕，加入 View
        for row in range(5):
            for col in range(5):
                value = self.grid[row][col]
                # 【修改】新增 parent_view 參數，傳自己給按鈕
                self.add_item(GridButton(row=row, col=col, true_value=value, author_id=author_id, parent_view=self))


# 指令註冊：/p 或 /玩
@bot.command(name="p", aliases=["玩"])
@commands.cooldown(rate=1, per=CD, type=commands.BucketType.member)
async def find_doro(ctx):

    # 建立名稱對應 emoji 物件字典，方便查找
    emoji_map = {emoji.name: emoji for emoji in ctx.guild.emojis}

    find_doro_embed = discord.Embed(
	    title="尋找金Doro",
	    color=discord.Color(0xC0C0C0),
        description="0/25"  # 【修改】新增描述初始為 0/25

    )
    find_doro_embed.set_thumbnail(url=pic_doro_blue)

    # 取得台灣時間
    find_doro_embed.timestamp = datetime.now(tz)

    find_doro_embed.set_footer(text=str(ctx.author.display_name),icon_url=ctx.author.display_avatar.url)

    # 【修改】建立 View 時帶入 ctx 參數
    await ctx.send(embed=find_doro_embed, view=GridView(ctx.author.id, emoji_map, ctx))



# 擦娃娃=======================================================================

#第一層防護：按鈕狀態控制 (disabled)#######################
#第二層防護：callback 裡的身分與狀態檢查#######################

# 每種肥料對應增加的經驗值
PLUS_VALUES = {
    'R': 200,
    'SR': 500,
    'SSR': 1000,
}

# 升級所需經驗與最大等級
EXP_PER_LEVEL = 3000
MAX_LEVEL = 15

# 擦娃娃成功機率表：R 娃娃
SUCCESS_PROB_TABLE_R = [
    0.176, 0.500, 1.000,  # Lv.0
    0.208, 0.650, 1.000,  # Lv.1
    0.240, 0.750, 1.000,  # Lv.2
    0.272, 0.850, 1.000,  # Lv.3
    0.400, 1.000, 1.000,  # Lv.4
    0.160, 0.500, 1.000,  # Lv.5
    0.192, 0.600, 1.000,  # Lv.6
    0.224, 0.700, 1.000,  # Lv.7
    0.272, 0.850, 1.000,  # Lv.8
    0.400, 1.000, 1.000,  # Lv.9
    0.144, 0.450, 1.000,  # Lv.10
    0.176, 0.550, 1.000,  # Lv.11
    0.224, 0.700, 1.000,  # Lv.12
    0.272, 0.850, 1.000,  # Lv.13
    0.400, 1.000, 1.000,  # Lv.14
]

# 大成功機率表（等級0~14 × 藍紫金）你提供的資料轉成小數形式
SUCCESS_PROB_TABLE = [
    0.036, 0.110, 0.250,  # Lv.0
    0.059, 0.198, 0.400,  # Lv.1
    0.078, 0.287, 0.550,  # Lv.2
    0.113, 0.413, 0.750,  # Lv.3
    0.150, 0.550, 1.000,  # Lv.4
    0.022, 0.080, 0.200,  # Lv.5
    0.033, 0.120, 0.300,  # Lv.6
    0.049, 0.180, 0.450,  # Lv.7
    0.076, 0.280, 0.700,  # Lv.8
    0.125, 0.500, 1.000,  # Lv.9
    0.012, 0.054, 0.150,  # Lv.10
    0.022, 0.099, 0.275,  # Lv.11
    0.031, 0.144, 0.400,  # Lv.12
    0.047, 0.216, 0.600,  # Lv.13
    0.100, 0.450, 1.000,  # Lv.14
]

#  exp_loading_bar(user_data["exp"])
def exp_loading_bar(exp, max_exp=3000, length=15):
    filled_len = int(exp / max_exp * length)
    empty_len = length - filled_len
    bar = "█" * filled_len + "░" * empty_len
    return f"[{bar}]"

# 根據目前等級與肥料種類（藍/紫/金）取出對應的大成功機率
def get_success_chance(level, fertilizer_type):
    if level >= MAX_LEVEL:
      return 0.0  # 防止超出表格，滿級無大成功
    idx = level * 3
    type_idx = {'R': 0, 'SR': 1, 'SSR': 2}[fertilizer_type]
    return SUCCESS_PROB_TABLE[idx + type_idx]

# 暫存玩家的遊戲資料（記憶體，不會永久保存）
player_data = {}

# 定義擦娃娃遊戲的互動介面 View（3 個按鈕 + 狀態追蹤）
class rub_doll_class(discord.ui.View):
    def __init__(self, user_id, active_user_id=None):
        super().__init__(timeout=300)  # 遊戲自動逾時
        self.user_id = user_id

        # 如果玩家沒玩過，就初始化資料
        self.data = player_data.setdefault(user_id, {
            'level': 0,
            'exp': 0,
            'usage': {'R': 0, 'SR': 0, 'SSR': 0},
            'start_time': datetime.now(tz)
        })
        self.message = None  # 用來儲存發送的訊息物件

        level = self.data['level']

        if level >= MAX_LEVEL:
            chance_r = chance_sr = chance_ssr = "-"
        else:
            chance_r = round(get_success_chance(level, 'R') * 100, 1)
            chance_sr = round(get_success_chance(level, 'SR') * 100, 1)
            chance_ssr = round(get_success_chance(level, 'SSR') * 100, 1)

        # 【調整這邊】 按鈕禁用條件，只有持有者且未滿級能用，其他都禁用
        disabled_state = (active_user_id != self.user_id) or self.is_finished()

        self.blue_button = discord.ui.Button(label=f"R {chance_r}%", style=discord.ButtonStyle.secondary, disabled=disabled_state)
        self.purple_button = discord.ui.Button(label=f"SR {chance_sr}%", style=discord.ButtonStyle.secondary, disabled=disabled_state)
        self.gold_button = discord.ui.Button(label=f"SSR {chance_ssr}%", style=discord.ButtonStyle.secondary, disabled=disabled_state)

        self.blue_button.callback = self.blue_callback
        self.purple_button.callback = self.purple_callback
        self.gold_button.callback = self.gold_callback

        self.add_item(self.blue_button)
        self.add_item(self.purple_button)
        self.add_item(self.gold_button)

    # 判斷玩家是否已滿等
    def is_finished(self):
        return self.data['level'] >= MAX_LEVEL

    # 更新 Embed 狀態內容（等級、經驗、使用次數）與按鈕狀態
    async def update_message(self, interaction: discord.Interaction):
        rub_doll_embed = discord.Embed(title="擦娃娃", color=discord.Color.pink())

        start_time = self.data.get('start_time')
        if start_time:
            rub_doll_embed.set_footer(
                text=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url
            )
            rub_doll_embed.timestamp = start_time

        level = self.data['level']
        exp = self.data['exp']

        if level < 5:
            prefix = "☆☆☆ "
            rub_doll_embed.set_thumbnail(url=pic_wawa_0)
        elif level < 10:
            prefix = "★☆☆ "
            rub_doll_embed.set_thumbnail(url=pic_wawa_1)
        elif level < 15:
            prefix = "★★☆ "
            rub_doll_embed.set_thumbnail(url=pic_wawa_2)
        else:
            prefix = "★★★ "
            rub_doll_embed.set_thumbnail(url=pic_wawa_3)

        sparkles = " ✨" if self.data.get("last_success") else ""

        if level < MAX_LEVEL:
            level_text = f"{prefix}{level}階級{sparkles}\n"f"{exp}/{EXP_PER_LEVEL}\n"+exp_loading_bar(exp)
        else:
            level_text = f"{prefix}15階級{sparkles}\n""MAX\n""[███████████████]"

        usage_text = " ".join([f"{k}:{v * 10}個" for k, v in self.data['usage'].items()])

        rub_doll_embed.description = (
            f"{level_text}\n"
            "總用數\n"
            f"{usage_text}"
        )

        # 重新計算機率與按鈕狀態，按鈕 disabled 根據互動者是否為持有者
        if level >= MAX_LEVEL:
            chance_r = chance_sr = chance_ssr = "-"
        else:
            chance_r = round(get_success_chance(level, 'R') * 100, 1)
            chance_sr = round(get_success_chance(level, 'SR') * 100, 1)
            chance_ssr = round(get_success_chance(level, 'SSR') * 100, 1)

        self.blue_button.label = f"R {chance_r}%"
        self.purple_button.label = f"SR {chance_sr}%"
        self.gold_button.label = f"SSR {chance_ssr}%"

        # 【調整這邊】 按鈕禁用條件保持一致：持有者且未滿級能用
        disabled_state = self.is_finished() or (interaction.user.id != self.user_id)


        self.blue_button.disabled = disabled_state
        self.purple_button.disabled = disabled_state
        self.gold_button.disabled = disabled_state

        try:
            if interaction.response.is_done():
                await interaction.edit_original_response(embed=rub_doll_embed, view=self)
            else:
                await interaction.response.edit_message(embed=rub_doll_embed, view=self)
        except discord.NotFound:
            pass

        self.message = await interaction.original_response()

    async def handle_fertilizer(self, interaction: discord.Interaction, fertilizer_type: str):
        self.data["last_success"] = False

        # 僅允許發起遊戲的人操作
        if interaction.user.id != self.user_id or self.is_finished():
            return

        # 禁用所有按鈕，防止連點
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        try:
            if interaction.response.is_done():
                await interaction.edit_original_response(view=self)
            else:
                await interaction.response.edit_message(view=self)
        except discord.NotFound:
            pass

        self.data['usage'][fertilizer_type] += 1

        chance = get_success_chance(self.data['level'], fertilizer_type)

        if random.random() < chance:
            self.data["last_success"] = True
            if self.data['level'] < 5:
                self.data['level'] = 5
            elif self.data['level'] < 10:
                self.data['level'] = 10
            elif self.data['level'] < 15:
                self.data['level'] = 15
            self.data['exp'] = 0
        else:
            self.data['exp'] += PLUS_VALUES[fertilizer_type]
            while self.data['exp'] >= EXP_PER_LEVEL and self.data['level'] < MAX_LEVEL:
                self.data['level'] += 1
                if self.data['level'] in (5, 10, 15):
                    self.data['exp'] = 0
                else:
                    self.data['exp'] -= EXP_PER_LEVEL
            if self.data['level'] >= MAX_LEVEL:
                self.data['exp'] = 0

        await self.update_message(interaction)


    # 動態按鈕 callback 寫法
    async def blue_callback(self, interaction: discord.Interaction):
        await self.handle_fertilizer(interaction, "R")

    async def purple_callback(self, interaction: discord.Interaction):
        await self.handle_fertilizer(interaction, "SR")

    async def gold_callback(self, interaction: discord.Interaction):
        await self.handle_fertilizer(interaction, "SSR")

# 建立指令
@bot.command(name="c", aliases=["擦"])
@commands.cooldown(rate=1, per=CD, type=commands.BucketType.member)
async def rub_doll(ctx: commands.Context):
    user_id = ctx.author.id

    # 強制重置玩家資料（每次開遊戲都從0開始）
    player_data[user_id] = {
        'level': 0,
        'exp': 0,
        'usage': {'R': 0, 'SR': 0, 'SSR': 0},
        'start_time': datetime.now(tz)
    }

    view = rub_doll_class(user_id, active_user_id=user_id)  # 啟用持有者按鈕

    rub_doll_embed = discord.Embed(title="擦娃娃", color=discord.Color.pink())

    # 👉 修改處：起始時也加入大成功率
    level = 0
    chance_r = round(get_success_chance(level, 'R') * 100, 1)
    chance_sr = round(get_success_chance(level, 'SR') * 100, 1)
    chance_ssr = round(get_success_chance(level, 'SSR') * 100, 1)
    chance_text = f"大成功率\nR:{chance_r}% SR:{chance_sr}% SSR:{chance_ssr}%"

    rub_doll_embed.description=(
      "☆☆☆ 0階級\n"
      "[░░░░░░░░░░░░░░░]\n"
      "0/3000\n"
      "總用數\n"
      "R:0個 SR:0個 SSR:0個"
    )

    rub_doll_embed.set_thumbnail(url=pic_wawa_0)

    # 取得台灣時間
    rub_doll_embed.timestamp = datetime.now(tz)

    rub_doll_embed.set_footer(text=str(ctx.author.display_name),icon_url=ctx.author.display_avatar.url)

    view.message = await ctx.send(embed=rub_doll_embed, view=view)



"""
##
intents.message_content = True
intents.voice_states = True  # 確保能監聽語音頻道狀態

@bot.command(name="joinvc")
async def joinvc(ctx, *, channel_name_or_id: str):
    #讓 bot 加入指定的語音頻道（名稱或 ID）
    target_channel = 1333115184981479459

    # 嘗試用 ID 找頻道
    try:
        channel_id = int(channel_name_or_id)
        target_channel = discord.utils.get(ctx.guild.voice_channels, id=channel_id)
    except ValueError:
        # 否則用名稱找
        target_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name_or_id)

    if not target_channel:
        await ctx.send(f"❌ 找不到語音頻道：`{channel_name_or_id}`")
        return

    # 已在語音頻道就不要重複加入
    if ctx.voice_client:
        await ctx.voice_client.move_to(target_channel)
        await ctx.send(f"🔁 已移動到語音頻道：`{target_channel.name}`")
    else:
        await target_channel.connect()
        await ctx.send(f"✅ 已加入語音頻道：`{target_channel.name}`")

@bot.command(name="leavevc")
async def leavevc(ctx):
    #讓 bot 離開語音頻道
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 已離開語音頻道")
    else:
        await ctx.send("❌ 我不在任何語音頻道中喔")

##
"""

#洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗洗

main_prob = {
    "優越代碼傷害增加": 0.12,  # code_damage_tiers
    "命中率增加": 0.12,       # hit_rate_tiers
    "最大裝彈數增加": 0.12,   # max_ammo_tiers
    "攻擊力增加": 0.10,       # attack_tiers
    "蓄力傷害增加": 0.12,     # charge_speed_tiers
    "蓄力速度增加": 0.12,     # charge_speed_tiers
    "暴擊率增加": 0.12,       # crit_rate_tiers
    "暴擊傷害增加": 0.10,     # crit_damage_tiers
    "防禦力增加": 0.10        # defense_tiers
}

# --- 對應等級資料表 ---
max_ammo_tiers = {
    1: {"27.84%": 0.12}, 2: {"31.95%": 0.12}, 3: {"36.06%": 0.12},
    4: {"40.17%": 0.12}, 5: {"44.28%": 0.12}, 6: {"48.39%": 0.07},
    7: {"52.50%": 0.07}, 8: {"56.60%": 0.07}, 9: {"60.71%": 0.07},
    10: {"64.82%": 0.07}, 11: {"68.93%": 0.01}, 12: {"73.04%": 0.01},
    13: {"77.15%": 0.01}, 14: {"81.26%": 0.01}, 15: {"85.37%": 0.01}
}

charge_damage_tiers = hit_rate_tiers = defense_tiers = attack_tiers = {
    1: {"4.77%": 0.12}, 2: {"5.47%": 0.12}, 3: {"6.18%": 0.12},
    4: {"6.88%": 0.12}, 5: {"7.59%": 0.12}, 6: {"8.29%": 0.07},
    7: {"9.00%": 0.07}, 8: {"9.70%": 0.07}, 9: {"10.40%": 0.07},
    10: {"11.11%": 0.07}, 11: {"11.81%": 0.01}, 12: {"12.52%": 0.01},
    13: {"13.22%": 0.01}, 14: {"13.93%": 0.01}, 15: {"14.63%": 0.01}
}

crit_rate_tiers = {
    1: {"2.30%": 0.12}, 2: {"2.64%": 0.12}, 3: {"2.98%": 0.12},
    4: {"3.32%": 0.12}, 5: {"3.66%": 0.12}, 6: {"4.00%": 0.07},
    7: {"4.35%": 0.07}, 8: {"4.69%": 0.07}, 9: {"5.03%": 0.07},
    10: {"5.37%": 0.07}, 11: {"5.71%": 0.01}, 12: {"6.05%": 0.01},
    13: {"6.39%": 0.01}, 14: {"6.73%": 0.01}, 15: {"7.07%": 0.01}
}

crit_damage_tiers = {
    1: {"6.64%": 0.12}, 2: {"7.62%": 0.12}, 3: {"8.60%": 0.12},
    4: {"9.58%": 0.12}, 5: {"10.56%": 0.12}, 6: {"11.54%": 0.07},
    7: {"12.52%": 0.07}, 8: {"13.50%": 0.07}, 9: {"14.48%": 0.07},
    10: {"15.46%": 0.07}, 11: {"16.44%": 0.01}, 12: {"17.42%": 0.01},
    13: {"18.40%": 0.01}, 14: {"19.38%": 0.01}, 15: {"20.36%": 0.01}
}

code_damage_tiers = {
    1: {"9.54%": 0.12}, 2: {"10.94%": 0.12}, 3: {"12.34%": 0.12},
    4: {"13.75%": 0.12}, 5: {"15.15%": 0.12}, 6: {"16.55%": 0.07},
    7: {"17.95%": 0.07}, 8: {"19.35%": 0.07}, 9: {"20.75%": 0.07},
    10: {"22.15%": 0.07}, 11: {"23.56": 0.01}, 12: {"24.96%": 0.01},
    13: {"26.36%": 0.01}, 14: {"27.76%": 0.01}, 15: {"29.16%": 0.01}
}

charge_speed_tiers = {
    1: {"1.98%": 0.12}, 2: {"2.28%": 0.12}, 3: {"2.57%": 0.12},
    4: {"2.86%": 0.12}, 5: {"3.16%": 0.12}, 6: {"3.45%": 0.07},
    7: {"3.75%": 0.07}, 8: {"4.04%": 0.07}, 9: {"4.33%": 0.07},
    10: {"4.63%": 0.07}, 11: {"4.92%": 0.01}, 12: {"5.21%": 0.01},
    13: {"5.51": 0.01}, 14: {"5.80%": 0.01}, 15: {"6.09%": 0.01}
}

# --- 對應表 ---
effect_to_tier = {
    "優越代碼傷害增加": code_damage_tiers,
    "命中率增加": hit_rate_tiers,
    "最大裝彈數增加": max_ammo_tiers,
    "攻擊力增加": attack_tiers,
    "蓄力傷害增加": charge_damage_tiers,
    "蓄力速度增加": charge_speed_tiers,
    "暴擊率增加": crit_rate_tiers,
    "暴擊傷害增加": crit_damage_tiers,
    "防禦力增加": defense_tiers
}

def weighted_random_choice(weighted_dict):
    total = sum(weighted_dict.values())
    r = random.uniform(0, total)
    upto = 0
    for k, w in weighted_dict.items():
        if upto + w >= r:
            return k
        upto += w


def draw_effect(available_pool):
    # 抽效果名稱
    effect = weighted_random_choice(available_pool)
    # 抽數值
    tier_table = effect_to_tier[effect]
    flat_tier_prob = {v: p for d in tier_table.values() for v, p in d.items()}
    value = weighted_random_choice(flat_tier_prob)
    return effect, value


@commands.command(name="洗", aliases=["w"])
@commands.cooldown(rate=1, per=CD, type=commands.BucketType.member)
async def random_entries(ctx):

    lines = []
    pool = main_prob.copy()

    """
    def format_line(effect, value):
        tiers = effect_to_tier.get(effect, {})
        for tier_level, tier_data in tiers.items():
            if value in tier_data:
                # 在前面加上 T 等級
                tier_str = f"T{tier_level}"
                if 12 <= tier_level <= 14:
                    return f"{tier_str} [[{effect}] {value}](https://example.com)"
                elif tier_level == 15:
                    return f"{tier_str} `[{effect} {value}]`"
                else:
                    return f"{tier_str} [{effect}] {value}"
        # 如果找不到對應 tier，則不顯示等級
        return f"[{effect}] {value}"
    """

    def format_line(effect, value):
        # 假設有 tiers 查找，這裡寫示範邏輯
        tiers = effect_to_tier.get(effect, {})
        for tier_level, tier_data in tiers.items():
            if value in tier_data:
                if tier_level >= 12 and tier_level <= 14:
                    # 模擬超連結（這裡用示範連結）
                    return f"[[{effect}] {value}](https://example.com)"
                elif tier_level == 15:
                    # 用反引號模擬黑底白字
                    return f"`[{effect} {value}]`"
        # 如果沒符合條件
        return f"[{effect}] {value}"


    # 第一行（100%）
    effect1, value1 = draw_effect(pool)
    lines.append(format_line(effect1, value1))
    pool.pop(effect1)

    # 第二行（50%）
    if random.random() < 0.5 and pool:
        effect2, value2 = draw_effect(pool)
        lines.append(format_line(effect2, value2))
        pool.pop(effect2)
    else:
        lines.append("未獲得效果")

    # 第三行（30%）
    if random.random() < 0.3 and pool:
        effect3, value3 = draw_effect(pool)
        lines.append(format_line(effect3, value3))
    else:
        lines.append("未獲得效果")

    # 用 description 輸出（避免 field 空格，也讓反引號生效）
    embed = discord.Embed(
        title="TUNING COMPLETE",
        description="\n".join(lines),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1374057184622542978/1375123322597015614/c57b88d6-62ed-4008-9edc-ce25edb86b2b.png?ex=68308ae4&is=682f3964&hm=3b2f3f1f74d3594289857166b978ed4b5450133979283855e991ff66628fe1a9&")
    # 取得台灣時間
    embed.timestamp = datetime.now(tz)

    embed.set_footer(text=str(ctx.author.display_name),icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)





# =======================================================================



# 當機器人啟動時
@bot.event
async def on_ready():
    print(f'✅ 機器人已上線：{bot.user}')
    activity = discord.CustomActivity(name=CUSTOM_ACTIVITY_TEXT)
    await bot.change_presence(status=discord.Status.online, activity=activity)

#==========擋RANDER========== xranderC
# 啟動 xranderC
#    bot.loop.create_task(xranderC())
#==========擋RANDER========== xranderC

# 啟動每日定時任務（只有在啟用時）
    if ENABLE_DAILY_MESSAGE and not daily_message_task.is_running():
        daily_message_task.start()



# =======================================================================

# 🔐 輸入你的機器人 TOKEN
TOKEN = ''

# RANDER環境變數
#TOKEN = os.getenv("DISCORD_TOKEN")

# main() 函式裡面加這行同時啟動機器人跟web server
async def main():
  try:
# 同時啟動機器人跟web server
    await asyncio.gather(
        bot.start(TOKEN),
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB
#        xranderB()
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB
    )
  except KeyboardInterrupt:
    print("手動終止，準備關閉...")
    await bot.close()
    # 若webserver也有關閉協程，也要await webserver.close()，視你的實作而定

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程式已被使用者手動中斷。")
