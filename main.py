import discord

from discord.ext.commands import bot

from dcBot import dcBot
from const import *

intents = discord.Intents.default()
intents.members = True

dc = bot.Bot(command_prefix="/",intents=intents)
dc.add_cog(dcBot(dc))

if __name__ == "__main__":
  dc.run(DC_TOKEN)
