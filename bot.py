import discord
import random
import os
import sys
import traceback
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
    t = Thread(target=run, daemon=True)
    t.start()

# ===== Discord Bot =====
TOKEN = os.environ.get("TOKEN", "")
print(f"[DEBUG] TOKEN: {'設定済み' if TOKEN else '未設定'}", flush=True)

if not TOKEN:
    print("[FATAL] 環境変数 TOKEN が設定されていません", flush=True)
    sys.exit(1)

print(f"[DEBUG] discord.py バージョン: {discord.__version__}", flush=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"[DEBUG] BASE_DIR: {BASE_DIR}", flush=True)

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

for item in RESPONSES:
    item["image"] = os.path.join(BASE_DIR, item["image"])
    print(f"[DEBUG] {item['image']} 存在: {os.path.exists(item['image'])}", flush=True)

@bot.event
async def on_ready():
    print(f"[DEBUG] ログイン成功: {bot.user}", flush=True)
    try:
        synced = await bot.tree.sync()
        print(f"[DEBUG] グローバルコマンド同期完了: {len(synced)}個", flush=True)
    except Exception as e:
        print(f"[ERROR] 同期エラー: {e}", flush=True)
        traceback.print_exc()

@bot.tree.command(name="松本", description="ランダムに松本ミームを送信する")
async def matsumoto(interaction: discord.Interaction):
    choice = random.choice(RESPONSES)
    img_path = choice["image"]
    
    if not os.path.exists(img_path):
        await interaction.response.send_message(
            content=f"{choice['text']}\n⚠️画像が見つかりません: `{img_path}`"
        )
        return
    
    await interaction.response.send_message(
        content=choice["text"],
        file=discord.File(img_path)
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    if bot.user not in message.mentions:
        return
    
    choice = random.choice(RESPONSES)
    img_path = choice["image"]
    if os.path.exists(img_path):
        await message.channel.send(content=choice["text"], file=discord.File(img_path))
    else:
        await message.channel.send(content=f"{choice['text']}\n⚠️画像が見つかりません")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"[ERROR] スラッシュコマンドエラー: {error}", flush=True)
    if not interaction.response.is_done():
        await interaction.response.send_message("エラーが発生しました", ephemeral=True)

keep_alive()

print("[DEBUG] bot.run() を開始します", flush=True)
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"[FATAL] bot.run() 例外: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
