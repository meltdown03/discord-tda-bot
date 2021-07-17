import logging
import discord
import os
import asyncio

from discord.ext import commands
from const import DC_ID, TOKEN_PATH
from tdaBot import tdaBot
from httpx._exceptions import HTTPStatusError

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class dcBot(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def updateGame(self):
    bp = await self.tdaClient.get_bp()
    game = discord.Game(f"with ${bp}")
    await self.bot.change_presence(activity=game)

  def setTDAClient(self, client_id, ref_url=None):
    self.tdaClient = tdaBot(self.bot, self, client_id, ref_url)

  @property
  def getUser(self):
    return self.bot.get_user(DC_ID)

  @commands.Cog.listener()
  async def on_ready(self):
    print("We have logged in as {0.user}".format(self.bot))
    user = self.getUser
    await user.send("TDA Bot Online, enter TDA acount number:")

    try:
      account_id = await self.bot.wait_for('message', timeout=240.0, check=lambda m:(m.author == user))
      account_id = account_id.content
      # logger.info(f"Account Number Received: {account_id}")
    except TimeoutError:
      await user.send("Timed out, restart bot")
    # else:
    await user.send("Enter TDA API client ID:")

    try:
      client_id = await self.bot.wait_for('message', timeout=240.0, check=lambda m:(m.author == user))
      client_id = client_id.content
    # logger.info(f"Client ID Received: {client_id}")
    except TimeoutError:
      await user.send("Timed out, restart bot")
    # else:
    if not os.path.exists(TOKEN_PATH):
      await user.send("Enter TDA API redirect URL:")

      try:
        ref_url = await self.bot.wait_for('message', timeout=600.0, check=lambda m:(m.author == user))
        ref_url = ref_url.content
        # logger.info(f"Redirect URL Received: {ref_url}")
        self.setTDAClient(client_id, ref_url)

        try:
          await self.tdaClient.read_stream(user, account_id)
        except HTTPStatusError as e:
          await user.send(f"Error: {e}")

        await self.updateGame()

      except TimeoutError:
        await user.send("Timed out, restart bot")

    else:

      try:
        self.setTDAClient(client_id)
        await self.tdaClient.read_stream(user, account_id)
        await self.updateGame()

      except HTTPStatusError as e:
        await user.send(f"Error: {e}")


  @commands.command()
  async def bal(self, ctx):
    user = ctx.author
    if user.id == DC_ID:
      bal = await self.tdaClient.get_bal()
      await user.send(f"Current Value: $ {bal}")
    else:
      await user.send("Unauthorized")

  @commands.command()
  async def bp(self, ctx):
    user = ctx.author
    if user.id == DC_ID:
      bp = await self.tdaClient.get_bp()
      await user.send(f"Current Buying Power: $ {bp}")
    else:
      await user.send("Unauthorized")
