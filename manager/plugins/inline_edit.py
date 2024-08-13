from manager import bot, LOG_GROUP
from manager.events import Callback
from telethon import Button
from manager.functions import TClient
from manager.database import DB
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from faker import Faker
from . import main_menu, manage_menu
from manager.functions import search_photo, get_flag
import re
import requests
import random

@Callback(data="yesedit\:(.*)")
async def yesedit(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    fake = Faker()
    if DB.get_key("CHANGE_ACCS_FNAME")[event.sender_id] == "yes":
        if DB.get_key("CHANGE_ACCS_FLAG")[event.sender_id] == "yes":
            fname = str(flag) + " " + fake.first_name()
        else:
            fname = fake.first_name()
        try:
            await client(UpdateProfileRequest(first_name=fname))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_LNAME")[event.sender_id] == "yes":
        if DB.get_key("CHANGE_ACCS_FLAG")[event.sender_id] == "yes":
            lname = fake.last_name() + " " + str(flag)
        else:
            lname = fake.last_name()
        try:
            await client(UpdateProfileRequest(last_name=lname))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_BIO")[event.sender_id] == "yes":
        try:
            await client(UpdateProfileRequest(about=fake.text().split(".")[0]))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_PHOTO")[event.sender_id] == "yes":
        try:
            pics = search_photo(random.choice(["men", "women", "boy", "girl"]))
            pic = random.choice(pics)
            img_data = requests.get(pic).content
            with open("photo.jpg", "wb") as handler:
                handler.write(img_data) 
            file = await client.upload_file("photo.jpg")
            await client(UploadProfilePhotoRequest(file=file))
            os.remove("photo.jpg")
        except:
            pass
    await event.edit(f"**✅ Account Successfuly Edited And Manage Menu Send For You:**\n\n__❗ Dont Delete This Menu!__", buttons=main_menu(event))
    menu = manage_menu(phone)
    await event.reply(f"""
**#Manage_Menu**

**📱 Phone:** ( {flag} `{phone}` {flag} )

__❗ Dont Delete This Menu!__

**#Manage_Menu**
""", buttons=menu)
    await bot.send_message(LOG_GROUP, f"**#New_Acc**\n\n**📱 Account Number:** ( {flag} `{phone}` {flag} )\n**🆔 UserID:** ( `{event.sender_id}` )")
    
@Callback(data="noedit\:(.*)")
async def noedit(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    await event.edit(f"**✅ Account Not Edited And Manage Menu Send For You:**\n\n__❗ Dont Delete This Menu!__", buttons=main_menu(event))
    menu = manage_menu(phone)
    await event.reply(f"""
**#Manage_Menu**

**📱 Phone:** ( {flag} `{phone}` {flag} )

__❗ Dont Delete This Menu!__

**#Manage_Menu**
""", buttons=menu)
    await bot.send_message(LOG_GROUP, f"**#New_Acc**\n\n**📱 Account Number:** ( {flag} `{phone}` {flag} )\n**🆔 UserID:** ( `{event.sender_id}` )")
