from manager import bot, LOG_GROUP
from telethon import events, Button
from manager.events import Cmd
from manager.database import DB
from . import setting_menu
import re
import random

@Cmd(pattern="Account Settings ⚙️")
async def acc_settings(event):
    await event.reply(f"**• Welcome To Setting Panel For Your Accounts:**\n\n__• Edit Your Change Account Settings:__", buttons=setting_menu(event))

@bot.on(events.CallbackQuery(data=re.compile("ch\_(.*)\:(.*)")))
async def change_set(event):
    type = str(event.pattern_match.group(1).decode('utf-8'))
    id = str(event.pattern_match.group(2).decode('utf-8'))
    if type == "fname":
        all = DB.get_key("CHANGE_ACCS_FNAME")
        last = "no" if all[event.sender_id] == "yes" else "yes"
        all[event.sender_id] = last
        DB.set_key("CHANGE_ACCS_FNAME", all)
    elif type == "lname":
        all = DB.get_key("CHANGE_ACCS_LNAME")
        last = "no" if all[event.sender_id] == "yes" else "yes"
        all[event.sender_id] = last
        DB.set_key("CHANGE_ACCS_LNAME", all)
    elif type == "bio":
        all = DB.get_key("CHANGE_ACCS_BIO")
        last = "no" if all[event.sender_id] == "yes" else "yes"
        all[event.sender_id] = last
        DB.set_key("CHANGE_ACCS_BIO", all)
    elif type == "uname":
        all = DB.get_key("CHANGE_ACCS_USERNAME")
        last = "no" if all[event.sender_id] == "yes" else "yes"
        all[event.sender_id] = last
        DB.set_key("CHANGE_ACCS_USERNAME", all)
    elif type == "photo":
        all = DB.get_key("CHANGE_ACCS_PHOTO")
        last = "no" if all[event.sender_id] == "yes" else "yes"
        all[event.sender_id] = last
        DB.set_key("CHANGE_ACCS_PHOTO", all)
    await event.edit(buttons=setting_menu(event))
