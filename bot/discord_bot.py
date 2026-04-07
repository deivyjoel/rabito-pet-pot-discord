import discord

from discord.ext import commands
from bot.rabito_cog import RabitoCog

async def create_bot(api):
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f'Bot is ready. Logged in as {bot.user}')
    
    # Cargar cogs
    await bot.add_cog(RabitoCog(bot, api))
    
    return bot
