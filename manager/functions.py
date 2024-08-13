from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from manager.database import DB
import pycountry, phonenumbers 
from phonenumbers.phonenumberutil import region_code_for_number
import os
import base64
import time
import requests 

async def TClient(ses):
    client = TelegramClient(StringSession(ses), 13367220, "52cdad8b941c04c0c85d28ed6b765825")
    await client.connect()
    get = await client.get_me()
    if not get:
        return False
    return client

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
