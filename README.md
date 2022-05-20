# YuGiOhCardBot



Notice: `u/_CX-MD_` has taken control of the account u/YuGiOhCardBot, the associated gmail, and the subreddit r/YuGiOhCardBot, and will be relaunching the bot. Please thank them and enjoy.



YuGiOhCardBot, a Reddit bot for Yu-Gi-Oh! card searches



Alright. So first, a little bit of drama. I made this bot because I was incredibly excited about Master Duel. I was having a lot of fun connecting with other players on Reddit and Discord. But more and more the community was upsetting me, and the more I tried to be involved, the more it seemed I was rejected. It really bothered me. I got some messages that were calling me this and that and saying that they could use my bot to track my IP and threats of violence and blah blah blah. I just got sick of it. So I pulled the bot offline and deleted all the code and posted a bit of a melodramatic thing on r/masterduel. I just wanna be done with the sub and the community at large and take a break from yugioh in general.

Well fine, that's all well and good, but maybe somebody would like to renew this bot and maintain it. So I checked my backups and pulled it out. I went through and commented all of the code so that people can find their way. I believe even someone with zero coding experience could get this running really easily. I myself never touched Python before this. Which shows, btw. The code is not good.

This bot was using Heroku.com for hosting. It required a paid tier to keep it alive and reliable and fast. The fees were largely why I pulled the bot instead of just forgetting about it.

I had been funding it with Patreon as well.

There are actually 3 separate programs that need to run for all the functionality. YGOCBC replies to comments, YGOCBS replies to submission text, and YGOCBchat replies to instant messages. I could not figure out any way for these things to run as one program. I don't think you can do that, honestly. I'd love to see it if I'm wrong.

Deploying to Heroku is relatively simple, but message me if you need help. I don't really remember the specifics, so I won't bother typing anything up about it just now.

The files for each of the 3 versions are mostly the same. From YGOCBC, Start.py is the only file with anything different in YGOCBS, and Start.py, Config.py, and requirements.txt are different in YGOCBchat.

The 3 Start.py files are spaced equally so that you can clearly see differences and navigate maintaining them all.

If you want to take over this bot and run it either on Heroku or set up a Raspberry Pi or something, please do so. I encourage it. I'd be happy to provide any guidance I can.

I would also be willing to transfer the u/YuGiOhCardBot account to someone, as well as the Gmail I made for it, reddit.yugiohcardbot@gmail.com, and r/YuGiOhCardBot.



I really loved making this bot. I learned a lot. But now I'm done with it.



You can contact me at:

Reddit: u/symmetricalboy

Discord: Gori#0001

Telegram: @GoriLovesYou



Below is the bot usage guide pulled off of the subreddit's wiki.

The bot is not currently live and does not work.



Yu-Gi-Oh! Card Bot Wiki



Hello Duelists!

I'd like to introduce you to u/YuGiOhCardBot, a Reddit bot for Yu-Gi-Oh! card searches!

u/YuGiOhCardBot will provide you links to card information.

It only responds to explicit requests. You can request it by putting your card name in curly brackets like so: {card name}

You can call for the bot anywhere in your post text and comments.

You can make multiple calls in one post/comment.

It can handle TCG, OCG, anime cards, Rush Duel cards... heck, you can even search with emoji.



Short mode

When you call the bot with single curly brackets like {card name}, it will respond with the card title as a link to the card image, and any links that are requested. Each sub has a default list of links it will return, but you can change the links it returns with flags.



Expanded mode

By using double curly brackets like {{card name}}, you'll get the full card text in a reply, as well as all the links available in the short mode.



Chat

Start a chat with u/YuGiOhCardBot!

The bot will happily respond to all your card searching needs in a DM, or you can add it to a group chat if you'd like.



Alternate syntax

The bot will respond to several different request formats.

Short mode

{card name}

[[card name]]

<<card name>>

((card name))

Expanded mode

{{card name}}

[[[card name]]]

<<<card name>>>

(((card name)))



Flags

Too many links? Not enough? You can specify which ones you want for the short replies by adding to your post any of the following flags:

ALL (returns all 9 providers)

DEF or default or defaults (adds the defaults for the sub you're on, which is useful for using with additional flags and adding a provider to the default list)

YGP or Yugipedia

KON or Konami

FAN or Fandom

PRO, YGOPro, or YGOProDeck

ORG, Yugiorg, or YGOrganization

PRI, Prices, or YugiohPrices

TCG or TCGPlayer

DL, DLM, DuelLinks, or DuelLinksMeta

MD, MDM, MasterDuel, or MasterDuelMeta

Not case sensitive.

The flags are for your entire post.

It will only return what you request. To keep the default links as well, add DEF.

Each flag needs to be in brackets by itself.

Expanded mode searches ignore flags and always return all links.

Valid search example:

{Ash Blossom}{dl}{yugipedia}{prices}



Default flags

Each subreddit has a default set of link flags. They are as follows:

r/yugioh: Yugipedia, Konami, and YugiohPrices

r/Yugioh101: Yugipedia and Konami

r/DuelLinks: Yugipedia, Konami, and DuelLinksMeta

r/masterduel: Yugipedia, Konami, and MasterDuelMeta

r/YuGiOhMasterDuel: Yugipedia, Konami, and MasterDuelMeta



Help

If you want the bot to explain itself briefly, post {HELP}.



Things that need work

For cards thar aren't in Master Duel or Duel Links, the bot will still generate links to where those cards should be located on MDM and DLM. It ideally check if the links are valid.

Typing in a request for NULL or typing a bunch of characters used for bot syntax do strange things. Fix that.

More OCG card names need to be hard-corrected.

The bot largely handles non-English requests, but it could use some touch-ups so that it explicitly is handling non-English well.

Code is hella redundant. It's like 2500 lines x3 and could probably reasonably be 1000 lines x1.

Plans were at one point in place to add card data specifically about Duel Links and Master Duel, such as card rarity and where to get the card. I had planned to skim information fro MDM/DLM to accomplish that.

I had wanted to use Reddit's Power-Up system to replace some of the emoji the bot uses with custom emoji symbols from the cards, such as attribute and property and star chips. Good luck if you wanna go down that road.



Credits

u/Nihilate created the OG, u/YugiohLinkBot, and I wouldn't have built this without that seed. Their code was largely unusable due to broken APIs, but some key elements were taken.

u/cris9696 for u/PlayStoreLinks__Bot, which was the framework that the entire thing is based on. Lot's of their code still lives in mine.

u/R31ent1ess suggested this existed, and they always deserve credit for that.

Dylan Singer, AKA Gori, GoriLovesYou, or u/symmetricalboy, is the sole author of this project.



Revision, modification, and redistribution

You are free to do as you please with this project, in any capacity. I politely request that you retain the above credits in some form so that project lineage can be retraced if one wishes.



I am finished with this project. There will be no further additions by me for the foreseeable future. 



All the best and Happy Dueling.


