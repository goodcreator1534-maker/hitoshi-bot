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
    {"text": "クイヤ", "image": "images/A27C1210-03FE-4AB9-815B-C30E408F28BE.jpg"},
    {"text": "よかったこの距離で", "image": "images/85E814A3-130F-40E1-90C8-1C615720989B.jpg"},
    {"text": "浜田の嫁に電話するとか", "image": "images/D032939C-E1D0-4443-A7DB-A48E09631DDE.jpg"},
    {"text": "最後の餃子か", "image": "images/CDDF6F97-3FDA-4554-A7A1-6627D06808C7.jpg"},
    {"text": "定食屋のテレビの位置やで", "image": "images/FAA98AEF-7089-43E3-98C9-20D666E4BB14.jpg"},
    {"text": "お祭り男か", "image": "images/7B85B083-E5F4-41E5-BF0C-ECD5025E8426.jpg"},
    {"text": "...", "image": "images/3C83EDED-1A52-4B1C-853F-6371C200F9A7.jpg"},
    {"text": "「サザエでございます」みたいに言うな", "image": "images/F3FBF19F-96B2-45E3-AEC0-20BF98A9BC2C.jpg"},
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
