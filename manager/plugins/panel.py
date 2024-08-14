from manager import bot, LOG_GROUP
from manager.events import Cmd, Callback
from telethon import Button
from . import main_menu, back_menu, panel_menu
from manager.database import DB
import re
import asyncio

@Cmd(pattern="Admin Panel 🔐", admin_only=True)
async def panel(event):
    await event.reply(f"**👋 Hi {bot.admin.first_name}!**\n\n**💠 Welcome To Admin Panel!**\n\n__❗ Use This Buttons!__", buttons=panel_menu())

@Callback(data="onoff")
async def change_status(event):
    status = "off" if DB.get_key("BOT_STATUS") == "on" else "on"
    DB.set_key("BOT_STATUS", status)
    await event.edit(buttons=panel_menu())
    status = "Actived ✅" if DB.get_key("BOT_STATUS") == "on" else "DeActived ❌"    
    await event.reply(f"**❗ The Bot Has Been Successfully {status}!**")

@Callback(data="sendtoall")
async def sendtoall(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**💡 Please Send Your Message To Be Sent For Bot Users:**", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    if response.text in DB.get_key("CMD_LIST"):
        return
    users = DB.get_key("BOT_USERS")
    count = 0
    for user in users:
        await bot.send_message(int(user), response)
        count += 1
        await asyncio.sleep(0.2)
    await response.reply(f"**✅ Your Message Successfuly Sended To** `{count}` **User From** `{len(users)}` **Users!**", buttons=main_menu(event))

@Callback(data="sendtouser")
async def sendtouser(event):
    users = DB.get_key("BOT_USERS")
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**💡 Please Send UserID For User:**", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    userid = int(response.text)
    if userid in DB.get_key("CMD_LIST"):
        return
    if userid not in users:
    	return await response.reply(f"**❌ The User** ( `{userid}` ) **Is Not Available!**", buttons=main_menu(event))
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply(f"**💡 Please Send Your Message To Be Sent For User:** ( `{userid}` )", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    if response.text in DB.get_key("CMD_LIST"):
        return
    await bot.send_message(userid, response)
    await response.reply(f"**✅ Your Message Successfuly Sended To User:** ( `{userid}` )", buttons=main_menu(event))

@Callback(data="getusers")
async def sendtoall(event):
    users = DB.get_key("BOT_USERS")
    acccount = DB.get_key("USER_ACCS_COUNT")
    if len(users) < 100:
        text = f"**📝 Bot Users:** ( `{len(users)}` )\n\n"
        count = 1
        for user in users:
            text += f"**{count} -** `{user}` ( `{acccount[user]}` )\n"
            count += 1
        await event.reply(text)
    else:
        text = f"📝 Bot Users: ( {len(users)} )\n\n"
        count = 1
        for user in users:
            text += f"{count} - {user} ( {acccount[user]} )\n"
            count += 1
        open("users.txt", "w").write(text)
        await event.reply("**📝 Bot Users!**", file="users.txt") 
