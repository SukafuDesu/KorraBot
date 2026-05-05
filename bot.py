import asyncio

import discord

from core.bot import Bot
from cogs.audio import context_menu_commands

bot = Bot(intents=discord.Intents.all())
GUILD_ID = 872277713304576010

async def main():
    await bot.load_extension("cogs.audio.disconnect")
    await bot.load_extension("cogs.audio.listeners")
    await bot.load_extension("cogs.audio.play")
    await bot.load_extension("cogs.audio.skip")
    await bot.load_extension("cogs.audio.queue")
    await bot.load_extension("cogs.korra.qotd")
    await bot.load_extension("cogs.korra.action")
    await bot.load_extension("cogs.korra.motivational")
    await bot.load_extension("cogs.korra.voting")
    await bot.load_extension("cogs.korra.huggingface")
    await bot.load_extension("cogs.events")
    
    context_menu_commands.init(bot)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Synced globally as {bot.user}")
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"Synced to guild {GUILD_ID}")

asyncio.run(main())

bot.run(bot.config["token"])
