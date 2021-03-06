import os

# TDA token path
DIRNAME = os.path.abspath(".")
TOKEN_PATH = os.path.join(DIRNAME, "userData", "token.pickle")

# If you supply these,  you won't be asked them in Discord in order to start listening
CLIENT_ID = os.environ['CLIENT_ID']
ACCT_ID = os.environ['ACCT_ID']
RED_URL = os.environ['RED_URL']

# Discord
# Discord Bot Secret Token. create at https://discord.com/developers/applications/
# you must give it the "Servers Members Intent" Permission under "Priviledged Gateway Intents" on the "Bot" page
DC_TOKEN = os.environ['DC_TOKEN']

# This is your discord user id, not your nickname
DC_ID = int(os.environ['DC_ID'])
# The ID of the channel you want to send the Fills to
CH_ID = int(os.environ['CH_ID'])
