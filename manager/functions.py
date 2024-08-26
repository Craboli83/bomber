from manager import *
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from manager.database import DB
import pycountry, phonenumbers 
from phonenumbers.phonenumberutil import region_code_for_number
from bs4 import BeautifulSoup
from traceback import format_exc
import os
import base64
import random
import time
import requests 
import importlib
import glob
import re

ACCOUNTS = {}

def load_plugins(folder):
    plugs = []
    notplugs = {}
    for file in glob.glob(folder + "*.py"):
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            importlib.import_module(filename)
            plugs.append(os.path.basename(file))
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return plugs, notplugs

async def Tlient(session, phone=None):
    if phone and phone in ACCOUNTS:
        client = ACCOUNTS[phone]
        await client.connect()
        if client and (await client.get_me()):
            return client
        else:
            del ACCOUNTS[phone]
            return False
            
async def TClient(session, phone=None):
    try:
        client = TelegramClient(
            session=StringSession(session),
            api_id=API_ID,
            api_hash=API_HASH,
            device_model="Manager 🔐",
        )
        await client.connect()
    except:
        return False
    if (await client.get_me()):
        return client
    else:
        return False

def get_flag(number):
    try:
        pn = phonenumbers.parse(str(number))
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
        flag = country.flag
    except:
        flag = "🏴󠁩󠁲󠁡󠁮󠁿­"
    return flag

def search_photo(query):
    query = query.replace(" ", "-")
    link = "https://unsplash.com/s/photos/" + query
    extra = requests.get(link).content
    res = BeautifulSoup(extra, "html.parser", from_encoding="utf-8")
    all = res.find_all("img", "YVj9w")
    return [image["src"] for image in all]