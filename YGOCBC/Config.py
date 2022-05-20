"""
You need to edit this file for the bot to work.

Subreddits have been left but you can change them very easily just by typing the name in the list. Follow syntax.

User agent doesn't really matter, you can make it whatever you want.

Client ID and secret are connected to the Reddit PRAW API and are taken from an app you generate in the account that will be acting as the bot.
Set up the Reddit account that you want to be posting as the bot, and go to https://old.reddit.com/prefs/apps/ and create a new app.
You can fill in all the info with whatever you want, it doesn't actually matter much. Just copy the ID and Secret into here and you're good to go.
One note: if you want to edit the bot to use OAuth instead of your account info directly, set the redirect to the following and check the link to generate an OAuth token:
https://not-an-aardvark.github.io/reddit-oauth-helper/

usename and password are just the login info for your bot's Reddit account. You may prefer OAuth, but figure that out on your own.

You can change the logger name if you want, it doesn't appear publicly. It appears in the log files the bot generates.

maxAppsPerComment is how many individual card requests can be in one post before the bot doesn't make an attempt to deal with it. It's set to 100 but that's never been an issue
for any reason. The bot can actually handle (almost) any number of requests if you change that number. If its reply overflows a max Reddit comment length, it repeats the
requests it wasn't able to fit at the bottom of its comment and replies to itself. This of course means that if there is an insane number of requests and the repeat requests
don't fit, it's going to generate an invalidly long comment and do absolutely nothing. 100 is probably fine.

The closing formula is just appended to every comment. It's the bot's signature. Edit as you will. The links are missing, so drop in your own.
"""

import logging

subreddits = ["yugioh","Yugioh101","masterduel","DuelLinks","YuGiOhMasterDuel"]
user_agent = 'YuGiOhCardBot:1.0'
client_id = 'REPLACE_ME'
client_secret = 'REPLACE_ME'
username = 'REPLACE_ME'
password = "REPLACE_ME"

loggingLevel = logging.DEBUG
loggerName = "YuGiOhCardBot"

logFile = "bot.log"
botRunningFile = "./tmp/botRunning"

maxAppsPerComment = 100

closingFormula = '-----\n\n^*Bleep* ^*bloop.* ^*I* ^*am* ^*a* ^*bot.* ^| ^[About](REPLACE_ME) ^| ^[Feeback](REPLACE_ME)'
