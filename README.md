Set your discord bot secret key (get from https://discord.com/developers/applications/#####BOT_ID######/bot) 
as an evironment variable named "DC_TOKEN", and get your Discord user
ID by right-clicking on your name and click "Copy ID". Set it as "DC_ID"
Note: You can also use a .env file if running in a pipenv/venv.
Add the bot to your server (see Discord bot tutorial for more help with these steps)

You should have your TDA API's Client ID, Account Number, and Redirect URL handy as well. The bot will ask
for these in a DM. It will also open a webpage to login/authorize the app via the TDA website on the first
run.

I setup a pipenv to run it, so clone this to a folder of your choosing. CD into it, run `pipenv install`.
This will install all required libraries. Then you can start it by running `pipenv run python main.py`
