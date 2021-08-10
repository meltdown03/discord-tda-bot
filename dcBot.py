import os

import discord
from discord import colour
from discord.ext import commands
from httpx._exceptions import HTTPStatusError

from const import ACCT_ID, CLIENT_ID, DC_ID, RED_URL, TOKEN_PATH
from tdaBot import TDABot


class DCBot(commands.Cog, name="TDA Cog"):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    def set_tdaclient(self, client_id, ref_url=None):
        self.tda_client = TDABot(self.bot, self, client_id, ref_url)

    @property
    def get_bot_user(self):
        return self.bot.get_user(DC_ID)

    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self.bot))

    @commands.command()
    async def start(self, ctx):
        user = self.get_bot_user
        if ctx.author == user:
            if CLIENT_ID and ACCT_ID and RED_URL and os.access(TOKEN_PATH, 2):
                await user.send("Credentials found")
                self.set_tdaclient(CLIENT_ID)
                await self.tda_client.update_game()
                await self.tda_client.read_stream(user, ACCT_ID)

            user = self.get_bot_user
            await user.send("TDA Bot Online, enter TDA acount number:")
            try:
                account_id = await self.bot.wait_for('message', timeout=240.0, check=lambda m: (m.author == user))
                account_id = account_id.content

            except TimeoutError:
                await user.send("Timed out, restart bot")

            await user.send("Enter TDA API client ID:")
            try:
                client_id = await self.bot.wait_for('message', timeout=240.0, check=lambda m: (m.author == user))
                client_id = client_id.content

            except TimeoutError:
                await user.send("Timed out, restart bot")

            if not os.access(TOKEN_PATH, 2):
                await user.send("Enter TDA API redirect URL:")
                try:
                    ref_url = await self.bot.wait_for('message', timeout=600.0, check=lambda m: (m.author == user))
                    ref_url = ref_url.content
                    self.set_tdaclient(client_id, ref_url)
                    try:
                        await self.tda_client.update_game()
                        await self.tda_client.read_stream(user, account_id)

                    except HTTPStatusError as e:
                        await user.send(f"Error: {e}")

                except TimeoutError:
                    await user.send("Timed out, restart bot")

            else:
                try:
                    self.set_tdaclient(client_id)
                    try:
                        await self.tda_client.update_game()
                        await self.tda_client.read_stream(user, account_id)

                    except HTTPStatusError as e:
                        await user.send(f"Error: {e}")

                except HTTPStatusError as e:
                    await user.send(f"Error: {e}")
        else:
            await ctx.user.send("Unauthorized, please ask the Server owner/admin to start the bot")

    @commands.command()
    async def bal(self, ctx):
        await self.tda_client.update_game()
        bal = await self.tda_client.get_bal
        embed = discord.Embed(title="Net Liq. Balance:", type="rich",
                              colour=discord.Color.dark_green(), description=f"${bal:.2f}")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def bp(self, ctx):
        await self.tda_client.update_game()
        bp = await self.tda_client.get_bp
        embed = discord.Embed(title="Buying Power:", type="rich",
                              colour=discord.Color.dark_green(), description=f"${bp:.2f}")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def pos(self, ctx):
        await self.tda_client.update_game()
        pos = await self.tda_client.get_pos
        embed = discord.Embed(title="Positions:", type="rich",
                              colour=discord.Color.dark_green(), description=pos)
        await ctx.channel.send(embed=embed)
