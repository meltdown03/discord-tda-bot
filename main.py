import discord
from discord.ext.commands import bot

from const import DC_TOKEN
from dcBot import DCBot

intents = discord.Intents.default()
intents.members = True

dc = bot.Bot(command_prefix="/", intents=intents,
             activity=discord.Game("type /start to connect to TDA"))
dc.add_cog(DCBot(dc))

if __name__ == "__main__":
    dc.run(DC_TOKEN)
