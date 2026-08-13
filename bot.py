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
    {"text": "クイヤ", "image": "images/IMG_9158.jpeg"},
    {"text": "よかったこの距離で", "image": "images/IMG_9159.jpeg"},
    {"text": "浜田の嫁に電話するとか", "image": "images/IMG_9160.jpeg"},
    {"text": "最後の餃子か", "image": "images/IMG_9161.jpeg"},
    {"text": "定食屋のテレビの位置やで", "image": "images/IMG_9162.jpeg"},
    {"text": "お祭り男か", "image": "images/IMG_9163.jpeg"},
    {"text": "...", "image": "images/IMG_9164.jpeg"},
    {"text": "「サザエでございます」みたいに言うな", "image": "images/IMG_9165.jpeg"},
]

@bot.event
async def on_ready():
    print(f"ログイン: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user not in message.mentions:
        return

    choice = random.choice(RESPONSES)
    await message.channel.send(
        content=choice["text"],
        file=discord.File(choice["image"])
    )

keep_alive()
bot.run(TOKEN)
