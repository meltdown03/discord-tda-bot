import json
import os

import discord
import xmltodict
from discord import channel
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from const import CH_ID, TOKEN_PATH
from parsers import (orderCancelledFormatter, orderEntryRequestFormatter,
                     orderFillFormatter)
from tda.auth import client_from_token_file, easy_client
from tda.client import Client
from tda.streaming import StreamClient, UnexpectedResponseCode


class TDABot():

    def __init__(self, bot, cog, client_id, ref_url=None):
        self.bot = bot
        self.cog = cog
        self.client_id = client_id
        self.ref_url = ref_url

        if not os.access(TOKEN_PATH, 2):
            self.client = easy_client(self.client_id, self.ref_url, TOKEN_PATH,
                                      webdriver_func=lambda: webdriver.Chrome(
                                          ChromeDriverManager().install()),
                                      asyncio=True)
        else:
            self.client = client_from_token_file(
                TOKEN_PATH, self.client_id, asyncio=True)

    @property
    async def get_bp(self):
        accts = await self.client.get_accounts()
        acct_info = accts.json()
        bp = acct_info[0]['securitiesAccount']['projectedBalances']['availableFunds']
        return bp

    @property
    async def get_bal(self):
        accts = await self.client.get_accounts()
        acct_info = accts.json()
        bal = acct_info[0]['securitiesAccount']['currentBalances']['liquidationValue']
        return bal

    @property
    async def get_pos(self):
        pos = await self.client.get_accounts(fields=Client.Account.Fields.POSITIONS)
        pos_json = pos.json()
        msg = ""
        pl = 0
        for i in pos_json[0]['securitiesAccount']['positions']:
            if i['instrument']['assetType'] == 'EQUITY':
                msg += str(f"**{i['instrument']['symbol']}** shares x{i['longQuantity']}")
                msg += str(f" at ${i['averagePrice']:.2f}\n --> Liq. Value ${i['marketValue']:.2f}\
 Today's P/L: ${i['currentDayProfitLoss']:.2f}\n")
                pl += i['currentDayProfitLoss']
            elif i['instrument']['assetType'] == 'OPTION':
                msg += str(f"**{i['instrument']['description']}** x{i['longQuantity']}")
                msg += str(f" at ${i['averagePrice']:.2f}\n --> Liq. Value ${i['marketValue']:.2f}\
 Today's P/L: ${i['currentDayProfitLoss']:.2f}\n")
                pl += i['currentDayProfitLoss']
        msg += str(f"\n**Total Daily P/L: ${pl:.2f}**")
        return msg

    async def update_game(self):
        bp = await self.get_bp
        game = discord.Game(f"with ${bp}")
        print("updated status balance: $", bp)
        await self.bot.change_presence(activity=game)

    async def get_activity(self, msg):
        user = self.cog.get_bot_user
        channel = self.bot.get_channel(CH_ID)
        timestamp = msg['timestamp']
        for msg in msg['content']:
            msgType = msg['MESSAGE_TYPE']
            msgData = msg['MESSAGE_DATA']

            if msgData != "":
                parsedDict = xmltodict.parse(msgData)
                # optional debug info
#                rawJsonMSG = '```json\n' + \
#                    json.dumps(parsedDict, indent=2) + '\n```'
#                if len(rawJsonMSG) < 2000:
#                    await user.send(rawJsonMSG)
                msgToSend = ''

                if msgType == 'UROUT':
                    await self.update_game()
                    # msgToSend = orderCancelledFormatter(parsedDict, timestamp)
                    return
                elif msgType == 'OrderEntryRequest':
                    await self.update_game()
                    # msgToSend = orderEntryRequestFormatter(
                    #     parsedDict, timestamp)
                    return
                elif msgType == 'OrderFill':
                    await self.update_game()
                    msgToSend = orderFillFormatter(parsedDict, timestamp)
                else:
                    return
                await channel.send(msgToSend)

            elif msgData == "" and msgType == "SUBSCRIBED" and self.loginMsgSent == False:
                self.loginMsgSent = True
                await user.send(f":white_check_mark: TDA account activity streamer started for account id: {self.account_id}\n\
         (You can now close this DM.)")

    async def read_stream(self, user, account_id):
        self.loginMsgSent = False
        self.account_id = account_id
        try:
            stream_client = StreamClient(
                self.client, account_id=self.account_id)
            await stream_client.login()
            await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
            await stream_client.account_activity_sub()
            stream_client.add_account_activity_handler(self.get_activity)

            while True:
                await stream_client.handle_message()

        except UnexpectedResponseCode as e:
            await user.send(f":x: Login failed, error: {e} - RESTART BOT AND TRY AGAIN")

        finally:
            await self.client.close_async_session()
