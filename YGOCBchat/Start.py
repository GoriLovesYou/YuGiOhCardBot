#This code has been thoroughly commented after it was finished, by an amateur, with the intent for an amateur to be able to follow along and use it.
#Line spacing in the document matches Start.py across all 3 versions for easy comaprison and editing.
#For any questions, contact Dylan Singer via:
#Reddit: /symmetricalboy
#Discord: Gori#0001
#Telegram: @GoriLovesYou



#Import requirements. Some may be unnecessary, I never cleaned it up...

import praw
import sys
import time
import os
import re
import pickle
import urllib
import html
import Config
import logging
import math
import misaka
import lxml
from misaka import Markdown, HtmlRenderer
from lxml.html import fromstring
import pyshorteners
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.parse
import websocket
from Reddit_ChatBot_Python import RedditAuthentication
from Reddit_ChatBot_Python import ChatBot

#random thing that didn't like being moved anywhere else.

s = pyshorteners.Shortener()

#Generates the log files.

def make_logger(logger_name, logfile, loggin_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(loggin_level)
    
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    
    fh = logging.FileHandler(logfile)
    fh.setLevel(loggin_level)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

#Copied code that kills the bot. I mostly removed this but I think it gets called somewhere...

def stopBot(delete_lockfile=True):
    logger.info("Shutting down")
    if os.path.isfile(Config.botRunningFile):
        logger.debug("Deleting lock file")
        os.remove(Config.botRunningFile)
    sys.exit(0)





















#This generates the reply. This is far and away the bulk of the code.
#This should probably be objectified and done entirely differently. It is redundant and bad.

def generate_reply(link_me_requests, link_me_requests_extended, resp):
    reply_body = ""

    #Takes the requests and makes a nice little passable list
    
    app_names = []
    for link_me_request in link_me_requests:
        requested_apps = link_me_request.split(",")
        for app_name in requested_apps:
            app_name = app_name.strip()
            if len(app_name) > 0 and len(app_name) <= 128:
                app_names.append(app_name) 
    app_names = {v.lower(): v for v in app_names}.values()

    app_names_extended = []
    for link_me_request_extended in link_me_requests_extended:
        requested_apps_extended = link_me_request_extended.split(",")
        for app_name_extended in requested_apps_extended:
            app_name_extended = app_name_extended.strip()
            if len(app_name_extended) > 0 and len(app_name_extended) <= 128:
                app_names_extended.append(app_name_extended) 
    app_names_extended = {v.lower(): v for v in app_names_extended}.values()

    #Legacy nonsense

    nOfRequestedApps = 0
    nOfFoundApps = 0
    
    #This section handles flags that limit which links a reply contains.
    #The defaults for each subreddit are hardcoded here.
    #Extended mode ignores the flags and always posts all.

    #Chat bot just uses one default link for brevity.

    ygocbFlags = 'ygp'










 
    #Collect and apply user selected flags
 
    flagHolder = ""
    
    for app_name in app_names:
        app_name = html.unescape(app_name)
        app_name = app_name.lower()
                
        if app_name.lower() == 'none' or app_name.lower() == 'def' or app_name.lower() == 'default' or app_name.lower() == 'defaults' or app_name.lower() == 'fan' or app_name.lower() == 'fandom' or app_name.lower() == 'delete' or app_name.lower() == 'help' or app_name.lower() == 'all' or app_name.lower() == 'ygp' or app_name.lower() == 'yugipedia' or app_name.lower() == 'kon' or app_name.lower() == 'konami' or app_name.lower() == 'pro' or app_name.lower() == 'ygopro' or app_name.lower() == 'ygoprodeck' or app_name.lower() == 'org' or app_name.lower() == 'yugiorg' or app_name.lower() == 'yugiorganization' or app_name.lower() == 'pri' or app_name.lower() == 'prices' or app_name.lower() == 'yugiohprices' or app_name.lower() == 'tcg' or app_name.lower() == 'tcgplayer' or app_name.lower() == 'dl' or app_name.lower() == 'dlm' or app_name.lower() == 'duellinks' or app_name.lower() == 'duellinksmeta' or app_name.lower() == 'md' or app_name.lower() == 'mdm' or app_name.lower() == 'masterduel' or app_name.lower() == 'masterduelmeta':
            flagHolder += app_name.lower()       
            flagHolder += ','
 
    for app_name in app_names_extended:
        app_name = html.unescape(app_name)
        app_name = app_name.lower()
                
        if app_name.lower() == 'none' or app_name.lower() == 'def' or app_name.lower() == 'default' or app_name.lower() == 'defaults' or app_name.lower() == 'fan' or app_name.lower() == 'fandom' or app_name.lower() == 'delete' or app_name.lower() == 'help' or app_name.lower() == 'all' or app_name.lower() == 'ygp' or app_name.lower() == 'yugipedia' or app_name.lower() == 'kon' or app_name.lower() == 'konami' or app_name.lower() == 'pro' or app_name.lower() == 'ygopro' or app_name.lower() == 'ygoprodeck' or app_name.lower() == 'org' or app_name.lower() == 'yugiorg' or app_name.lower() == 'yugiorganization' or app_name.lower() == 'pri' or app_name.lower() == 'prices' or app_name.lower() == 'yugiohprices' or app_name.lower() == 'tcg' or app_name.lower() == 'tcgplayer' or app_name.lower() == 'dl' or app_name.lower() == 'dlm' or app_name.lower() == 'duellinks' or app_name.lower() == 'duellinksmeta' or app_name.lower() == 'md' or app_name.lower() == 'mdm' or app_name.lower() == 'masterduel' or app_name.lower() == 'masterduelmeta':
            flagHolder += app_name.lower()       
            flagHolder += ','
 
    if flagHolder != "":
        if re.search('def', flagHolder):
            ygocbFlags += ','
            ygocbFlags += flagHolder
        if not re.search('def', flagHolder):
            ygocbFlags = flagHolder

    if flagHolder != "":
        if re.search('none', flagHolder):
            ygocbFlags = ""

    #Start looping through extended mode requests

    for app_name in app_names_extended:
    
        app_name = app_name.lower()
            
        #Hardcoded corrections
        #The bot didn't like a bunch of searches so I manually made adjustments.
        #This contains common abbreviations as well as jokes and puns.
        #Mostly, Google handles all the corrections, but some things just didn't work.      
        
        if re.search('-', app_name):
            app_name = re.sub('-', ' ', app_name)
            
        if re.search('rongo', app_name):
            app_name = re.sub('rongo', 'rhongo', app_name)

        if app_name.lower() == "simorgh":
            app_name = "Simorgh, Bird of Sovereignty"

        if app_name.lower() == "dad":
            app_name = "Dark Armed Dragon"

        if app_name.lower() == "rebd":
            app_name = "Red-Eyes Black Dragon"

        if app_name.lower() == "rml":
            app_name = "Royal Magical Library"

        if app_name.lower() == "drnm":
            app_name = "Dark Ruler No More"

        if app_name.lower() == "dm":
            app_name = "Dark Magician"

        if app_name.lower() == "brick":
            app_name = "Blue-Eyes White Dragon"

        if app_name.lower() == "kaiba":
            app_name = "Blue-Eyes White Dragon"

        if app_name.lower() == "yugi":
            app_name = "Dark Magician"

        if app_name.lower() == "joey":
            app_name = "Red-Eyes Black Dragon"
            
        if re.search("seto kaiba", app_name):
            app_name = "Blue-Eyes White Dragon"

        if re.search("yugi muto", app_name):
            app_name = "Dark Magician"

        if re.search("joey wheeler", app_name):
            app_name = "Red-Eyes Black Dragon"

        if app_name.lower() == "bls":
            app_name = "Black Luster Soldier"

        if app_name.lower() == "no fun allowed":
            app_name = "Solemn Judgement"

        if app_name.lower() == "very fun dragon":
            app_name = "True King of All Calamities"

        if app_name.lower() == "dn":
            app_name = "Dogmatika Nexus"

        if re.search("narval", app_name):
            app_name = re.sub("narval", "nervall", app_name)

        if app_name.lower() == "black lotus":
            app_name = "samsara lotus"

        if app_name.lower() == "goat":
            app_name = "Scapegoat"

        if app_name.lower() == "dragon":
            app_name = "chamber dragonmaid"

        if app_name.lower() == "dark magician pandora":
            app_name = "dark magician arkana"

        if re.search("numeronius", app_name):
            app_name = re.sub("numeronius", "numerounius", app_name)
            
        if app_name.lower() == "numerounius":
            app_name = "Number C1000: Numerounius"

        if app_name.lower() == "barian 1":
            app_name = "Number 1: Infection Buzz King"

        if app_name.lower() == "barian number 1":
            app_name = "Number 1: Infection Buzz King"
            
        if app_name.lower() == "barian 2":
            app_name = "Number 2: Ninja Shadow Mosquito"
            
        if app_name.lower() == "barian number 2":
            app_name = "Number 2: Ninja Shadow Mosquito"

        if app_name.lower() == "barian 3":
            app_name = "Number 3: Cicada King"

        if app_name.lower() == "barian number 3":
            app_name = "Number 3: Cicada King"

        if app_name.lower() == "barian 4":
            app_name = "Number 4: Stealth Kragen"

        if app_name.lower() == "barian number 4":
            app_name = "Number 4: Stealth Kragen"

        if app_name.lower() == "barian 10":
            app_name = "Number 10: Dark Illumiknight"

        if app_name.lower() == "barian number 10":
            app_name = "Number 10: Dark Illumiknight"

        if app_name.lower() == "c":
            app_name = "Maxx C"

        if app_name.lower() == "d":
            app_name = "Batteryman D"

        if app_name.lower() == "cybernetic horizon":
            app_name = "cybernetic horizon card"

        if app_name.lower() == "duelist alliance":
            app_name = "duelist alliance card"

        if app_name.lower() == "wight":
            app_name = "skull servant"

        if app_name.lower() == "skull archfiend":
            app_name = "summoned skull"

        if app_name.lower() == "critter":
            app_name = "sangan"            

        if app_name.lower() == "cyclone":
            app_name = "mystical space typhoon"

        if app_name.lower() == "gust of wind":
            app_name = "mystical wind typhoon"

        if app_name.lower() == "hurricane":
            app_name = "giant trunade"

        if app_name.lower() == "wyvern":
            app_name = "Winged Dragon, Guardian of the Fortress #2"

        if app_name.lower() == "chaos pod":
            app_name = "morphing jar 2"

        if app_name.lower() == "rda":
            app_name = "red dragon archfiend"

        if app_name.lower() == "hrda":
            app_name = "hot red dragon archfiend"

        if app_name.lower() == "hot rda":
            app_name = "hot red dragon archfiend"

        if app_name.lower() == "pugm":
            app_name = "perfectly ultimate great moth"

        if app_name.lower() == "gepd":
            app_name = "Galaxy-Eyes Photon Dragon"

        if app_name.lower() == "gedd":
            app_name = "Googly-Eyes Drum Dragon"

        if app_name.lower() == "chaos soldier":
            app_name = "black luster soldier"

        if app_name.lower() == "xyz":
            app_name = "xyz dragon dark rebellion"
 
        if app_name.lower() == "xyz dragon":
            app_name = "xyz dragon dark rebellion"

        if app_name.lower() == "golden sphere":
            app_name = "sphere mode"

        if app_name.lower() == "mobc":
            app_name = "magician of black chaos"        

        if app_name.lower() == "ladd":
            app_name = "Light and Darkness Dragon"

        if app_name.lower() == "exodia":
            app_name = "exodia the forbidden one"

        if app_name.lower() == "ced":
            app_name = "Chaos Emperor Dragon Envoy of the End"

        if re.search("waifu", app_name):
            app_name = "Waifujokething"

        if re.search("go brrr", app_name):
            app_name = re.sub("go brrr", "", app_name)
            
        if re.search("goes brrr", app_name):
            app_name = re.sub("goes brrr", "", app_name)
            
        if re.search("screw the rules", app_name):
            app_name = "Abridged"

        if app_name.lower() == "etele":
            app_name = "Emergency Teleport"

        if re.search("yugi boy", app_name):
            app_name = "Abridged"
            
        if re.search("attention duelists", app_name):
            app_name = "Abridged"
        
        if app_name.lower() == "@ignister":
            app_name = "Achichi @Ignister"
            
        if app_name.lower() == "laugh":
            app_name = "charisma token"

        if app_name.lower() == "charisma":
            app_name = "charisma token"

        #If the flags make sense, let's do some Googling and link building.
        
        if app_name.lower() != 'none' and app_name.lower() != 'def' and app_name.lower() != 'default' and app_name.lower() != 'defaults' and app_name.lower() != 'fan' and app_name.lower() != 'fandom' and app_name.lower() != 'delete' and app_name.lower() != 'help' and app_name.lower() != 'all' and app_name.lower() != 'ygp' and app_name.lower() != 'yugipedia' and app_name.lower() != 'kon' and app_name.lower() != 'konami' and app_name.lower() != 'pro' and app_name.lower() != 'ygopro' and app_name.lower() != 'ygoprodeck' and app_name.lower() != 'org' and app_name.lower() != 'yugiorg' and app_name.lower() != 'yugiorganization' and app_name.lower() != 'pri' and app_name.lower() != 'prices' and app_name.lower() != 'yugiohprices' and app_name.lower() != 'tcg' and app_name.lower() != 'tcgplayer' and app_name.lower() != 'dl' and app_name.lower() != 'dlm' and app_name.lower() != 'duellinks' and app_name.lower() != 'duellinksmeta' and app_name.lower() != 'md' and app_name.lower() != 'mdm' and app_name.lower() != 'masterduel' and app_name.lower() != 'masterduelmeta':
 
            nOfRequestedApps += 1
            
            singleCard = ""
            
            #fallback if the search fails
            
            konami_code = "0000"

            #check that the comment isn't getting too long as we loop through.
            
            if len(reply_body) < 8000:
                
                #Google it, with yugipedia added
                
                query_1 = ('{} "yugipedia"'.format(app_name))
                link_long_1 = "https://yugipedia.com/wiki/"
                for j in search(query_1, tld="com", lang="en", num=1, stop=1, pause=2):
                    link_long_1 = j

                #If the first link is a Yugipedia page, get the Konami Card Database number.
                #If that page is an Anime card, set the code to anime
                
                if re.search("yugipedia", link_long_1):
                    
                    yppage = requests.get(link_long_1)
                    soup = BeautifulSoup(yppage.content, "html.parser")
                    ypdump = soup.get_text()
                    konami_code = '0000'
                    if re.search("Yugioh-Card database #[0-9]+", ypdump):
                        konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                        konami_code = konami_code.group()
                        konami_code = str(konami_code)
                        konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                    else:
                        footerdump = soup.find_all("div", {"class": "below hlist"})
                        footerdump = str(footerdump)
                        if re.search("Anime cards", footerdump):
                            konami_code = "Anime"

                #If the search failed, try again and check the next link. Rinse, repeat.

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=2, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=3, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=4, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                #If it doesn't take one of the first 4 hits on Google,
                #Try removing tcgplayer and wikipedia.
                #Check if someone is joking and it's a different card game.

                if konami_code == '0000':
                    query_1 = ('{} -tcgplayer -wikipedia'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=1, pause=2):
                        link_long_1 = j            

                    if re.search("wizards", link_long_1) or re.search("cardkingdom", link_long_1):
                        app_name = "Magic: The Gathering"
                        ygocbFlags = ""
                        konami_code = "9999"
                    if re.search("pokémon", link_long_1) or re.search("pokemon", link_long_1) or re.search("bulbapedia", link_long_1):
                        app_name = "Pokémon"
                        ygocbFlags = ""   
                        konami_code = "9999"
                    if re.search("digimon", link_long_1) or re.search("wikimon", link_long_1):
                        app_name = "Digimon"
                        ygocbFlags = ""
                        konami_code = "9999"

                #If we got a match, fetch the clean card title

                if konami_code != '0000' and konami_code != '9999':
                    titledump = soup.find_all("h1", {"class": "firstHeading"})
                    titledump = str(titledump)
                    titledump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", titledump)
                    titledump = re.sub("<>", "", titledump)
                    titledump = re.sub("\[", "", titledump)
                    titledump = re.sub("\]", "", titledump)
                    titledump = re.sub(" ", "_", titledump)
                    link_long_1 = "https://yugipedia.com/wiki/"+titledump

                    link_long_1 = html.unescape(link_long_1)

                #If the link isn't Yugipedia, fallback
                
                if link_long_1 == "https://yugipedia.com/wiki/":
                    konami_code = '0000'

                #If we've got an anime-only card, we start fetching data

                if konami_code == "Anime":
                    yppage = requests.get(link_long_1)
                    soup = BeautifulSoup(yppage.content, "html.parser")
                    
                    #Get the card text
                    
                    loredump = ""
                    loredump = soup.find_all("div", {"class": "lorebox-lore"})                  
                    carddata_text = str(loredump)                                   
                    carddata_text = re.sub("<br/>", " ", carddata_text)
                    carddata_text = re.sub("</dd>", " ", carddata_text)
                    carddata_text = re.sub("</dt>", " ", carddata_text)
                    carddata_text = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", carddata_text)
                    carddata_text = re.sub("<>", "", carddata_text)
                    carddata_text = "::"+carddata_text+"::"
                    carddata_text = re.sub("::\[", "", carddata_text)
                    carddata_text = re.sub("\]::", "", carddata_text)

                    #Get the card image. Try a couple spots.

                    imagedump = ""
                    imagedump2 = ""
                    imagedump = soup.find_all("div", {"class": "cardtable-main_image-wrapper"})
                    imagedump = str(imagedump)
                    imagedump2 = imagedump
                    if re.search("300px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/300px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    elif re.search("200px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/200px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    else:
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//)([^hg]*)(?=png(?!g))'
                        imagedump = re.search(imageregex, imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump+"png"

                    #Fetch card info, try to clean it up.
                    
                    columndump = ""                    
                    
                    columndump = soup.find_all("div", {"class": "card-table-columns"})
                    columndump = str(columndump)
                    columndump = re.sub("<br/>", ":", columndump)
                    columndump = re.sub("</th>", ":", columndump)
                    columndump = re.sub("</td>", ":", columndump)
                    columndump = re.sub("</tr>", ":", columndump)
                    columndump = re.sub("</dd>", ":", columndump)                    
                    columndump = re.sub("</dt>", ":", columndump)
                    columndump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", columndump)
                    columndump = re.sub("<>", "", columndump)
                    columndump = re.sub("\[", "", columndump)
                    columndump = re.sub("\]", "", columndump)
                    columndump = re.sub("[:]+", ":", columndump)
                    columndump = re.findall("^.*", columndump, re.M)
                    columndump = str(columndump)
                    columndump = re.sub("'", "", columndump)
                    columndump = re.sub('"', "", columndump)
                    columndump = re.sub(",", "", columndump)
                    columndump = re.sub("[ ]+", " ", columndump)
                    columndump = re.sub(" :", ":", columndump)
                    columndump = re.sub(": ", ":", columndump)
                    columndump = re.sub("\[ ", ":", columndump)

                    boxdump = soup.find_all("div", {"class": "lorebox lorebox--main"})
                    boxdump = str(boxdump)
                    
                    carddata_type = ""
                    carddata_types = ""
                    if re.search("card-table-types", boxdump):
                        carddata_type = "Monster"
                        carddata_types = soup.find_all("div", {"class": "hlist hslash card-table-types"})
                        carddata_types = str(carddata_types)
                        carddata_types = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", carddata_types)
                        carddata_types = re.sub("<>", "", carddata_types)
                        carddata_types = re.sub("\[", "", carddata_types)
                        carddata_types = re.sub("\]", "", carddata_types)

                    #We've got a Monster card.
                    #Set what type of Monster it is.

                    if carddata_type == "Monster":
                        if re.search("Pendulum", carddata_types):
                            if re.search("Link", carddata_types):
                                carddata_type = "Pendulum Link Monster 🟦🟩"
                            elif re.search("Xyz", carddata_types):
                                carddata_type = "Pendulum Xyz Monster ⬛🟩"
                            elif re.search("Synchro", carddata_types):
                                carddata_type = "Pendulum Synchro Monster ⬜🟩"
                            elif re.search("Fusion", carddata_types):
                                carddata_type = "Pendulum Fusion Monster 🟪🟩"
                            elif re.search("Ritual", carddata_types):
                                carddata_type = "Pendulum Ritual Monster 🟦🟩"
                            elif re.search("Effect", carddata_types):
                                carddata_type = "Pendulum Effect Monster 🟧🟩"
                            else:
                                carddata_type = "Pendulum Normal Monster 🟨🟩"
                        elif re.search("Link", carddata_types):
                            carddata_type = "Link Monster 🟦"
                        elif re.search("Xyz", carddata_types):
                            carddata_type = "Xyz Monster ⬛"
                        elif re.search("Synchro", carddata_types):
                            carddata_type = "Synchro Monster ⬜"
                        elif re.search("Fusion", carddata_types):
                            carddata_type = "Fusion Monster 🟪"
                        elif re.search("Ritual", carddata_types):
                            carddata_type = "Ritual Monster 🟦"
                        elif re.search("Effect", carddata_types):
                            carddata_type = "Effect Monster 🟧"
                        else:
                            carddata_type = "Normal Monster 🟨"
                            
                    if re.search(":Card type:", columndump): 

                        carddata_type = re.search('(?<=(?<!:):Card type:)([^::]*)(?=:(?!:))', columndump)
                        carddata_type = carddata_type.group()
                        carddata_type = str(carddata_type) 

                    #Set the card type for a spell

                    if carddata_type == "Spell":
                        carddata_type = "Spell 🟩"

                    #It's a trap!

                    if carddata_type == "Trap":
                        carddata_type = "Trap 🟪"

                    #Collect properties for spell/trap cards

                    carddata_property = ""
                    if re.search(":Property:", columndump): 

                        carddata_property = re.search('(?<=(?<!:):Property:)([^::]*)(?=:(?!:))', columndump)
                        carddata_property = carddata_property.group()
                        carddata_property = str(carddata_property) 
            
                    #Collect Anime appearances (episodes)
            
                    carddata_appearances = ""
                    if re.search(":Appearances:", columndump): 
                        print(columndump)
                        columndump = re.sub(":Appearances:", "%", columndump)
                        columndump = re.sub(":Links:", "%", columndump)
                        columndump = re.sub("\:\]", "%", columndump)
                        carddata_appearances = re.search('(?<=(?<!%)%)([^%%]*)(?=%(?!%))', columndump)
                        carddata_appearances = carddata_appearances.group()
                        carddata_appearances = str(carddata_appearances)                     
   
                    #Get Pendulum Monster data
   
                    carddata_pendulumeffect = ""
                    carddata_scale = ""
                    if re.search("Pendulum", carddata_type):
                        pedump = soup.find_all("div", {"class": "lorebox-lore lorebox-lore--pendulum"})                  
                        carddata_pendulumeffect = str(pedump)                                   
                        carddata_pendulumeffect = re.sub("<br/>", "\n\n", carddata_pendulumeffect)
                        carddata_pendulumeffect = re.sub("</dd>", "\n\n", carddata_pendulumeffect)
                        carddata_pendulumeffect = re.sub("</dt>", "\n\n", carddata_pendulumeffect)
                        carddata_pendulumeffect = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", carddata_pendulumeffect)
                        carddata_pendulumeffect = re.sub("<>", "", carddata_pendulumeffect)
                        carddata_pendulumeffect = "::"+carddata_pendulumeffect+"::"
                        carddata_pendulumeffect = re.sub("::\[", "", carddata_pendulumeffect)
                        carddata_pendulumeffect = re.sub("\]::", "", carddata_pendulumeffect)
                        scaledump = soup.find_all("div", {"class": "lorebox-pendulum_scale nomobile"})
                        carddata_scale = str(scaledump)
                        carddata_scale = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", carddata_scale)
                        carddata_scale = re.sub("<>", "", carddata_scale)
                        carddata_scale = re.sub("\[", "", carddata_scale)
                        carddata_scale = re.sub("\]", "", carddata_scale)
                        carddata_scale = "◀🟦 "+carddata_scale+" 🟥▶"

                    #Attempt to clean up raw data

                    boxdump = re.sub("<br/>", ":", boxdump)
                    boxdump = re.sub("</th>", ":", boxdump)
                    boxdump = re.sub("</td>", ":", boxdump)
                    boxdump = re.sub("</tr>", ":", boxdump)
                    boxdump = re.sub("</dd>", ":", boxdump)                    
                    boxdump = re.sub("</dt>", ":", boxdump)
                    boxdump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", boxdump)
                    boxdump = re.sub("<>", "", boxdump)
                    boxdump = re.sub("\[", "", boxdump)
                    boxdump = re.sub("\]", "", boxdump)
                    boxdump = re.sub("[:]+", ":", boxdump)
                    boxdump = re.findall("^.*", boxdump, re.M)
                    boxdump = str(boxdump)
                    boxdump = re.sub("'", "", boxdump)
                    boxdump = re.sub(",", "", boxdump)
                    boxdump = re.sub("[ ]+", " ", boxdump)
                    boxdump = re.sub(" :", ":", boxdump)
                    boxdump = re.sub(": ", ":", boxdump)
                    boxdump = re.sub("\[ ", ":", boxdump)                    
                      
                    #Get and set all the card values

                    carddata_atk = ""
                    if re.search("ATK / ", boxdump):
                        carddata_atk = re.search('(?<=(?<!A)ATK / )([^A ]*)(?= (?! ))', boxdump)
                        carddata_atk = carddata_atk.group()
                        carddata_atk = str(carddata_atk)

                    carddata_def = ""
                    if re.search("DEF / ", boxdump):
                        carddata_def = re.search('(?<=(?<!D)DEF / )([^D ]*)(?= (?! ))', boxdump)
                        carddata_def = carddata_def.group()
                        carddata_def = str(carddata_def)

                    carddata_link = ""
                    if re.search("LINK – ", boxdump):
                        carddata_link = re.search('(?<=(?<!L)LINK – )([^L ]*)(?= (?! ))', boxdump)
                        carddata_link = carddata_link.group()
                        carddata_link = str(carddata_link)

                    carddata_level = ""
                    if re.search(":Level:", columndump):
                        carddata_level = re.search('(?<=(?<!:):Level:)([^::]*)(?=:(?!:))', columndump)
                        carddata_level = carddata_level.group()
                        carddata_level = str(carddata_level)
                        if len(carddata_level) > 0 and len(carddata_level) <= 2:
                            carddata_level = int(carddata_level)
                        else:
                            konami_code = "0000"
                        carddata_starchips = "  ✪" * carddata_level
                    
                    carddata_rank = ""
                    if re.search(":Rank:", columndump):
                        carddata_rank = re.search('(?<=(?<!:):Rank:)([^::]*)(?=:(?!:))', columndump)
                        carddata_rank = carddata_rank.group()
                        carddata_rank = str(carddata_rank)
                        if len(carddata_rank) > 0 and len(carddata_rank) <= 2:
                            carddata_rank = int(carddata_rank)
                        else:
                            konami_code = "0000"
                        carddata_starchips = "  ⍟" * carddata_rank

                    carddata_arrows = ""
                    if re.search(":Link Arrows:", columndump): 

                        carddata_arrows = re.search('(?<=(?<!:):Link Arrows:)([^::]*)(?=:(?!:))', columndump)
                        carddata_arrows = carddata_arrows.group()
                        carddata_arrows = str(carddata_arrows)
                        carddata_arrow_symbol_builder = ""
                        if re.search("Top-Left", carddata_arrows):
                            carddata_arrow_symbol_builder += "↖️ "
                        if re.search("Top-Center", carddata_arrows):
                            carddata_arrow_symbol_builder += "⬆️ "
                        if re.search("Top-Right", carddata_arrows):
                            carddata_arrow_symbol_builder += "↗️ "
                        if re.search("Middle-Left", carddata_arrows):
                            carddata_arrow_symbol_builder += "⬅️ "
                        if re.search("Middle-Right", carddata_arrows):
                            carddata_arrow_symbol_builder += "➡️ "
                        if re.search("Bottom-Left", carddata_arrows):
                            carddata_arrow_symbol_builder += "↙️ "
                        if re.search("Bottom-Center", carddata_arrows):
                            carddata_arrow_symbol_builder += "⬇️ "
                        if re.search("Bottom-Right", carddata_arrows):
                            carddata_arrow_symbol_builder += "↘️ "
                        carddata_arrows = carddata_arrow_symbol_builder
                    
                    carddata_attribute = ""
                    if re.search(":Attribute:", columndump): 

                        carddata_attribute = re.search('(?<=(?<!:):Attribute:)([^::]*)(?=:(?!:))', columndump)
                        carddata_attribute = carddata_attribute.group()
                        carddata_attribute = str(carddata_attribute)                        
                            
                        if carddata_attribute == "FIRE":
                            carddata_attribute += " 🔴"
                        if carddata_attribute == "LIGHT":
                            carddata_attribute += " 🟡"
                        if carddata_attribute == "WIND":
                            carddata_attribute += " 🟢"
                        if carddata_attribute == "WATER":
                            carddata_attribute += " 🔵"
                        if carddata_attribute == "DARK":
                            carddata_attribute += " 🟣"
                        if carddata_attribute == "EARTH":
                            carddata_attribute += " 🟤"
                        if carddata_attribute == "DIVINE":
                            carddata_attribute += " ⚪"
                        if carddata_attribute == "LAUGH":
                            carddata_attribute += " 🟠"
        
                    #I like emoji
        
                    carddata_types = re.sub("Aqua", "Aqua 💧", carddata_types)
                    carddata_types = re.sub("Beast", "Beast 🐗", carddata_types)
                    carddata_types = re.sub("Creator God", "Creator God 🌅", carddata_types)
                    carddata_types = re.sub("Cyberse", "Cyberse 🤖", carddata_types)
                    carddata_types = re.sub("Dinosaur", "Dinosaur 🦖", carddata_types)
                    carddata_types = re.sub("Divine-Beast 🐗", "Divine-Beast 📿", carddata_types)
                    carddata_types = re.sub("Dragon", "Dragon 🐉", carddata_types)
                    carddata_types = re.sub("Fairy", "Fairy 🧚", carddata_types)
                    carddata_types = re.sub("Fiend", "Fiend 👿", carddata_types)
                    carddata_types = re.sub("Fish", "Fish 🐟", carddata_types)
                    carddata_types = re.sub("Insect", "Insect 🪲", carddata_types)
                    carddata_types = re.sub("Machine", "Machine ⚙️", carddata_types)
                    carddata_types = re.sub("Plant", "Plant 🌱", carddata_types)
                    carddata_types = re.sub("Psychic", "Psychic 🧠", carddata_types)
                    carddata_types = re.sub("Pyro", "Pyro 🔥", carddata_types)
                    carddata_types = re.sub("Reptile", "Reptile 🦎", carddata_types)
                    carddata_types = re.sub("Rock", "Rock 🪨", carddata_types)
                    carddata_types = re.sub("Sea Serpent", "Sea Serpent 🐍", carddata_types)
                    carddata_types = re.sub("Spellcaster", "Spellcaster 🧙", carddata_types)
                    carddata_types = re.sub("Thunder", "Thunder 🌩️", carddata_types)
                    carddata_types = re.sub("Warrior", "Warrior ⚔️", carddata_types)
                    carddata_types = re.sub("Winged Beast 🐗", "Winged Beast 🦅", carddata_types)
                    carddata_types = re.sub("Wyrm", "Wyrm 🪱", carddata_types)
                    carddata_types = re.sub("Zombie", "Zombie 🧟", carddata_types)
                    carddata_types = re.sub("Pendulum", "Pendulum 🧬", carddata_types)
                    carddata_types = re.sub("Link", "Link 🔗", carddata_types)
                    carddata_types = re.sub("Xyz", "Xyz ☄️", carddata_types)
                    carddata_types = re.sub("Synchro", "Synchro 💫", carddata_types)
                    carddata_types = re.sub("Fusion", "Fusion 🌀", carddata_types)
                    carddata_types = re.sub("Ritual", "Ritual 🕯️", carddata_types)
                    carddata_types = re.sub("Effect", "Effect ⏩", carddata_types)
                    carddata_types = re.sub("Normal", "Normal ⏺️", carddata_types)
                    carddata_types = re.sub("Tuner", "Tuner 🧲", carddata_types)
                    carddata_types = re.sub("Gemini", "Gemini ♊", carddata_types)
                    carddata_types = re.sub("Flip", "Flip ↪️", carddata_types)
                    carddata_types = re.sub("Token", "Token 🎲", carddata_types)
                    carddata_types = re.sub("Toon", "Toon 🤪", carddata_types)
                    carddata_types = re.sub("Union", "Union 🫂", carddata_types)
                    carddata_types = re.sub("Spirit", "Spirit 👻", carddata_types)
                    carddata_types = re.sub("Maximum", "Maximum 💥", carddata_types)
                    carddata_types = re.sub("Beast 🐗-Warrior ⚔️", "Beast-Warrior 👹", carddata_types)
                    carddata_types = re.sub("Celestial Warrior ⚔️", "Celestial Warrior 🌠", carddata_types)
                    carddata_types = re.sub("Cyborg", "Cyborg 🧑‍🚀", carddata_types)
                    carddata_types = re.sub("High Dragon 🐉", "High Dragon 🏺", carddata_types)
                    carddata_types = re.sub("Magical Knight", "Magical Knight 🧝", carddata_types)
                    carddata_types = re.sub("Omega Psychic 🧠", "Omega Psychic 🧿", carddata_types)
                    carddata_types = re.sub("Galaxy", "Galaxy 🌌", carddata_types)
                    carddata_types = re.sub("Charisma", "Charisma 💋", carddata_types)
                    carddata_types = re.sub("Human", "Human 🧑", carddata_types)
                    carddata_types = re.sub("Business", "Business 💼", carddata_types)
                    carddata_types = re.sub("Newspaper", "Newspaper 📰", carddata_types)
                    carddata_types = re.sub("Swindler", "Swindler 🦹", carddata_types)
                    carddata_types = re.sub("Son", "Son 👦", carddata_types)
                    carddata_types = re.sub("Swirly", "Swirly 😵‍💫", carddata_types)
                    carddata_types = re.sub("Immortal", "Immortal 🧛", carddata_types)
                    carddata_types = re.sub("Yokai", "Yokai 🪀", carddata_types)
                    carddata_types = re.sub("Black Magic", "Black Magic 🔮", carddata_types)
                    carddata_types = re.sub("White Magic", "White Magic 🪄", carddata_types)
                    carddata_types = re.sub("Sea Beast 🐗", "Sea Beast 🧜‍", carddata_types)
                    carddata_types = re.sub("Illusion Magic", "Illusion Magic 🪞", carddata_types)
                    carddata_types = re.sub("Dragon 🐉 Magic", "Dragon Magic 🏮", carddata_types)
                     
                    carddata_property = re.sub("Normal", "Normal ⏺️", carddata_property)
                    carddata_property = re.sub("Continuous", "Continuous ♾️", carddata_property)
                    carddata_property = re.sub("Ritual", "Ritual 🕯️", carddata_property)
                    carddata_property = re.sub("Quick-Play", "Quick-Play ⚡", carddata_property)
                    carddata_property = re.sub("Field", "Field ✧", carddata_property)
                    carddata_property = re.sub("Equip", "Equip ➕", carddata_property)                                 
                    
                    carddata_property = re.sub("Counter", "Counter ↩️", carddata_property)
                    
                    carddata_type = "Anime Only "+carddata_type

                    #Organize the data into the actual reply format.
                    #This section is TOTALLY DIFFERENT in the chat bot.
                    #Chat bot builds the reply and starts sending messages directly from here.
                                        
                    prettyName = html.unescape(re.sub(r'https://yugipedia.com/wiki/', '', re.sub(r'_', ' ', link_long_1)))
                    
                    prettyName = urllib.parse.unquote(prettyName)                    
                     
                    chatbot.send_message(prettyName, resp.channel_url)
                    time.sleep(1)
                    
                    chatbot.send_message("Image: "+carddata_image, resp.channel_url)
                    time.sleep(1)
                    
                    if re.search("Monster", carddata_type):
                        chatbot.send_message("Card type: {}".format(carddata_type), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Attribute: {}".format(carddata_attribute), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Monster type: {}".format(carddata_types), resp.channel_url)
                        time.sleep(1)
                        if re.search("Link", carddata_type):
                            chatbot.send_message("Link arrows: {}".format(carddata_arrows), resp.channel_url)
                            time.sleep(1)
                        elif re.search("Xyz", carddata_type):
                            chatbot.send_message("Rank: {} {}".format(carddata_rank, carddata_starchips), resp.channel_url)
                            time.sleep(1)
                        else:
                            chatbot.send_message("Level: {} {}".format(carddata_level, carddata_starchips), resp.channel_url)
                            time.sleep(1)
                        if re.search("Pendulum", carddata_type):
                            chatbot.send_message("Pendulum scale: {}".format(carddata_scale), resp.channel_url)
                            time.sleep(1)
                        chatbot.send_message("ATK 🗡️: {}".format(carddata_atk), resp.channel_url)
                        time.sleep(1)
                        if re.search("Link", carddata_type):
                            chatbot.send_message("LINK 🔗: {}".format(carddata_link), resp.channel_url)
                            time.sleep(1)
                        else:
                            chatbot.send_message("DEF 🛡️: {}".format(carddata_def), resp.channel_url)
                            time.sleep(1)
                        if re.search("Pendulum", carddata_type):
                            chatbot.send_message("Pendulum Effect: {}".format(carddata_pendulumeffect), resp.channel_url)
                            time.sleep(1)
                            chatbot.send_message("Monster Effect: {}".format(carddata_text), resp.channel_url)
                            time.sleep(1)
                        else:
                            chatbot.send_message("{}".format(carddata_text), resp.channel_url)
                            time.sleep(1)
                        chatbot.send_message("{}".format(carddata_appearances), resp.channel_url)
                        time.sleep(1)

                    if re.search("Spell", carddata_type) or re.search("Trap", carddata_type):

                        chatbot.send_message("Card type: {}".format(carddata_type), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Property: {}".format(carddata_property), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("{}".format(carddata_text), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("{}".format(carddata_appearances), resp.channel_url)
                        time.sleep(1)

                        
                    #YGP
                    chatbot.send_message("Yugipedia: {}".format(link_long_1), resp.channel_url)
                    time.sleep(1)
                    
                    #FAN
                    link_long_9 = re.sub(r'yugipedia', 'yugioh.fandom', link_long_1)                   
                    chatbot.send_message("Fandom: {}".format(link_long_9), resp.channel_url)
                    time.sleep(1)

                #The card has a normal database code.
                #Let's process the card.
                #This section is largely redundant with the anime card section above.
                #Should really be objectified...
                
                if konami_code != '0000' and konami_code != '9999' and konami_code != "Anime":
                    cardtextextended = ""
                    carddata_type = ""
                    yppage = requests.get(link_long_1)
                    soup = BeautifulSoup(yppage.content, "html.parser")
                    
                    #card lore
                    loredump = ""
                    loredump = soup.find_all("div", {"class": "lore"})                  
                    carddata_text = str(loredump)                                   
                    carddata_text = re.sub("<br/>", " ", carddata_text)
                    carddata_text = re.sub("</dd>", " ", carddata_text)
                    carddata_text = re.sub("</dt>", " ", carddata_text)
                    carddata_text = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", carddata_text)
                    carddata_text = re.sub("<>", "", carddata_text)
                    carddata_text = "::"+carddata_text+"::"
                    carddata_text = re.sub("::\[", "", carddata_text)
                    carddata_text = re.sub("\]::", "", carddata_text)
                    
                    #card info collection, type, and image

                    imagedump = ""
                    imagedump2 = ""
                    imagedump = soup.find_all("div", {"class": "cardtable-main_image-wrapper"})
                    imagedump = str(imagedump)
                    imagedump2 = imagedump
                    if re.search("300px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/300px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    elif re.search("200px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/200px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    else:
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//)([^hg]*)(?=png(?!g))'
                        imagedump = re.search(imageregex, imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump+"png"

                    columndump = ""                    
                    
                    columndump = soup.find_all("div", {"class": "card-table-columns"})
                    columndump = str(columndump)
                    columndump = re.sub("<br/>", ":", columndump)
                    columndump = re.sub("</th>", ":", columndump)
                    columndump = re.sub("</td>", ":", columndump)
                    columndump = re.sub("</tr>", ":", columndump)
                    columndump = re.sub("</dd>", ":", columndump)                    
                    columndump = re.sub("</dt>", ":", columndump)
                    columndump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", columndump)
                    columndump = re.sub("<>", "", columndump)
                    columndump = re.sub("\[", "", columndump)
                    columndump = re.sub("\]", "", columndump)
                    columndump = re.sub("[:]+", ":", columndump)
                    columndump = re.findall("^.*", columndump, re.M)
                    columndump = str(columndump)
                    columndump = re.sub("'", "", columndump)
                    columndump = re.sub(",", "", columndump)
                    columndump = re.sub("[ ]+", " ", columndump)
                    columndump = re.sub(" :", ":", columndump)
                    columndump = re.sub(": ", ":", columndump)
                    columndump = re.sub("\[ ", ":", columndump)

                    carddata_status = re.search('(?<=(?<!:):Status:)([^::]*)(?=:(?!:))', columndump)
                    carddata_status = carddata_status.group()
                    carddata_status = str(carddata_status)

                    #Flag Rush Duel cards
                    
                    rush_duel = False
                    if re.search("Rush Duel", carddata_status):
                        rush_duel = True
                    
                    columndump = re.sub("Status.+", "", columndump)
                    
                    carddata_type = re.search('(?<=(?<!:):Card type:)([^::]*)(?=:(?!:))', columndump)
                    carddata_type = carddata_type.group()
                    carddata_type = str(carddata_type)

                    if carddata_type == "Monster":
                    
                        carddata_types = re.search('(?<=(?<!:):Types:)([^::]*)(?=:(?!:))', columndump)
                        carddata_types = carddata_types.group()
                        carddata_types = str(carddata_types) 

                        carddata_attribute = re.search('(?<=(?<!:):Attribute:)([^::]*)(?=:(?!:))', columndump)
                        carddata_attribute = carddata_attribute.group()
                        carddata_attribute = str(carddata_attribute)                        
                            
                        if carddata_attribute == "FIRE":
                            carddata_attribute += " 🔴"
                        if carddata_attribute == "LIGHT":
                            carddata_attribute += " 🟡"
                        if carddata_attribute == "WIND":
                            carddata_attribute += " 🟢"
                        if carddata_attribute == "WATER":
                            carddata_attribute += " 🔵"
                        if carddata_attribute == "DARK":
                            carddata_attribute += " 🟣"
                        if carddata_attribute == "EARTH":
                            carddata_attribute += " 🟤"
                        if carddata_attribute == "DIVINE":
                            carddata_attribute += " ⚪"
                        if carddata_attribute == "LAUGH":
                            carddata_attribute += " 🟠"                        
                                              
                        if re.search("Maximum", carddata_types):
                            carddata_type = "Maximum Monster 🟧"
                            carddata_max = re.search('(?<=(?<!:):MAXIMUM ATK:)([^::]*)(?=:(?!:))', columndump)
                            carddata_max = carddata_max.group()
                            carddata_max = str(carddata_max)                            
                    
                        elif re.search("Pendulum", carddata_types):
                            if re.search("Link", carddata_types):
                                carddata_type = "Pendulum Link Monster 🟦🟩"
                            elif re.search("Xyz", carddata_types):
                                carddata_type = "Pendulum Xyz Monster ⬛🟩"
                            elif re.search("Synchro", carddata_types):
                                carddata_type = "Pendulum Synchro Monster ⬜🟩"
                            elif re.search("Fusion", carddata_types):
                                carddata_type = "Pendulum Fusion Monster 🟪🟩"
                            elif re.search("Ritual", carddata_types):
                                carddata_type = "Pendulum Ritual Monster 🟦🟩"
                            elif re.search("Effect", carddata_types):
                                carddata_type = "Pendulum Effect Monster 🟧🟩"
                            else:
                                carddata_type = "Pendulum Normal Monster 🟨🟩"                            
                            
                            carddata_scale = re.search('(?<=(?<!:):Pendulum Scale:)([^::]*)(?=:(?!:))', columndump)
                            carddata_scale = carddata_scale.group()
                            carddata_scale = str(carddata_scale)                            
                            carddata_scale = "◀🟦 "+carddata_scale+" 🟥▶"
                    
                        elif re.search("Link", carddata_types):
                            carddata_type = "Link Monster 🟦"                        
                        
                            carddata_arrows = re.search('(?<=(?<!:):Link Arrows:)([^::]*)(?=:(?!:))', columndump)
                            carddata_arrows = carddata_arrows.group()
                            carddata_arrows = str(carddata_arrows)
                            carddata_arrow_symbol_builder = ""
                            if re.search("Top-Left", carddata_arrows):
                                carddata_arrow_symbol_builder += "↖️ "
                            if re.search("Top-Center", carddata_arrows):
                                carddata_arrow_symbol_builder += "⬆️ "
                            if re.search("Top-Right", carddata_arrows):
                                carddata_arrow_symbol_builder += "↗️ "
                            if re.search("Middle-Left", carddata_arrows):
                                carddata_arrow_symbol_builder += "⬅️ "
                            if re.search("Middle-Right", carddata_arrows):
                                carddata_arrow_symbol_builder += "➡️ "
                            if re.search("Bottom-Left", carddata_arrows):
                                carddata_arrow_symbol_builder += "↙️ "
                            if re.search("Bottom-Center", carddata_arrows):
                                carddata_arrow_symbol_builder += "⬇️ "
                            if re.search("Bottom-Right", carddata_arrows):
                                carddata_arrow_symbol_builder += "↘️ "
                            carddata_arrows = carddata_arrow_symbol_builder
                            carddata_atklink = re.search('(?<=(?<!:):ATK / LINK:)([^::]*)(?=:(?!:))', columndump)
                            carddata_atklink = carddata_atklink.group()
                            carddata_atklink = str(carddata_atklink)                                     
                            carddata_atk = re.sub(" / .+", "", carddata_atklink)
                            carddata_link = re.sub(".+ / ", "", carddata_atklink)                    
                        
                        elif re.search("Xyz", carddata_types):
                            carddata_type = "Xyz Monster ⬛"

                            carddata_level = re.search('(?<=(?<!:):Rank:)([^::]*)(?=:(?!:))', columndump)
                            carddata_level = carddata_level.group()
                            carddata_level = str(carddata_level)                                                
                            if len(carddata_level) > 0 and len(carddata_level) <= 2:
                                carddata_level = int(carddata_level)
                            else:
                                konami_code = "0000"
                            carddata_starchips = "  ⍟" * carddata_level  
                        
                        elif re.search("Synchro", carddata_types):
                            carddata_type = "Synchro Monster ⬜"                      
                        
                        elif re.search("Fusion", carddata_types):
                            carddata_type = "Fusion Monster 🟪"  
                        
                        elif re.search("Ritual", carddata_types):
                            carddata_type = "Ritual Monster 🟦"
                            
                        elif re.search("Effect", carddata_types):
                            carddata_type = "Effect Monster 🟧"
                            
                        else:
                            carddata_type = "Normal Monster 🟨"  
                    
                        if not re.search("Link", carddata_type) and not re.search("Xyz", carddata_type):
                            carddata_level = re.search('(?<=(?<!:):Level:)([^::]*)(?=:(?!:))', columndump)
                            carddata_level = carddata_level.group()
                            carddata_level = str(carddata_level)
                            if len(carddata_level) > 0 and len(carddata_level) <= 2:
                                carddata_level = int(carddata_level)
                            else:
                                konami_code = "0000"
                            carddata_starchips = "  ✪" * carddata_level
                            
                        if not re.search("Link", carddata_type):
                            carddata_atkdef = re.search('(?<=(?<!:):ATK / DEF:)([^::]*)(?=:(?!:))', columndump)
                            carddata_atkdef = carddata_atkdef.group()
                            carddata_atkdef = str(carddata_atkdef)
                            carddata_atk = re.sub(" / .+", "", carddata_atkdef)
                            carddata_def = re.sub(".+ / ", "", carddata_atkdef)                            
                    
                        carddata_types = re.sub("Aqua", "Aqua 💧", carddata_types)
                        carddata_types = re.sub("Beast", "Beast 🐗", carddata_types)
                        carddata_types = re.sub("Creator God", "Creator God 🌅", carddata_types)
                        carddata_types = re.sub("Cyberse", "Cyberse 🤖", carddata_types)
                        carddata_types = re.sub("Dinosaur", "Dinosaur 🦖", carddata_types)
                        carddata_types = re.sub("Divine-Beast 🐗", "Divine-Beast 📿", carddata_types)
                        carddata_types = re.sub("Dragon", "Dragon 🐉", carddata_types)
                        carddata_types = re.sub("Fairy", "Fairy 🧚", carddata_types)
                        carddata_types = re.sub("Fiend", "Fiend 👿", carddata_types)
                        carddata_types = re.sub("Fish", "Fish 🐟", carddata_types)
                        carddata_types = re.sub("Insect", "Insect 🪲", carddata_types)
                        carddata_types = re.sub("Machine", "Machine ⚙️", carddata_types)
                        carddata_types = re.sub("Plant", "Plant 🌱", carddata_types)
                        carddata_types = re.sub("Psychic", "Psychic 🧠", carddata_types)
                        carddata_types = re.sub("Pyro", "Pyro 🔥", carddata_types)
                        carddata_types = re.sub("Reptile", "Reptile 🦎", carddata_types)
                        carddata_types = re.sub("Rock", "Rock 🪨", carddata_types)
                        carddata_types = re.sub("Sea Serpent", "Sea Serpent 🐍", carddata_types)
                        carddata_types = re.sub("Spellcaster", "Spellcaster 🧙", carddata_types)
                        carddata_types = re.sub("Thunder", "Thunder 🌩️", carddata_types)
                        carddata_types = re.sub("Warrior", "Warrior ⚔️", carddata_types)
                        carddata_types = re.sub("Winged Beast 🐗", "Winged Beast 🦅", carddata_types)
                        carddata_types = re.sub("Wyrm", "Wyrm 🪱", carddata_types)
                        carddata_types = re.sub("Zombie", "Zombie 🧟", carddata_types)
                        carddata_types = re.sub("Pendulum", "Pendulum 🧬", carddata_types)
                        carddata_types = re.sub("Link", "Link 🔗", carddata_types)
                        carddata_types = re.sub("Xyz", "Xyz ☄️", carddata_types)
                        carddata_types = re.sub("Synchro", "Synchro 💫", carddata_types)
                        carddata_types = re.sub("Fusion", "Fusion 🌀", carddata_types)
                        carddata_types = re.sub("Ritual", "Ritual 🕯️", carddata_types)
                        carddata_types = re.sub("Effect", "Effect ⏩", carddata_types)
                        carddata_types = re.sub("Normal", "Normal ⏺️", carddata_types)
                        carddata_types = re.sub("Tuner", "Tuner 🧲", carddata_types)
                        carddata_types = re.sub("Gemini", "Gemini ♊", carddata_types)
                        carddata_types = re.sub("Flip", "Flip ↪️", carddata_types)
                        carddata_types = re.sub("Token", "Token 🎲", carddata_types)
                        carddata_types = re.sub("Toon", "Toon 🤪", carddata_types)
                        carddata_types = re.sub("Union", "Union 🫂", carddata_types)
                        carddata_types = re.sub("Spirit", "Spirit 👻", carddata_types)
                        carddata_types = re.sub("Maximum", "Maximum 💥", carddata_types)
                        carddata_types = re.sub("Beast 🐗-Warrior ⚔️", "Beast-Warrior 👹", carddata_types)
                        carddata_types = re.sub("Celestial Warrior ⚔️", "Celestial Warrior 🌠", carddata_types)
                        carddata_types = re.sub("Cyborg", "Cyborg 🧑‍🚀", carddata_types)
                        carddata_types = re.sub("High Dragon 🐉", "High Dragon 🏺", carddata_types)
                        carddata_types = re.sub("Magical Knight", "Magical Knight 🧝", carddata_types)
                        carddata_types = re.sub("Omega Psychic 🧠", "Omega Psychic 🧿", carddata_types)
                        carddata_types = re.sub("Galaxy", "Galaxy 🌌", carddata_types)
                        carddata_types = re.sub("Charisma", "Charisma 💋", carddata_types)
                        carddata_types = re.sub("Human", "Human 🧑", carddata_types)
                        carddata_types = re.sub("Business", "Business 💼", carddata_types)
                        carddata_types = re.sub("Newspaper", "Newspaper 📰", carddata_types)
                        carddata_types = re.sub("Swindler", "Swindler 🦹", carddata_types)
                        carddata_types = re.sub("Son", "Son 👦", carddata_types)
                        carddata_types = re.sub("Swirly", "Swirly 😵‍💫", carddata_types)
                        carddata_types = re.sub("Immortal", "Immortal 🧛", carddata_types)
                        carddata_types = re.sub("Yokai", "Yokai 🪀", carddata_types)
                        carddata_types = re.sub("Black Magic", "Black Magic 🔮", carddata_types)
                        carddata_types = re.sub("White Magic", "White Magic 🪄", carddata_types)
                        carddata_types = re.sub("Sea Beast 🐗", "Sea Beast 🧜‍", carddata_types)
                        carddata_types = re.sub("Illusion Magic", "Illusion Magic 🪞", carddata_types)
                        carddata_types = re.sub("Dragon 🐉 Magic", "Dragon Magic 🏮", carddata_types)
                    
                    if carddata_type == "Spell":
                        carddata_type = "Spell 🟩"

                        carddata_property = re.search('(?<=(?<!:):Property:)([^::]*)(?=:(?!:))', columndump)
                        carddata_property = carddata_property.group()
                        carddata_property = str(carddata_property) 
                        carddata_property = re.sub("Normal", "Normal ⏺️", carddata_property)
                        carddata_property = re.sub("Continuous", "Continuous ♾️", carddata_property)
                        carddata_property = re.sub("Ritual", "Ritual 🕯️", carddata_property)
                        carddata_property = re.sub("Quick-Play", "Quick-Play ⚡", carddata_property)
                        carddata_property = re.sub("Field", "Field ✧", carddata_property)
                        carddata_property = re.sub("Equip", "Equip ➕", carddata_property)                                 
                    
                    if carddata_type == "Trap":                
                        carddata_type = "Trap 🟪"

                        carddata_property = re.search('(?<=(?<!:):Property:)([^::]*)(?=:(?!:))', columndump)
                        carddata_property = carddata_property.group()
                        carddata_property = str(carddata_property)
                        carddata_property = re.sub("Normal", "Normal ⏺️", carddata_property)
                        carddata_property = re.sub("Continuous", "Continuous ♾️", carddata_property)
                        carddata_property = re.sub("Counter", "Counter ↩️", carddata_property)
                    
                    if rush_duel:
                        carddata_type = "Rush Duel "+carddata_type

                    #Build our reply.
                    
                    prettyName = html.unescape(re.sub(r'https://yugipedia.com/wiki/', '', re.sub(r'_', ' ', link_long_1)))
                    
                    prettyName = urllib.parse.unquote(prettyName)                    
                     
                    chatbot.send_message(prettyName, resp.channel_url)
                    time.sleep(1)
                    
                    chatbot.send_message("Image: "+carddata_image, resp.channel_url)
                    time.sleep(1)
                    
                    if re.search("Monster", carddata_type):
                        chatbot.send_message("Card type: {}".format(carddata_type), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Attribute: {}".format(carddata_attribute), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Monster type: {}".format(carddata_types), resp.channel_url)
                        time.sleep(1)
                        if re.search("Link", carddata_type):
                            chatbot.send_message("Link arrows: {}".format(carddata_arrows), resp.channel_url)
                            time.sleep(1)
                        elif re.search("Xyz", carddata_type):
                            chatbot.send_message("Rank: {} {}".format(carddata_level, carddata_starchips), resp.channel_url)
                            time.sleep(1)
                        else:
                            chatbot.send_message("Level: {} {}".format(carddata_level, carddata_starchips), resp.channel_url)
                            time.sleep(1)
                        if re.search("Pendulum", carddata_type):
                            chatbot.send_message("Pendulum scale: {}".format(carddata_scale), resp.channel_url)
                            time.sleep(1)
                        if re.search("Maximum", carddata_type):
                            chatbot.send_message("MAX ATK 💥: {}".format(carddata_max), resp.channel_url)
                            time.sleep(1)
                        chatbot.send_message("ATK 🗡️: {}".format(carddata_atk), resp.channel_url)
                        time.sleep(1)
                        if re.search("Link", carddata_type):
                            chatbot.send_message("LINK 🔗: {}".format(carddata_link), resp.channel_url)
                            time.sleep(1)
                        else:
                            chatbot.send_message("DEF 🛡️: {}".format(carddata_def), resp.channel_url)
                            time.sleep(1)
                        chatbot.send_message("{}".format(carddata_text), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("{}".format(carddata_status), resp.channel_url)
                        time.sleep(1)

                    if re.search("Spell", carddata_type) or re.search("Trap", carddata_type):

                        chatbot.send_message("Card type: {}".format(carddata_type), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("Property: {}".format(carddata_property), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("{}".format(carddata_text), resp.channel_url)
                        time.sleep(1)
                        chatbot.send_message("{}".format(carddata_status), resp.channel_url)
                        time.sleep(1)
                        
                    if rush_duel:
                        #YGP
                        chatbot.send_message("Yugipedia: {}".format(link_long_1), resp.channel_url)
                        time.sleep(1)

                        #KON
                        link_long_2 = "https://www.db.yugioh-card.com/rushdb/card_search.action?ope=2&cid={}".format(konami_code)
                        chatbot.send_message("Konami: {}".format(link_long_2), resp.channel_url)
                        time.sleep(1)
                        
                        #FAN
                        link_long_9 = re.sub(r'yugipedia', 'yugioh.fandom', link_long_1)                   
                        chatbot.send_message("Fandom: {}".format(link_long_9), resp.channel_url)
                        time.sleep(1)
                        
                        #PRO
                        link_long_3 = re.sub(r'https://yugipedia.com/wiki/', 'https://db.ygoprodeck.com/card/?search=', re.sub(r'_', '%20', link_long_1))                   
                        chatbot.send_message("YGOProDeck: {}".format(link_long_3), resp.channel_url)
                        time.sleep(1)

                    if not rush_duel:
                        #YGP
                        chatbot.send_message("Yugipedia: {}".format(link_long_1), resp.channel_url)
                        time.sleep(1)

                        #KON
                        link_long_2 = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid={}".format(konami_code)
                        chatbot.send_message("Konami: {}".format(link_long_2), resp.channel_url)
                        time.sleep(1)
                        
                        #FAN
                        link_long_9 = re.sub(r'yugipedia', 'yugioh.fandom', link_long_1)                   
                        chatbot.send_message("Fandom: {}".format(link_long_9), resp.channel_url)
                        time.sleep(1)
                        
                        #PRO
                        link_long_3 = re.sub(r'https://yugipedia.com/wiki/', 'https://db.ygoprodeck.com/card/?search=', re.sub(r'_', '%20', link_long_1))                   
                        chatbot.send_message("YGOProDeck: {}".format(link_long_3), resp.channel_url)
                        time.sleep(1)

                        #ORG
                        link_long_4 = "https://db.ygorganization.com/card#{}".format(konami_code)
                        chatbot.send_message("YGOrganization: {}".format(link_long_4), resp.channel_url)
                        time.sleep(1)
                        
                        #PRI
                        link_long_5 = re.sub(r'https://yugipedia.com/wiki/', 'https://yugiohprices.com/card_price?name=', re.sub(r'_', '%20', link_long_1))
                        chatbot.send_message("YugiohPrices: {}".format(link_long_5), resp.channel_url)
                        time.sleep(1)

                        #TCG
                        query_2 = ('{} yugioh tcgplayer'.format(re.sub(r'_', ' ', re.sub(r'https://yugipedia.com/wiki/', '', link_long_1))))
                        link_long_6 = "https://www.tcgplayer.com/search/yugioh/product?productLineName=yugioh"
                        for j in search(query_2, tld="com", lang="en", num=1, stop=1, pause=2):
                            link_long_6 = j
                        chatbot.send_message("TCGPlayer: {}".format(link_long_6), resp.channel_url)
                        time.sleep(1)
                        
                        #DLM
                        link_long_7 = re.sub(r'https://yugipedia.com/wiki/', 'https://www.duellinksmeta.com/cards/', re.sub(r'_', '%20', link_long_1)) 
                        chatbot.send_message("DuelLinksMeta: {}".format(link_long_7), resp.channel_url)
                        time.sleep(1)

                        #MDM
                        link_long_8 = re.sub(r'https://yugipedia.com/wiki/', 'https://www.masterduelmeta.com/cards/', re.sub(r'_', '%20', link_long_1))
                        chatbot.send_message("MasterDuelMeta: {}".format(link_long_8), resp.channel_url)
                        time.sleep(1)

                #Canned joke responses

                if app_name == "Abridged":
                    konami_code = "9999"
                    chatbot.send_message("Hm? Is that from Abridged? I love The Abridged Series! https://www.youtube.com/playlist?list=PLTagxffHmpfT765IfQj68dMmfFs3W7s1f", resp.channel_url)
                    time.sleep(1)

                if app_name == "Waifujokething":
                    konami_code = "9999"
                    chatbot.send_message("Waifu? I personally have a crush on CAN:D LIVE. https://yugipedia.com/wiki/CAN:D_LIVE", resp.channel_url)
                    time.sleep(1)
  
                if app_name == "your mom":
                    konami_code = "9999"
                    chatbot.send_message("I don't have a mother. 😢", resp.channel_url)
                    time.sleep(1)
  
                if app_name == "my mom":
                    konami_code = "9999"
                    chatbot.send_message("What's that? Something about your mom? Tell her I said hi. 😉", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "your dad":
                    konami_code = "9999"
                    chatbot.send_message("Did you have a question about my dad? He's u/symmetricalboy. Say hi!", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "my dad":
                    konami_code = "9999"
                    chatbot.send_message("Your dad is never coming back. Sorry.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "what does it do":
                    konami_code = "9999"
                    chatbot.send_message("Pot of Greed", resp.channel_url)
                    time.sleep(1)
                    chatbot.send_message("Pot of Greed, also known as Pot of Greed, is a card that is a card in both the Yu-Gi-Oh! Official Card Game as well as also the Yu-Gi-Oh! Trading Card Game and is a card that happens to be of the Spell card type, which is a type of card, and it is also a Normal Spell considered to be a Normal Spell when in the hand and on the field and in the Graveyard and when Banished by card effects, and the effect of which is that when it is activated by declaring an activation during the time when an activation may be declared by the player in control of that card being activated, it is placed on the controlling player's side of the field, which is the side of the field controlled by that player, and it is placed in any one of your Spell or Trap Card Zones, but not more than one, except the Field Spell Card Zone, or a Spell or Trap Card Zone occupied by another card which is controlled by either player, and if you do, you may Excavate, but not reveal, and subsequently Draw, two cards which are the top two cards from the top of your deck, and if you do, reveal them to yourself, and add them to your hand in any order; you do not shuffle your deck after targeting, excavating, drawing, selecting, and subsequently placing within your hand those two cards which were taken from the top of your deck and added to your hand, which is the hand of the player that controlled this card; after the card resolves it is sent from the Spell or Trap Card Zone in which it was activated to your Graveyard, which is the Graveyard on your side of the field, which is the side of the field controlled by the player that controlled this card.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "kiteroid":
                    konami_code = "9999"
                    chatbot.send_message("We're not gonna talk about Kiteroid.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Magic: The Gathering":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/magicTCG. I bet my friend u/MTGCardFetcher can help you there.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Pokémon":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/pokemon. I don't know how to search for Pokémon, but Scarlet and Violet look really cool!", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Digimon":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/digimon. I don't know how to search for Digimon, but I sure loved the first movie!", resp.channel_url)
                    time.sleep(1)
                
                #Didn't find a good match
                
                if konami_code == '0000':
                    chatbot.send_message(app_name, resp.channel_url)
                    time.sleep(1)
                    chatbot.send_message("No results.", resp.channel_url)
                    time.sleep(1)







            
            
            nOfFoundApps += 1
            logger.info("'{}' found.".format(app_name))

    #The above was for extended mode.
    #Now we repeat everything for short mode.
    #Definitely redundant beyond reason.
    #I'm not going to comment through everything,
    #It's mostly the same as above with less data collection
    #and more flag handling in the links.

    for app_name in app_names:
    
        app_name = app_name.lower()
        
        #Hard code corrections
        if re.search('-', app_name):
            app_name = re.sub('-', ' ', app_name)
            
        if re.search('rongo', app_name):
            app_name = re.sub('rongo', 'rhongo', app_name)

        if app_name.lower() == "simorgh":
            app_name = "Simorgh, Bird of Sovereignty"

        if app_name.lower() == "dad":
            app_name = "Dark Armed Dragon"

        if app_name.lower() == "rebd":
            app_name = "Red-Eyes Black Dragon"

        if app_name.lower() == "rml":
            app_name = "Royal Magical Library"

        if app_name.lower() == "drnm":
            app_name = "Dark Ruler No More"

        if app_name.lower() == "dm":
            app_name = "Dark Magician"

        if app_name.lower() == "brick":
            app_name = "Blue-Eyes White Dragon"

        if app_name.lower() == "kaiba":
            app_name = "Blue-Eyes White Dragon"

        if app_name.lower() == "yugi":
            app_name = "Dark Magician"

        if app_name.lower() == "joey":
            app_name = "Red-Eyes Black Dragon"
            
        if re.search("seto kaiba", app_name):
            app_name = "Blue-Eyes White Dragon"

        if re.search("yugi muto", app_name):
            app_name = "Dark Magician"

        if re.search("joey wheeler", app_name):
            app_name = "Red-Eyes Black Dragon"

        if app_name.lower() == "bls":
            app_name = "Black Luster Soldier"

        if app_name.lower() == "no fun allowed":
            app_name = "Solemn Judgement"

        if app_name.lower() == "very fun dragon":
            app_name = "True King of All Calamities"

        if app_name.lower() == "dn":
            app_name = "Dogmatika Nexus"

        if re.search("narval", app_name):
            app_name = re.sub("narval", "nervall", app_name)

        if app_name.lower() == "black lotus":
            app_name = "samsara lotus"

        if app_name.lower() == "goat":
            app_name = "Scapegoat"

        if app_name.lower() == "dragon":
            app_name = "chamber dragonmaid"

        if app_name.lower() == "dark magician pandora":
            app_name = "dark magician arkana"

        if re.search("numeronius", app_name):
            app_name = re.sub("numeronius", "numerounius", app_name)
            
        if app_name.lower() == "numerounius":
            app_name = "Number C1000: Numerounius"

        if app_name.lower() == "barian 1":
            app_name = "Number 1: Infection Buzz King"

        if app_name.lower() == "barian number 1":
            app_name = "Number 1: Infection Buzz King"
            
        if app_name.lower() == "barian 2":
            app_name = "Number 2: Ninja Shadow Mosquito"
            
        if app_name.lower() == "barian number 2":
            app_name = "Number 2: Ninja Shadow Mosquito"

        if app_name.lower() == "barian 3":
            app_name = "Number 3: Cicada King"

        if app_name.lower() == "barian number 3":
            app_name = "Number 3: Cicada King"

        if app_name.lower() == "barian 4":
            app_name = "Number 4: Stealth Kragen"

        if app_name.lower() == "barian number 4":
            app_name = "Number 4: Stealth Kragen"

        if app_name.lower() == "barian 10":
            app_name = "Number 10: Dark Illumiknight"

        if app_name.lower() == "barian number 10":
            app_name = "Number 10: Dark Illumiknight"

        if app_name.lower() == "c":
            app_name = "Maxx C"

        if app_name.lower() == "d":
            app_name = "Batteryman D"

        if app_name.lower() == "cybernetic horizon":
            app_name = "cybernetic horizon card"

        if app_name.lower() == "duelist alliance":
            app_name = "duelist alliance card"

        if app_name.lower() == "wight":
            app_name = "skull servant"

        if app_name.lower() == "skull archfiend":
            app_name = "summoned skull"

        if app_name.lower() == "critter":
            app_name = "sangan"            

        if app_name.lower() == "cyclone":
            app_name = "mystical space typhoon"

        if app_name.lower() == "gust of wind":
            app_name = "mystical wind typhoon"

        if app_name.lower() == "hurricane":
            app_name = "giant trunade"

        if app_name.lower() == "wyvern":
            app_name = "Winged Dragon, Guardian of the Fortress #2"

        if app_name.lower() == "chaos pod":
            app_name = "morphing jar 2"

        if app_name.lower() == "rda":
            app_name = "red dragon archfiend"

        if app_name.lower() == "hrda":
            app_name = "hot red dragon archfiend"

        if app_name.lower() == "hot rda":
            app_name = "hot red dragon archfiend"

        if app_name.lower() == "pugm":
            app_name = "perfectly ultimate great moth"

        if app_name.lower() == "gepd":
            app_name = "Galaxy-Eyes Photon Dragon"

        if app_name.lower() == "gedd":
            app_name = "Googly-Eyes Drum Dragon"

        if app_name.lower() == "chaos soldier":
            app_name = "black luster soldier"

        if app_name.lower() == "xyz":
            app_name = "xyz dragon dark rebellion"
 
        if app_name.lower() == "xyz dragon":
            app_name = "xyz dragon dark rebellion"

        if app_name.lower() == "golden sphere":
            app_name = "sphere mode"

        if app_name.lower() == "mobc":
            app_name = "magician of black chaos"

        if app_name.lower() == "ladd":
            app_name = "Light and Darkness Dragon"

        if app_name.lower() == "exodia":
            app_name = "exodia the forbidden one"

        if app_name.lower() == "ced":
            app_name = "Chaos Emperor Dragon Envoy of the End"

        if re.search("waifu", app_name):
            app_name = "Waifujokething"

        if re.search("go brrr", app_name):
            app_name = re.sub("go brrr", "", app_name)
            
        if re.search("goes brrr", app_name):
            app_name = re.sub("goes brrr", "", app_name)  

        if re.search("screw the rules", app_name):
            app_name = "Abridged"            

        if app_name.lower() == "etele":
            app_name = "Emergency Teleport"
            
        if re.search("yugi boy", app_name):
            app_name = "Abridged"
            
        if re.search("attention duelists", app_name):
            app_name = "Abridged"
        
        if app_name.lower() == "@ignister":
            app_name = "Achichi @Ignister"
            
        if app_name.lower() == "laugh":
            app_name = "charisma token"

        if app_name.lower() == "charisma":
            app_name = "charisma token"
        
        if app_name.lower() != 'none' and app_name.lower() != 'def' and app_name.lower() != 'default' and app_name.lower() != 'defaults' and app_name.lower() != 'fan' and app_name.lower() != 'fandom' and app_name.lower() != 'delete' and app_name.lower() != 'help' and app_name.lower() != 'all' and app_name.lower() != 'ygp' and app_name.lower() != 'yugipedia' and app_name.lower() != 'kon' and app_name.lower() != 'konami' and app_name.lower() != 'pro' and app_name.lower() != 'ygopro' and app_name.lower() != 'ygoprodeck' and app_name.lower() != 'org' and app_name.lower() != 'yugiorg' and app_name.lower() != 'yugiorganization' and app_name.lower() != 'pri' and app_name.lower() != 'prices' and app_name.lower() != 'yugiohprices' and app_name.lower() != 'tcg' and app_name.lower() != 'tcgplayer' and app_name.lower() != 'dl' and app_name.lower() != 'dlm' and app_name.lower() != 'duellinks' and app_name.lower() != 'duellinksmeta' and app_name.lower() != 'md' and app_name.lower() != 'mdm' and app_name.lower() != 'masterduel' and app_name.lower() != 'masterduelmeta':
 
            nOfRequestedApps += 1
            
            singleCard = ""
            
            konami_code = "0000"
            
            if len(reply_body) < 8000:
                query_1 = ('{} "yugipedia"'.format(app_name))
                link_long_1 = "https://yugipedia.com/wiki/"
                for j in search(query_1, tld="com", lang="en", num=1, stop=1, pause=2):
                    link_long_1 = j
                
                if re.search("yugipedia", link_long_1):
                    #Get card code
                    yppage = requests.get(link_long_1)
                    soup = BeautifulSoup(yppage.content, "html.parser")
                    ypdump = soup.get_text()
                    konami_code = '0000'
                    if re.search("Yugioh-Card database #[0-9]+", ypdump):
                        konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                        konami_code = konami_code.group()
                        konami_code = str(konami_code)
                        konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                    else:
                        footerdump = soup.find_all("div", {"class": "below hlist"})
                        footerdump = str(footerdump)
                        if re.search("Anime cards", footerdump):
                            konami_code = "Anime"

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=2, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        #Get card code
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=3, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        #Get card code
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                if konami_code == '0000':
                
                    query_1 = ('{} "yugipedia"'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=4, pause=2):
                        link_long_1 = j
                    
                    if re.search("yugipedia", link_long_1):
                        #Get card code
                        yppage = requests.get(link_long_1)
                        soup = BeautifulSoup(yppage.content, "html.parser")
                        ypdump = soup.get_text()
                        konami_code = '0000'
                        if re.search("Yugioh-Card database #[0-9]+", ypdump):
                            konami_code = re.search("Yugioh-Card database #[0-9]+", ypdump)
                            konami_code = konami_code.group()
                            konami_code = str(konami_code)
                            konami_code = re.sub(r'Yugioh-Card database #', '', konami_code)
                        else:
                            footerdump = soup.find_all("div", {"class": "below hlist"})
                            footerdump = str(footerdump)
                            if re.search("Anime cards", footerdump):
                                konami_code = "Anime"

                if konami_code == '0000':
                    query_1 = ('{} -tcgplayer -wikipedia'.format(app_name))
                    link_long_1 = "https://yugipedia.com/wiki/"
                    for j in search(query_1, tld="com", lang="en", num=1, stop=1, pause=2):
                        link_long_1 = j            

                    if re.search("wizards", link_long_1) or re.search("cardkingdom", link_long_1):
                        app_name = "Magic: The Gathering"
                        ygocbFlags = ""
                        konami_code = "9999"
                    if re.search("pokémon", link_long_1) or re.search("pokemon", link_long_1) or re.search("bulbapedia", link_long_1):
                        app_name = "Pokémon"
                        ygocbFlags = ""   
                        konami_code = "9999"
                    if re.search("digimon", link_long_1) or re.search("wikimon", link_long_1):
                        app_name = "Digimon"
                        ygocbFlags = ""
                        konami_code = "9999"

                if konami_code != '0000' and konami_code != '9999':
                
                    titledump = soup.find_all("h1", {"class": "firstHeading"})
                    titledump = str(titledump)
                    titledump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", titledump)
                    titledump = re.sub("<>", "", titledump)
                    titledump = re.sub("\[", "", titledump)
                    titledump = re.sub("\]", "", titledump)
                    titledump = re.sub(" ", "_", titledump)
                    link_long_1 = "https://yugipedia.com/wiki/"+titledump

                    link_long_1 = html.unescape(link_long_1)

                if link_long_1 == "https://yugipedia.com/wiki/":
                    konami_code = '0000'

                if konami_code != '0000' and konami_code != '9999':
                    imagedump = ""
                    imagedump2 = ""
                    imagedump = soup.find_all("div", {"class": "cardtable-main_image-wrapper"})
                    imagedump = str(imagedump)
                    imagedump2 = imagedump
                    if re.search("300px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/300px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    elif re.search("200px", imagedump):
                        imagedump = re.search('(?<=(?<!\<)\<a class="image" href="/wiki/File:)([^<>]*)(?="\>(?!\>))', imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//thumb/)([^hx]*)(?=/'+re.escape(imagedump)+r'/200px(?!x))'
                        imagedump2 = re.search(imageregex, imagedump2)
                        imagedump2 = imagedump2.group()
                        imagedump2 = str(imagedump2)
                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump2+"/"+imagedump
                    else:
                        imageregex = r'(?<=(?<!h)https://ms.yugipedia.com//)([^hg]*)(?=png(?!g))'
                        imagedump = re.search(imageregex, imagedump)
                        imagedump = imagedump.group()
                        imagedump = str(imagedump)                        
                        carddata_image = "https://ms.yugipedia.com//"+imagedump+"png"

                    rush_duel = False
                    if konami_code != 'Anime':
                        columndump = ""                    
                        
                        columndump = soup.find_all("div", {"class": "card-table-columns"})
                        columndump = str(columndump)
                        columndump = re.sub("<br/>", ":", columndump)
                        columndump = re.sub("</th>", ":", columndump)
                        columndump = re.sub("</td>", ":", columndump)
                        columndump = re.sub("</tr>", ":", columndump)
                        columndump = re.sub("</dd>", ":", columndump)                    
                        columndump = re.sub("</dt>", ":", columndump)
                        columndump = re.sub("(?<=(?<!\<)\<)([^<>]*)(?=\>(?!\>))", "", columndump)
                        columndump = re.sub("<>", "", columndump)
                        columndump = re.sub("\[", "", columndump)
                        columndump = re.sub("\]", "", columndump)
                        columndump = re.sub("[:]+", ":", columndump)
                        columndump = re.findall("^.*", columndump, re.M)
                        columndump = str(columndump)
                        columndump = re.sub("'", "", columndump)
                        columndump = re.sub(",", "", columndump)
                        columndump = re.sub("[ ]+", " ", columndump)
                        columndump = re.sub(" :", ":", columndump)
                        columndump = re.sub(": ", ":", columndump)
                        columndump = re.sub("\[ ", ":", columndump)

                        carddata_status = re.search('(?<=(?<!:):Status:)([^::]*)(?=:(?!:))', columndump)
                        carddata_status = carddata_status.group()
                        carddata_status = str(carddata_status)
                        
                        rush_duel = False
                        if re.search("Rush Duel", carddata_status):
                            rush_duel = True

                    prettyName = html.unescape(re.sub(r'https://yugipedia.com/wiki/', '', re.sub(r'_', ' ', link_long_1)))
                    
                    prettyName = urllib.parse.unquote(prettyName)                    
                     
                    chatbot.send_message(prettyName, resp.channel_url)
                    time.sleep(1)
                    
                    chatbot.send_message("Image: "+carddata_image, resp.channel_url)
                    time.sleep(1)

                    #YGP
                    if re.search('all', ygocbFlags.lower()) or re.search('ygp', ygocbFlags.lower()) or re.search('yugipedia', ygocbFlags.lower()):
                        chatbot.send_message("Yugipedia: {}".format(link_long_1), resp.channel_url)
                        time.sleep(1)

                    #KON
                    if re.search('all', ygocbFlags.lower()) or re.search('kon', ygocbFlags.lower()):
                        if konami_code != 'Anime' and rush_duel == False:
                            link_long_2 = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid={}".format(konami_code)
                            chatbot.send_message("Konami: {}".format(link_long_2), resp.channel_url)
                            time.sleep(1)
                        if konami_code != 'Anime' and rush_duel == True:
                            link_long_2 = "https://www.db.yugioh-card.com/rushdb/card_search.action?ope=2&cid={}".format(konami_code)
                            chatbot.send_message("Konami: {}".format(link_long_2), resp.channel_url)
                            time.sleep(1)
                    
                     #FAN
                    if re.search('all', ygocbFlags.lower()) or re.search('fan', ygocbFlags.lower()):
                        link_long_9 = re.sub(r'yugipedia', 'yugioh.fandom', link_long_1)                   
                        chatbot.send_message("Fandom: {}".format(link_long_9), resp.channel_url)           
                        time.sleep(1)
                        
                    if konami_code != 'Anime':
                        #PRO
                        if re.search('all', ygocbFlags.lower()) or re.search('pro', ygocbFlags.lower()):
                            link_long_3 = re.sub(r'https://yugipedia.com/wiki/', 'https://db.ygoprodeck.com/card/?search=', re.sub(r'_', '%20', link_long_1))                   
                            chatbot.send_message("YGOProDeck: {}".format(link_long_3), resp.channel_url)
                            time.sleep(1)
                            
                    if konami_code != 'Anime' and rush_duel == False:
                        #ORG
                        if re.search('all', ygocbFlags.lower()) or re.search('org', ygocbFlags.lower()):
                            link_long_4 = "https://db.ygorganization.com/card#{}".format(konami_code)
                            chatbot.send_message("YGOrganization: {}".format(link_long_4), resp.channel_url)
                            time.sleep(1)
                            
                        #PRI
                        if re.search('all', ygocbFlags.lower()) or re.search('pri', ygocbFlags.lower()):
                            link_long_5 = re.sub(r'https://yugipedia.com/wiki/', 'https://yugiohprices.com/card_price?name=', re.sub(r'_', '%20', link_long_1))
                            chatbot.send_message("YugiohPrices: {}".format(link_long_5), resp.channel_url)
                            time.sleep(1)
                            
                        #TCG
                        if re.search('all', ygocbFlags.lower()) or re.search('tcg', ygocbFlags.lower()):
                            query_2 = ('{} yugioh tcgplayer'.format(re.sub(r'_', ' ', re.sub(r'https://yugipedia.com/wiki/', '', link_long_1))))
                            link_long_6 = "https://www.tcgplayer.com/search/yugioh/product?productLineName=yugioh"
                            for j in search(query_2, tld="com", lang="en", num=1, stop=1, pause=2):
                                link_long_6 = j
                            chatbot.send_message("TCGPlayer: {}".format(link_long_6), resp.channel_url)                   
                            time.sleep(1)
                            
                        #DLM
                        if re.search('all', ygocbFlags.lower()) or re.search('dl', ygocbFlags.lower()) or re.search('duellinks', ygocbFlags.lower()):
                            link_long_7 = re.sub(r'https://yugipedia.com/wiki/', 'https://www.duellinksmeta.com/cards/', re.sub(r'_', '%20', link_long_1)) 
                            chatbot.send_message("DuelLinksMeta: {}".format(link_long_7), resp.channel_url)
                            time.sleep(1)
                            
                        #MDM
                        if re.search('all', ygocbFlags.lower()) or re.search('md', ygocbFlags.lower()) or re.search('masterduel', ygocbFlags.lower()):
                            link_long_8 = re.sub(r'https://yugipedia.com/wiki/', 'https://www.masterduelmeta.com/cards/', re.sub(r'_', '%20', link_long_1))
                            chatbot.send_message("MasterDuelMeta: {}".format(link_long_8), resp.channel_url)                          
                            time.sleep(1)
                            
                if app_name == "Abridged":
                    konami_code = "9999"
                    chatbot.send_message("Hm? Is that from Abridged? I love The Abridged Series! https://www.youtube.com/playlist?list=PLTagxffHmpfT765IfQj68dMmfFs3W7s1f", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Waifujokething":
                    konami_code = "9999"
                    chatbot.send_message("Waifu? I personally have a crush on CAN:D LIVE. https://yugipedia.com/wiki/CAN:D_LIVE", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "your mom":
                    konami_code = "9999"
                    chatbot.send_message("I don't have a mother. 😢", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "my mom":
                    konami_code = "9999"
                    chatbot.send_message("What's that? Something about your mom? Tell her I said hi. 😉", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "your dad":
                    konami_code = "9999"
                    chatbot.send_message("Did you have a question about my dad? He's u/symmetricalboy. Say hi!", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "my dad":
                    konami_code = "9999"
                    chatbot.send_message("Your dad is never coming back. Sorry.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "what does it do":
                    konami_code = "9999"
                    chatbot.send_message("Pot of Greed", resp.channel_url)
                    time.sleep(1)
                    chatbot.send_message("Pot of Greed, also known as Pot of Greed, is a card that is a card in both the Yu-Gi-Oh! Official Card Game as well as also the Yu-Gi-Oh! Trading Card Game and is a card that happens to be of the Spell card type, which is a type of card, and it is also a Normal Spell considered to be a Normal Spell when in the hand and on the field and in the Graveyard and when Banished by card effects, and the effect of which is that when it is activated by declaring an activation during the time when an activation may be declared by the player in control of that card being activated, it is placed on the controlling player's side of the field, which is the side of the field controlled by that player, and it is placed in any one of your Spell or Trap Card Zones, but not more than one, except the Field Spell Card Zone, or a Spell or Trap Card Zone occupied by another card which is controlled by either player, and if you do, you may Excavate, but not reveal, and subsequently Draw, two cards which are the top two cards from the top of your deck, and if you do, reveal them to yourself, and add them to your hand in any order; you do not shuffle your deck after targeting, excavating, drawing, selecting, and subsequently placing within your hand those two cards which were taken from the top of your deck and added to your hand, which is the hand of the player that controlled this card; after the card resolves it is sent from the Spell or Trap Card Zone in which it was activated to your Graveyard, which is the Graveyard on your side of the field, which is the side of the field controlled by the player that controlled this card.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "kiteroid":
                    konami_code = "9999"
                    chatbot.send_message("We're not gonna talk about Kiteroid.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Magic: The Gathering":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/magicTCG. I bet my friend u/MTGCardFetcher can help you there.", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Pokémon":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/pokemon. I don't know how to search for Pokémon, but Scarlet and Violet look really cool!", resp.channel_url)
                    time.sleep(1)
                    
                if app_name == "Digimon":
                    konami_code = "9999"
                    chatbot.send_message("I think you might be looking for r/digimon. I don't know how to search for Digimon, but I sure loved the first movie!", resp.channel_url)
                    time.sleep(1)
                    
                if konami_code == '0000':
                    chatbot.send_message(app_name, resp.channel_url)
                    time.sleep(1)
                    chatbot.send_message("No results.", resp.channel_url)
                    time.sleep(1)
                    
            nOfFoundApps += 1
            logger.info("'{}' found.".format(prettyName))

    #Help mode

    if re.search('help', ygocbFlags.lower()):
        chatbot.send_message("Hello!", resp.channel_url)
        time.sleep(1)
        chatbot.send_message("I can help you find information about cards. To ask me about a card, just type the card name, or something close to it, in curly brackets. Then I'll reply with links to all sorts of sites with details about the card. Try it out now!", resp.channel_url)
        time.sleep(1)
 
























#Build the log file
 
logger = make_logger(Config.loggerName, 
    logfile=Config.logFile, 
    loggin_level=Config.loggingLevel)

#main method
#This is the part that actually does stuff.
#All of the above is called from within this section.
#When it finishes a comment, it loops back through this, forever or until it breaks.

if __name__ == "__main__":

    #This is the bot signing into Reddit
    
    try:
        reddit_authentication = RedditAuthentication.PasswordAuth(reddit_username=Config.username,
                                                                  reddit_password=Config.password,
                                                                  twofa=None)
         
        chatbot = ChatBot(print_chat=True,
                          store_session=True,
                          log_websocket_frames=False,
                          authentication=reddit_authentication)
         
        logger.info("Successfully logged in")

    except Exception as e:
        logger.critical("Unknown exception '{}' occured on login!".format(e))
        stopBot()



    #This section handles the bot request syntax that the user types in.
    #This is how the bot figures out if someone is trying to call it.
    #It's listening for patterns of brackets and parenteses and whatever.
    #I really do not recommend you edit this.
    #It was absolutely awful getting it to work correctly.
    #Python regex is bananas and doesn't do what you expect.
    #If you think you understand it, it changes the rules with one character.
    #Just marvel at the insanity of those symbols and don't touch it.

    link_me_regex1 = re.compile("(?<=(?<!\{)\{)([^{}]*)(?=\}(?!\}))", re.M | re.I)

    link_me_regex2 = re.compile("(?<=(?<!\{)\{\{)([^{}]*)(?=\}\}(?!\}))", re.M | re.I)

    link_me_regex3 = re.compile(r"(?<=(?<!\\)\\\[\\\[)([^\\]*)(?=\\\]\\\](?!\\))", re.M | re.I)

    link_me_regex4 = re.compile(r"(?<=(?<!\\)\\\[\\\[\\\[)([^\\]*)(?=\\\]\\\]\\\](?!\\))", re.M | re.I)

    link_me_regex5 = re.compile(r"(?<=(?<!\\)\\\\\[\\\\\[)([^\\]*)(?=\\\\\]\\\\\](?!\\))", re.M | re.I)

    link_me_regex6 = re.compile(r"(?<=(?<!\\)\\\\\[\\\\\[\\\\\[)([^\\]*)(?=\\\\\]\\\\\]\\\\\](?!\\))", re.M | re.I)

    link_me_regex7 = re.compile("(?<=(?<!\<)\<\<)([^<>]*)(?=\>\>(?!\>))", re.M | re.I)

    link_me_regex8 = re.compile("(?<=(?<!\<)\<\<\<)([^<>]*)(?=\>\>\>(?!\>))", re.M | re.I)

    link_me_regex9 = re.compile("(?<=(?<!\()\(\()([^()]*)(?=\)\)(?!\)))", re.M | re.I)

    link_me_regex10 = re.compile("(?<=(?<!\()\(\(\()([^()]*)(?=\)\)\)(?!\)))", re.M | re.I)

    #Loop forever

    while(1):
        
        #Accept chat invites and greeting
        
        @chatbot.event.on_invitation
        def on_invit(resp):

            chatbot.accept_chat_invite(resp.channel_url)
            chatbot.send_message("Hi! How can I help?", resp.channel_url)
            time.sleep(1)
            return True     

        #Listen for a new message

        @chatbot.event.on_message
        def chat_responder(resp):
            comment = resp.message                
         
            comment = str(comment)

            #When it gets something new, search for things that match the bot syntax
            #to see if we want to respond at all or ignore it.
         
            clean_comment = re.sub(r'\[', '\\\[', comment)
            clean_comment = re.sub(r'\]', '\\\]', clean_comment)
            
            clean_comment = re.sub(r',', ' ', clean_comment)  
            clean_comment = re.sub(r'/', ' ', clean_comment)                
            
            link_me_requests = ""
            link_me_requests_extended = ""
            
            link_me_requests = link_me_regex1.findall(clean_comment)
            link_me_requests_extended = link_me_regex2.findall(clean_comment) 
            link_me_requests += link_me_regex3.findall(clean_comment)
            link_me_requests_extended += link_me_regex4.findall(clean_comment)                
            link_me_requests += link_me_regex5.findall(clean_comment)
            link_me_requests_extended += link_me_regex6.findall(clean_comment)
            link_me_requests += link_me_regex7.findall(clean_comment)
            link_me_requests_extended += link_me_regex8.findall(clean_comment)
            link_me_requests += link_me_regex9.findall(clean_comment)
            link_me_requests_extended += link_me_regex10.findall(clean_comment)                
            
            #If it sees a request, we get to work!

            if len(link_me_requests) > 0 or len(link_me_requests_extended) > 0:
                
                #While the chat bot is processing a request, it puts up a typing indicator.
                
                chatbot.send_typing_indicator(resp.channel_url)                        
                        
                logger.debug("Generating reply to '{}'".format(comment))
       
                generate_reply(link_me_requests, link_me_requests_extended, resp)
                
                chatbot.stop_typing_indicator(resp.channel_url)
        
        #Chatbot code that keeps it alive
        
        chatbot.run_4ever(auto_reconnect=True)






#This file was last updated 2022-20-05 05:30 AM by Dylan Singer




