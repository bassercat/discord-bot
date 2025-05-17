# -*- coding: utf-8 -*-

# 安裝需要的套件 RANDER取消
#!pip install -q discord.py nest_asyncio

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

# 修補 Colab 的 asyncio loop 問題
#nest_asyncio.apply()
# 禁用語音套件警告
discord.VoiceClient.warn_nacl = False

"""#==========擋RANDER========== aiohttp 網頁伺服器
from aiohttp import web
#==========擋RANDER========== aiohttp 網頁伺服器"""

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

# ============================== 🛠️ 自訂設定區 ==============================



# 建立機器人
bot = commands.Bot(command_prefix='!', intents=intents)



"""#==========擋RANDER========== aiohttp 網頁伺服器 xranderB
async def xranderA(request):
    return web.Response(text="dorororo")

async def xranderB():
    app = web.Application()
    app.router.add_get('/', xranderA)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)  # 監聽0.0.0.0，端口8080（Render要求）
    await site.start()
    print("Web server started on port 8080")
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB"""



"""#==========擋RANDER========== xranderC 10min ping

async def xranderC():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            channel = bot.get_channel(S_COMMAND_CHANNELS)
            if channel:
                async for _ in channel.history(limit=1):
                    pass  # fake request
            print("10min ping")
        except Exception as e:
            print(f"{e}")
        await asyncio.sleep(600)  # 每 10 分鐘
        
#==========擋RANDER========== xranderC"""



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
    emoji_map = {e.name: e for e in ctx.guild.emojis}

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



# 抽卡功能===========================================================================***



# 檢測抽 > /d
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 只有特定頻道才觸發
    if message.channel.id == DRAW_CHANNELS and message.content.strip() == "抽":
        ctx = await bot.get_context(message)
        try:
            await drawcard.invoke(ctx)  # 呼叫指令，會自動處理 cooldown
        except CommandOnCooldown as e:
            pass
        return
    await bot.process_commands(message)  # 其他指令照常處理


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
async def drawcard(ctx):
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

    #整理訊息
    draw_text = ""
    draw_text = "十抽結果：\n"
    draw_text += f"R 共{count_R}隻\n"
    draw_text += f"SR 共{count_SR}隻\n"

    pickup_name = ssr_pickup[0]
    if pickup_name in ssr_counter:
        draw_text += f"{pickup_name} 共{ssr_counter[pickup_name]}隻\n"
        del ssr_counter[pickup_name]

    for name in sorted(ssr_counter):
        draw_text += f"{name} 共{ssr_counter[name]}隻\n"
    #送出
    await ctx.send(draw_text)



#機率檢測 /prob
@bot.command(name="prob")
@is_allowed_user()
async def show_prob(ctx):
    if ctx.channel.id != DRAW_CHANNELS:
        return
    #嵌入訊息
    prob_check_embed = discord.Embed(
        title="抽卡機率設定",
        color=discord.Color.blue()
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



# =======================================================================

# 當機器人啟動時
@bot.event
async def on_ready():
    print(f'✅ 機器人已上線：{bot.user}')
    activity = discord.CustomActivity(name=CUSTOM_ACTIVITY_TEXT)
    await bot.change_presence(status=discord.Status.online, activity=activity)

"""#==========擋RANDER========== xranderC
# 啟動 xranderC
    bot.loop.create_task(xranderC())
#==========擋RANDER========== xranderC"""

# 啟動每日定時任務（只有在啟用時）
    if ENABLE_DAILY_MESSAGE and not daily_message_task.is_running():
        daily_message_task.start()

# =======================================================================

# 🔐 輸入你的機器人 TOKEN

# RANDER環境變數
TOKEN = os.getenv("DISCORD_TOKEN")

# main() 函式裡面加這行同時啟動機器人跟web server
async def main():
# 同時啟動機器人跟web server
    await asyncio.gather(
        bot.start(TOKEN),
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB
#        xranderB()
#==========擋RANDER========== aiohttp 網頁伺服器 xranderB
    )

if __name__ == "__main__":
    asyncio.run(main())


