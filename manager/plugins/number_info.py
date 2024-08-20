from manager import bot
from telethon import functions, types
from manager.events import Cmd
from manager.database import DB
from . import main_menu, back_menu
from manager.functions import get_flag
import datetime
import random

@Cmd(pattern="Info Number ℹ️")
async def infonumber(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**📜 Ok, Send Your Phone Number To Get Information For This:**\n\n__• Ex: +19307777777 __", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
        phone = response.text
    if phone in DB.get_key("CMD_LIST"):
        return
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
        ntime = datetime.datetime.now().strftime(strst)
        status = info.status.to_dict()["_"].replace("UserStatus", "")
        if info.status:
            ustats = info.status.to_dict()["_"].replace("UserStatus", "")
            if ustats == "Offline":
                utime = info.status.was_online.strftime(strst)
                stats = ustats + " - " + utime
            else:
                stats = ustats
        else:
            stats = "---"
        userinfo = f"""**💠 Number Info:** ( {flag} `{phone}` {flag} )\n\n**• ID:** ( `{info.id}` )\n**• First Name:** ( `{info.first_name}` )\n**• Last Name:** ( `{info.last_name or "---"}` )\n**• Username :** ( `{username}` )\n**• Contact:** ( `{cont}` )\n\n**• Status:** ( `{stats}` )\n\n**• Time:** ( `{ntime}` )"""
        await event.reply(userinfo)
    else:
        await event.reply(f"**❌ Cann't Get Information For Your Number:** ( {flag} `{phone}` {flag} )")
    await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))