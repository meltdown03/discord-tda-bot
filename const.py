import os

# TDA token path
DIRNAME = os.path.abspath(".")
TOKEN_PATH = os.path.join(DIRNAME, "userData", "token.pickle")

# Discord
# Discord Bot Secret Token. create at https://discord.com/developers/applications/
# you must give it the "Servers Members Intent" Permission under "Priviledged Gateway Intents" on the "Bot" page
DC_TOKEN = os.environ['DC_TOKEN']
# No quotes, this is your discord user id, not your nickname
DC_ID = int(os.environ['DC_ID'])
