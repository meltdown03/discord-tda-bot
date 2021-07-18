import logging
import os

from discord.ext import commands
from httpx._exceptions import HTTPStatusError

from const import DC_ID, TOKEN_PATH
from tdaBot import TDABot

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class DCBot(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        print("start command ran")
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

        if not os.path.exists(TOKEN_PATH):
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

    @commands.command()
    async def bal(self, ctx):
        print("bal command ran")
        user = ctx.author
        if user.id == DC_ID:
            bal = await self.tda_client.get_bal()
            await user.send(f"Current Value: $ {bal}")
        else:
            await user.send("Unauthorized")

    @commands.command()
    async def bp(self, ctx):
        print("bp command ran")
        user = ctx.author
        if user.id == DC_ID:
            bp = await self.tda_client.get_bp()
            await user.send(f"Current Buying Power: $ {bp}")
        else:
            await user.send("Unauthorized")
