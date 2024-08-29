from manager import bot, LOG_GROUP
from . import main_menu
from manager.events import Callback
from telethon import functions, types, Button
from manager.functions import TClient, get_flag
from manager.database import DB
import faker
import random
import re
import os

@Callback(data="editacc:(.*)")
async def editacc(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    await event.edit("`♻️ Please Wait . . .`")
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
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
            await client(functions.account.UpdateProfileRequest(first_name=fname, last_name=""))
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
            year, month, day = int(date[0]), int(date[1]), int(date[2])
            await client(functions.account.UpdateBirthdayRequest(birthday=types.Birthday(day=day, month=month, year=year)))
        except:
            pass
    if DB.get_key("CHANGE_ACCS_PHOTO")[event.sender_id] == "yes":
        try:
            title = random.choice(["men", "women", "boy", "girl", "mens", "womens", "men persian", "women persian"])
            query = await client.inline_query("Pic", title)
            number = random.randint(0, 30)
            message = await query[number].click("me")
            pic = await message.download_media()
            file = await client.upload_file(pic)
            await client(functions.photos.UploadProfilePhotoRequest(file=file))
            os.remove(pic)
            await message.delete()
        except:
            pass
    await event.edit(f"**✅ Your Account Successfuly Edited!**\n\n**📱 Phone:** ( {flag} `{phone}` {flag} )")

@Callback(data="infoacc:(.*)")
async def infoacc(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    info = None
    try:
        info = await bot.client.get_entity(phone)
    except:
        contact = await bot.client(functions.contacts.ImportContactsRequest(contacts=[types.InputPhoneContact(client_id=random.randrange(-2**63, 2**63), phone=phone, first_name=phone, last_name="")]))
        if contact.users:
            info = contact.users[0]
    if info:
        username = f"@{info.username}" if info.username else "---"
        cont = "✅" if info.contact else "❌"
        strst = "%e %B %Y | %H:%M"
        if info.status:
            ustats = info.status.to_dict()["_"].replace("UserStatus", "")
            if ustats == "Offline":
                utime = info.status.was_online.strftime(strst)
                stats = ustats + " - " + utime
            else:
                stats = ustats
        else:
            stats = "---"
        userinfo = f"""**💠 Number Info:** ( {flag} `{phone}` {flag} )\n\n**• ID:** ( `{info.id}` )\n**• First Name:** ( `{info.first_name}` )\n**• Last Name:** ( `{info.last_name or "---"}` )\n**• Username :** ( `{username}` )\n**• Contact:** ( `{cont}` )\n\n**• Status:** ( `{stats}` )"""
        await event.reply(userinfo)
    else:
        await event.reply(f"**❌ Can't Get Information For Your Number:** ( {flag} `{phone}` {flag} )")

@Callback(data="delacc:(.*)")
async def delacc(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    allaccs = DB.get_key("USER_ACCS")
    del allaccs[event.sender_id][phone]
    DB.set_key("USER_ACCS", allaccs)
    await event.edit(f"**✅ This Account Successfuly Deleted From Accounts List!**\n\n**📱 Account Number:** ( {flag} `{phone}` {flag} )")
    await event.respond("**♻️ Main Menu:**", buttons=main_menu())

@Callback(data="logout:(.*)")
async def logout(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    await client.log_out()
    allaccs = DB.get_key("USER_ACCS")
    del allaccs[event.sender_id][phone]
    DB.set_key("USER_ACCS", allaccs)
    await event.edit(f"**🚫 Im LogOut From Your Account!**\n\n**📱 Account Number:** ( {flag} `{phone}` {flag} )")

@Callback(data="getcodes:(.*)")
async def getcodes(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    count = 1
    codes = f"**📋 Telegram Codes For Number:** ( {flag} `{phone}` {flag} )\n\n"
    async for mes in client.iter_messages(777000):
        if match:= re.search("(\\d*)\\.", mes.text):
            if match.group(1):
                codes += f"**• {count} -**  `{match.group(1)}`\n"
                count += 1
    await bot.send_message(event.chat_id, codes)

@Callback(data="resauths:(.*)")
async def getauths(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    accs = await client(functions.account.GetAuthorizationsRequest())
    all = len(accs.authorizations)
    cur = 0
    for acc in accs.authorizations:
        if not acc.current:
            await client(functions.account.ResetAuthorizationRequest(hash=acc.hash))
            cur += 1
    await event.answer(f"❗ {cur} Session From {all} Sessions Has Been Terminated!", alert=True)

@Callback(data="getauths:(.*)")
async def getauths(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    accs = await client(functions.account.GetAuthorizationsRequest())
    all = len(accs.authorizations)
    for acc in accs.authorizations:
        hash = acc.hash
        text = f"""
**💡 Account Authorization:**

**📱 Your Number:** ( {flag} `{phone}` {flag} )

**• Hash:** ( `{hash}` )
**• Device:** ( `{acc.device_model}` )
**• Platform:** ( `{acc.platform}` )
**• App Name:** ( `{acc.app_name}` )
**• App Version:** ( `{acc.app_version}` )
**• Country:** ( `{acc.country}` )
**• Official App:** ( `{"✅" if acc.official_app else "❌"}` )
**• This Bot App:** ( `{"✅" if acc.current else "❌"}` )
"""
        buttons = [[Button.inline("• Terminate •", data=f"terses:{phone}:{hash}")]]
        if hash == 0:
            buttons = None
            text += "\n\n__❗ This Is My Self And Connot Terminate This Session!__"
        await event.reply(text, buttons=buttons)

@Callback(data="terses:(.*):(.*)")
async def getauths(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    hash = int(event.pattern_match.group(2).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    client = await TClient(session, phone)
    if not client:
        buttons = [[Button.inline("❌ Delete ❌", data=f"delacc:{phone}")]]
        return await event.edit(f"**❗ This Account Is Out Of Reach Of The Robot!**\n\n__❔ Do You Want To Delete It From The List Of Accounts?__", buttons=buttons)
    await client.connect()
    accs = await client(functions.account.GetAuthorizationsRequest())
    for acc in accs.authorizations:
        if acc.hash == hash:
            await client(functions.account.ResetAuthorizationRequest(hash=acc.hash))
            await event.edit(f"**✅ This Session Has Been Terminated From Your Account:** ( {flag} `{phone}` {flag} )")
        else:
            await event.edit(f"**🚫 Can't Terminate This Session From Your Account:** ( {flag} `{phone}` {flag} )")

@Callback(data="sestel:(.*)")
async def getauths(event):
    phone = str(event.pattern_match.group(1).decode('utf-8'))
    flag = get_flag(phone)
    session = DB.get_key("USER_ACCS")[event.sender_id][phone]
    await event.reply(f"**📱 Phone:** ( {flag} `{phone}` {flag} )\n\n**💡 Telethon String Session:** ( `{session}` )")
