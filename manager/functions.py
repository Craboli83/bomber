from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from manager.database import DB
import pycountry, phonenumbers 
from phonenumbers.phonenumberutil import region_code_for_number
from bs4 import BeautifulSoup
from traceback import format_exc
import os
import pathlib
import base64
import time
import requests 
import importlib
import glob
import re
import sys

def load_plugins(folder):
    plugs = []
    notplugs = {}
    for file in glob.glob(folder + "*.py"):
        plugin_name = os.path.basename(file)
        try:
            path = pathlib.Path(f"manager/plugins/{plugin_name}")
            name = "manager.plugins.{}".format(plugin_name.replace(".py" , ""))
            spec = importlib.util.spec_from_file_location(name, path)
            load = importlib.util.module_from_spec(spec)
            load.logger = logging.getLogger(plugin_name)
            spec.loader.exec_module(load)
            sys.modules[name] = load
            plugs.append(plugin_name)
        except:
            notplugs.update({plugin_name: format_exc()})
    return plugs, notplugs

async def TClient(session):
    try:
        client = TelegramClient(StringSession(session), 13367220, "52cdad8b941c04c0c85d28ed6b765825", device_model="AccManager 🔐")
    except:
        return False
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
