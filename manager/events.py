from . import bot, LOG_GROUP, CHANNELS
from telethon import events, functions, Button
from telethon.errors.common import AlreadyInConversationError
from manager.database import DB
from traceback import format_exc
from manager.plugins import main_menu
import re
import asyncio

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

    if pattern and pattern not in bot.COMMANDS:
        bot.COMMANDS.append(pattern)
    pattern = f"(?i)^\{pattern}$"

    def decorator(func):
        async def wrapper(event):

            if not event.is_private or event.out:
                return

            if admin_only and event.sender_id not in bot.admins:
                return
            
            if not DB.get_key("VIP_USERS"):
                DB.set_key("VIP_USERS", [])

            if event.sender_id not in bot.admins:
                vipusers = DB.get_key("VIP_USERS")
                if event.sender_id not in vipusers:
                    return await event.reply(f"**⛔️ This Bot Is Only For Vip Users!**\n\n**💠 Contact Creator For Vip Added!**\n\n**💡 Maker: @TheAboli**", buttons=None)

            if event.sender_id not in bot.admins:
                notsubs = await check_subs(event.sender_id)
                if notsubs:
                    info = await bot.get_entity(event.sender_id)
                    text = f"**👋 Hi {info.first_name}!**\n\n**🔶 Sorry, For Use From Bot Please Join To My Channels!**\n\n**✅ After Joining Start Again Bot!**"
                    buttons = []
                    for nsub in notsubs:
                        buttons.append([Button.url(notsubs[nsub], nsub)])
                    return await event.reply(text, buttons=buttons)

            if DB.get_key("BOT_STATUS") == "off" and event.sender_id not in bot.admins:
                return await event.reply("**❌ Sorry, The Bot Has Been DeActived!**\n\n__❗ Please Try Again Later!__")

            if not DB.get_key("BOT_STATUS"):
                DB.set_key("BOT_STATUS", "on")

            BOT_USERS = DB.get_key("BOT_USERS") or []
            if event.sender_id not in BOT_USERS:
                BOT_USERS.append(event.sender_id)
                DB.set_key("BOT_USERS", BOT_USERS)
                await bot.send_message(LOG_GROUP, f"**#New_User**\n\n**🆔 UserID:** ( `{event.sender_id}` )")

            USER_ACCS = DB.get_key("USER_ACCS") or {}
            if event.sender_id not in USER_ACCS:                 
                USER_ACCS.update({event.sender_id: {}})
                DB.set_key("USER_ACCS", USER_ACCS)

            CHANGE_ACCS_NAME = DB.get_key("CHANGE_ACCS_NAME") or {}
            if event.sender_id not in CHANGE_ACCS_NAME:                 
                CHANGE_ACCS_NAME.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_NAME", CHANGE_ACCS_NAME)

            CHANGE_ACCS_BIO = DB.get_key("CHANGE_ACCS_BIO") or {}
            if event.sender_id not in CHANGE_ACCS_BIO:                 
                CHANGE_ACCS_BIO.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_BIO", CHANGE_ACCS_BIO)

            CHANGE_ACCS_BIRTH = DB.get_key("CHANGE_ACCS_BIRTH") or {}
            if event.sender_id not in CHANGE_ACCS_BIRTH:                 
                CHANGE_ACCS_BIRTH.update({event.sender_id: "yes"})
                DB.set_key("CHANGE_ACCS_BIRTH", CHANGE_ACCS_BIRTH)

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
                await event.reply("**❌ Your Last Request Has Been Canceled, Try Again!**")
                return await event.respond("**♻️ Main Menu:**", buttons=main_menu())
            except AlreadyInConversationError:
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