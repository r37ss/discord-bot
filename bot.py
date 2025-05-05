import os
import discord
import feedparser
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
INSTAGRAM_RSS_URLS = os.getenv("INSTAGRAM_RSS").split(',')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Persistent storage using a simple dictionary
feed_state = {url: {'last_id': None, 'last_checked': None} for url in INSTAGRAM_RSS_URLS}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    if not check_feeds.is_running():
        check_feeds.start()

@tasks.loop(minutes=45)  # Optimized to 45-minute intervals
async def check_feeds():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    for rss_url in INSTAGRAM_RSS_URLS:
        try:
            state = feed_state[rss_url]
            
            # Skip if checked recently
            if state['last_checked'] and (datetime.now() - state['last_checked']) < timedelta(minutes=30):
                continue

            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                continue

            current_latest = feed.entries[0].id
            
            if state['last_id'] != current_latest:
                latest_entry = feed.entries[0]
                await channel.send(
                    f"📸 New Post from {feed.feed.title}\n{latest_entry.link}"
                )
                # Update state
                feed_state[rss_url] = {
                    'last_id': current_latest,
                    'last_checked': datetime.now()
                }

        except Exception as e:
            print(f"Error with {rss_url}: {str(e)}")

@bot.command()
async def hello(ctx):
    await ctx.send("👋 Hello! I'm alive and ready!")

@bot.command()
async def cica(ctx):
    """Force immediate feed check"""
    await check_feeds()
    await ctx.send("✅ Manual feed check completed!")

bot.run(TOKEN)