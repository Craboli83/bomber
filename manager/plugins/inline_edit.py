from manager import bot, LOG_GROUP
from . import main_menu, manage_menu
from manager.events import Callback
from telethon import functions, types, Button
from manager.functions import TClient, get_flag
from manager.database import DB
import faker
import re
import requests
import random

@Callback(data="yesedit:(.*)")
async def yesedit(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    fake = faker.Faker(faker.config.AVAILABLE_LOCALES)
    profile = fake.simple_profile()
    if DB.get_key("CHANGE_ACCS_NAME")[event.sender_id] == "yes":
        if DB.get_key("CHANGE_ACCS_FLAG")[event.sender_id] == "yes":
            fname = str(flag) + " " + profile["name"] + " " + str(flag)
        else:
            fname = profile["name"]
        try:
            await client(functions.account.UpdateProfileRequest(first_name=fname))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_BIO")[event.sender_id] == "yes":
        try:
            await client(functions.account.UpdateProfileRequest(about=fake.text().split(".")[0]))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_BIRTH")[event.sender_id] == "yes":
        try:
            date = str(profile["birthdate"])
            date = date.split("-")
            year, month, day = date[0], date[1], date[2]
            await client(functions.account.UpdateBirthdayRequest(birthday=types.Birthday(day=day, month=month, year=year)))
        except Exception as e:
            await client.send_message("Theaboli", str(e))
            pass
    if DB.get_key("CHANGE_ACCS_PHOTO")[event.sender_id] == "yes":
        try:
            pics = search_photo(random.choice(["men", "women", "boy", "girl"]))
            pic = random.choice(pics)
            img_data = requests.get(pic).content
            with open("photo.jpg", "wb") as handler:
                handler.write(img_data) 
            file = await client.upload_file("photo.jpg")
            await client(functions.photos.UploadProfilePhotoRequest(file=file))
            os.remove("photo.jpg")
        except:
            pass
    await event.edit(f"**✅ Account Successfuly Edited And Manage Menu Send For You:**\n\n__❗ Dont Delete This Menu!__")
    menu = manage_menu(phone)
    await event.reply(f"""
**#Manage_Menu**

**📱 Phone:** ( {flag} `{phone}` {flag} )

__❗ Dont Delete This Menu!__

**#Manage_Menu**
""", buttons=menu)
    await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))

@Callback(data="noedit:(.*)")
async def noedit(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    await event.edit(f"**✅ Account Not Edited And Manage Menu Send For You:**\n\n__❗ Dont Delete This Menu!__")
    menu = manage_menu(phone)
    await event.reply(f"""
**#Manage_Menu**

**📱 Phone:** ( {flag} `{phone}` {flag} )

__❗ Dont Delete This Menu!__

**#Manage_Menu**
""", buttons=menu)
    await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))