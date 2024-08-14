from . import bot, LOG_GROUP, CHANNELS
from telethon import events, functions, Button
from manager.database import DB
from traceback import format_exc
from manager.plugins import main_menu
import os
import sys
import re
import asyncio
import time
import telethon

async def is_spam(event):
    spams = DB.get_key("USER_SPAMS")
    ban = 60
    max = 5
    msgs = 8
    user_id = event.sender_id
    if user_id not in spams:
        spams[user_id] = {"next_time": int(time.time()) + max, "messages": 1, "banned": 0}
        usr = spams[user_id]
    else:
        usr = spams[user_id]
        usr["messages"] += 1
    if usr["banned"] >= int(time.time()):
        return True
    else:
        if usr["next_time"] >= int(time.time()):
            if usr["messages"] >= msgs:
                spams[user_id]["banned"] = time.time() + ban
                await event.reply(f"**🚫 You Are Spamed In Bot And Blocked, Try Again Later!**")
                await bot.send_message(LOG_GROUP, f"**#New_Spam**\n\n**🆔 UserID:** ( `{user_id}` )", buttons=[[Button.inline("Block 🚫", data=f"block:{event.sender_id}")]])
                return True
        else:
            spams[user_id]["messages"] = 1
            spams[user_id]["next_time"] = int(time.time()) + max
            return False

async def check_subs(userid):
    notsubs = {}
    for sub in CHANNELS:
        try:
            await bot(functions.channels.GetParticipantRequest(channel=sub, participant=userid))
        except:
            info = await bot.get_entity(sub)
            notsubs[sub] = info.title
    return notsubs

def Cmd(
    pattern=None,
    admin_only=False,
    **kwargs,
):

    cmds = DB.get_key("CMD_LIST") or []
    if pattern and pattern not in cmds:
        cmds.append(pattern)
        DB.set_key("CMD_LIST", cmds)

    def decorator(func):
        async def wrapper(event):

            if not event.is_private or event.out:
                return

            if admin_only and event.sender_id != bot.admin.id:
                return

            if not DB.get_key("BLOCK_USERS"):
                DB.set_key("BLOCK_USERS", [])
            
            if not event.sender_id == bot.admin.id and event.sender_id in DB.get_key("BLOCK_USERS"):
                return await bot.send_message(LOG_GROUP, f"**#New_Message_From_Spam_User**\n\n**🆔 UserID:** ( `{event.sender_id}` )", buttons=[[Button.inline("UnBlock ✅", data=f"unblock:{event.sender_id}")]])

            if not DB.get_key("USER_SPAMS"):
                DB.set_key("USER_SPAMS", {})

            if not event.sender_id == bot.admin.id and (await is_spam(event)):
                return

            if not event.sender_id == bot.admin.id:
                notsubs = await check_subs(event.sender_id)
                if notsubs:
                    info = await bot.get_entity(event.sender_id)
                    text = f"**👋 Hi {info.first_name}!**\n\n**🔶 Sorry, For Use From Bot Please Join To My Channels!**"
                    buttons = []
                    for nsub in notsubs:
                        buttons.append([Button.url(notsubs[nsub], nsub)])
                    buttons.append([Button.inline("• Joined ✅", data=f"checkjoin:{event.sender_id}")])
                    return await event.reply(text, buttons=buttons)

            if DB.get_key("BOT_STATUS") == "off" and not event.sender_id == bot.admin.id:
                return await event.reply("**❌ Sorry, The Bot Has Been DeActived!**\n\n__❗ Please Try Again Later!__")

            if not DB.get_key("BOT_STATUS"):
                DB.set_key("BOT_STATUS", "on")

            BOT_USERS = DB.get_key("BOT_USERS") or []
            if event.sender_id not in BOT_USERS:
                BOT_USERS.append(event.sender_id)
                DB.set_key("BOT_USERS", BOT_USERS)
                await bot.send_message(LOG_GROUP, f"**#New_User**\n\n**🆔 UserID:** ( `{event.sender_id}` )")

            USER_ACCS_COUNT = DB.get_key("USER_ACCS_COUNT") or {}
            if event.sender_id not in USER_ACCS_COUNT:                 
                USER_ACCS_COUNT.update({event.sender_id: 0})
                DB.set_key("USER_ACCS_COUNT", USER_ACCS_COUNT)

            USER_ACCS = DB.get_key("USER_ACCS") or {}
            if event.sender_id not in USER_ACCS:                 
                USER_ACCS.update({event.sender_id: {}})
                DB.set_key("USER_ACCS", USER_ACCS)

            CHANGE_ACCS_FNAME = DB.get_key("CHANGE_ACCS_FNAME") or {}
            if event.sender_id not in CHANGE_ACCS_FNAME:                 
                CHANGE_ACCS_FNAME.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_FNAME", CHANGE_ACCS_FNAME)

            CHANGE_ACCS_LNAME = DB.get_key("CHANGE_ACCS_LNAME") or {}
            if event.sender_id not in CHANGE_ACCS_LNAME:                 
                CHANGE_ACCS_LNAME.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_LNAME", CHANGE_ACCS_LNAME)

            CHANGE_ACCS_BIO = DB.get_key("CHANGE_ACCS_BIO") or {}
            if event.sender_id not in CHANGE_ACCS_BIO:                 
                CHANGE_ACCS_BIO.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_BIO", CHANGE_ACCS_BIO)

            CHANGE_ACCS_FLAG = DB.get_key("CHANGE_ACCS_FLAG") or {}
            if event.sender_id not in CHANGE_ACCS_FLAG:                 
                CHANGE_ACCS_FLAG.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_FLAG", CHANGE_ACCS_FLAG)

            CHANGE_ACCS_PHOTO = DB.get_key("CHANGE_ACCS_PHOTO") or {}
            if event.sender_id not in CHANGE_ACCS_PHOTO:                 
                CHANGE_ACCS_PHOTO.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_PHOTO", CHANGE_ACCS_PHOTO)

            try:
                await func(event)
            except asyncio.exceptions.TimeoutError:
                return await event.reply("**❌ Your Last Request Has Been Canceled, Try Again!**", buttons=main_menu(event))
            except telethon.errors.common.AlreadyInConversationError:
                return
            except:
                error = format_exc()
                await bot.send_message(LOG_GROUP, f"**#Error**\n\n**💡 Error:** ( `{error}` )")
        bot.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        bot.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        return wrapper
    return decorator

def Callback(
    data=None,
    **kwargs,
):
    if data:
        data = re.compile(data)
    def decorator(func):
        async def wrapper(event):
            try:
                await func(event)
            except:
                error = format_exc()
                await bot.send_message(LOG_GROUP, f"**#Error**\n\n**💡 Error:** ( `{error}` )")
        bot.add_event_handler(wrapper, events.CallbackQuery(data=data, **kwargs))
        return wrapper
    return decorator
