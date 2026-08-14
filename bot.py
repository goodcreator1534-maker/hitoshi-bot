import discord
import random
import os
from discord.ext import commands
from flask import Flask
from threading import Thread

# ===== Renderでスリープしないよう対策 =====
app = Flask('')

@app.route('/')
def home():
    return "松本ランダムbot起動中"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== Discord Bot =====
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

RESPONSES = [
    {"text": "よかったこの距離で", "image": "images/IMG_9158.jpeg"},
    {"text": "お祭り男か", "image": "images/IMG_9159.jpeg"},
    {"text": "クイヤ", "image": "images/IMG_9160.jpeg"},
    {"text": "最後の餃子か", "image": "images/IMG_9161.jpeg"},
    {"text": "定食屋のテレビの位置やで", "image": "images/IMG_9162.jpeg"},
    {"text": "「サザエでございます」みたいに言うな", "image": "images/IMG_9163.jpeg"},
    {"text": "...", "image": "images/IMG_9164.jpeg"},
    {"text": "浜田の嫁に電話するとか", "image": "images/IMG_9165.jpeg"},
    {"text": "すみません難しいタレントで", "image": "images/IMG_9203.jpeg"},
]

_synced = False

@bot.event
async def on_ready():
    global _synced
    print(f"ログイン: {bot.user}")
    
    # 同期は初回1回だけ（再接続時の重複防止）
    if not _synced:
        try:
            synced = await bot.tree.sync()
            print(f"グローバルコマンド {len(synced)}個 同期完了")
            _synced = True
        except Exception as e:
            print(f"同期エラー: {e}")

# ===== スラッシュコマンド =====
@bot.tree.command(name="松本", description="ランダムに松本ミームを送信する")
async def matsumoto(interaction: discord.Interaction):
    choice = random.choice(RESPONSES)
    image_path = choice["image"]
    
    # 画像が見つからない場合のフォールバック（これがないと「応答しません」になる）
    if not os.path.exists(image_path):
        print(f"画像が見つかりません: {image_path}")
        await interaction.response.send_message(
            content=f"{choice['text']}\n⚠️画像が見つかりません: `{image_path}`"
        )
        return
    
    await interaction.response.send_message(
        content=choice["text"],
        file=discord.File(image_path)
    )

# ===== メンション反応 =====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # プレフィックスコマンド処理を維持（!command 用）
    await bot.process_commands(message)
    
    if bot.user not in message.mentions:
        return

    choice = random.choice(RESPONSES)
    image_path = choice["image"]
    
    if os.path.exists(image_path):
        await message.channel.send(
            content=choice["text"],
            file=discord.File(image_path)
        )
    else:
        await message.channel.send(
            content=f"{choice['text']}\n⚠️画像が見つかりません: `{image_path}`"
        )

# ===== エラーハンドリング（必須）=====
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"コマンドエラー: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message("エラーが発生しました", ephemeral=True)

keep_alive()
bot.run(TOKEN)
