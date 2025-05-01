import os
import discord
import feedparser
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)
INSTAGRAM_RSS = os.getenv("INSTAGRAM_RSS")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send("👋 Hello! I'm alive and ready!")

@bot.command()
async def cica(ctx):
    """Posts the latest Instagram RSS feed entry."""
    feed = feedparser.parse(INSTAGRAM_RSS)
    if feed.entries:
        latest_entry = feed.entries[0]
        await ctx.send(f"📸 New post: {latest_entry.link}")
    else:
        await ctx.send("No entries found in the feed!")

bot.run(TOKEN)

