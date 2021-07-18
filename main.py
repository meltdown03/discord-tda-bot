import discord
import logging

from discord.ext.commands import bot

from dcBot import DCBot
from const import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='main.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

dc = bot.Bot(command_prefix="/", intents=intents,
             activity=discord.Game("type /start to connect to TDA"))
dc.add_cog(DCBot(dc))

if __name__ == "__main__":
    dc.run(DC_TOKEN)
