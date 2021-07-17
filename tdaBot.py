import logging
import json
import xmltodict
import os

from discord.errors import HTTPException
from tda.auth import client_from_token_file, easy_client
from tda.streaming import StreamClient, UnexpectedResponseCode
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from const import TOKEN_PATH
from parsers import orderFillFormatter, orderEntryRequestFormatter


logger = logging.getLogger('tda')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='tda.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class tdaBot():

  def __init__(self, bot, cog, client_id, ref_url=None):
    self.bot = bot
    self.cog = cog
    self.client_id = client_id
    self.ref_url = ref_url
    
    if not os.path.exists(TOKEN_PATH):
      self.client = easy_client(self.client_id, self.ref_url, TOKEN_PATH,
                         webdriver_func=lambda: webdriver.Chrome(ChromeDriverManager().install()),
                         asyncio=True)
    else:
      self.client = client_from_token_file(TOKEN_PATH, self.client_id, asyncio=True)
  
  async def get_account_info(self):
    acct = await self.client.get_accounts()
    return acct.json()

  async def get_bp(self):
    acct_info = await self.get_account_info()
    bp = acct_info[0]['securitiesAccount']['projectedBalances']['availableFunds']
    return bp

  async def get_bal(self):
    acct_info = await self.get_account_info()
    bal = acct_info[0]['securitiesAccount']['currentBalances']['liquidationValue']
    return bal

  async def get_orders(self, msg):
    user = self.cog.getUser
    await self.cog.updateGame()
    for msg in msg['content']:
      msgType = msg['MESSAGE_TYPE']
      msgData = msg['MESSAGE_DATA']

      if msgData:
        parsedDict = xmltodict.parse(msgData)
        rawJsonMSG = '```json\n' + json.dumps(parsedDict, indent=2) + '\n```'
        msgToSend = ''

        if msgType == 'OrderEntryRequest':
          # msgToSend = orderEntryRequestFormatter(parsedDict)
          return
        elif msgType == 'OrderFill':
          msgToSend = orderFillFormatter(parsedDict)
        else:
          return

        logger.info(f'Parsed Response JSON:\n{rawJsonMSG}')

        try:
          await user.send(msgToSend)
        except HTTPException as e:
          print(f'Discord HTTPException: {e}\nMsg Attempt: {msgToSend}')

  async def read_stream(self, user, account_id):
    try:
      stream_client = StreamClient(self.client, account_id=int(account_id))
      await stream_client.login()
      await user.send(f":white_check_mark: TDA account activity streamer started for account id: {account_id}\n\
         (You can now close this DM.)")
      await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
      await stream_client.account_activity_sub()
      stream_client.add_account_activity_handler(self.get_orders)
  
      while True:
        await stream_client.handle_message()
  
    except UnexpectedResponseCode as e:
      await user.send(f":x: Login failed, error: {e} - RESTART BOT AND TRY AGAIN")

    finally:
      await self.client.close_async_session()
