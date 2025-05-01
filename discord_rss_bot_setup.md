# Discord Instagram RSS Bot – Local Setup Guide

A concise, step-by-step guide to run a Discord bot locally that fetches Instagram posts from an RSS feed.

---

## 📁 Project Structure

```
DiscordBot/
├── bot.py
├── .env
├── .gitignore
├── requirements.txt
├── venv/
```

---

## ⚙️ 1. Environment Setup

```bash
cd ~/Documents
mkdir DiscordBot && cd DiscordBot
python3 -m venv venv
source venv/bin/activate
pip install discord.py feedparser python-dotenv
pip freeze > requirements.txt
```

---

## 🛡️ 2. .env Configuration

Create a `.env` file with:

```env
DISCORD_TOKEN=your-bot-token
CHANNEL_ID=your-channel-id
INSTAGRAM_RSS=https://your-rss-feed.xml
```

- `DISCORD_TOKEN`: from the [Discord Developer Portal](https://discord.com/developers/applications)
- `CHANNEL_ID`: right-click the channel in Discord and select **"Copy Channel ID"** (Developer Mode must be enabled)
- `INSTAGRAM_RSS`: from a service like [rss.app](https://rss.app)

---

## 📦 3. .gitignore (Recommended)

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## 🧠 4. bot.py Template

```python
import os
import discord
import feedparser
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
INSTAGRAM_RSS = os.getenv("INSTAGRAM_RSS")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

latest_post = None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    check_instagram_feed.start()

@bot.command()
async def hello(ctx):
    await ctx.send("👋 Hello! I'm alive.")

@bot.command()
async def cica(ctx):
    feed = feedparser.parse(INSTAGRAM_RSS)
    if feed.entries:
        await ctx.send(f"📸 Latest post: {feed.entries[0].link}")
    else:
        await ctx.send("No entries found.")

@tasks.loop(minutes=5)
async def check_instagram_feed():
    global latest_post
    feed = feedparser.parse(INSTAGRAM_RSS)
    if feed.entries:
        newest = feed.entries[0]
        if newest.link != latest_post:
            latest_post = newest.link
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"📸 New Instagram post: {newest.link}")

bot.run(TOKEN)
```

---

## ▶️ 5. Run the Bot

```bash
source venv/bin/activate
python bot.py
```

---

✅ Your bot is now live locally, listening to commands, and posting the latest Instagram RSS feed items to your Discord channel.


---

## 🔑 6. Creating a Discord Bot & Retrieving Token & Channel ID

### 🧱 A. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**, give it a name, and click **Create**
3. In the left sidebar, go to **"Bot"**, then click **"Add Bot"**
4. Customize your bot (optional): name, avatar

---

### 🔐 B. Get Your Bot Token

1. Go to your bot’s **Bot** section in the Developer Portal
2. Click **“Reset Token”** (if needed), then **Copy** the token
3. Paste it in your `.env`:

```env
DISCORD_TOKEN=your-token-here
```

> ⚠️ Keep your token secret. Never share it publicly.

---

### 📢 C. Get the Channel ID

1. In Discord, go to **User Settings → Advanced → Enable Developer Mode**
2. Right-click the **text channel** you want the bot to post in
3. Select **"Copy Channel ID"**
4. Paste into your `.env`:

```env
CHANNEL_ID=123456789012345678
```

---

### 🔗 D. Invite the Bot to Your Server

Use this URL format, replacing `YOUR_CLIENT_ID`:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=274878221440
```

- `YOUR_CLIENT_ID` = Application ID (found under "General Information")
- Open in browser, select your server, and click **Authorize**
