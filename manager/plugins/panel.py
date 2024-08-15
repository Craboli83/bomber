from manager import bot, LOG_GROUP
from manager.events import Cmd, Callback
from telethon import Button
from . import main_menu, back_menu, panel_menu
from manager.database import DB
import re
import os
import asyncio

@Cmd(pattern="Admin Panel 🔐|\\/panel", admin_only=True)
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
async def getuserslist(event):
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

@Callback(data="getuaccs")
async def getuaccs(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**💡 Please Send UserID To Get User Accounts:**", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    userid = response.text
    if response.text in DB.get_key("CMD_LIST"):
        return
    accs = DB.get_key("USER_ACCS")[event.sender_id]
    if len(accs) == 0:
        return await event.reply(f"**📋 User** ( `{userid}` ) **Is Not Added Account To Bot!**", buttons=main_menu(event))
    text = f"💡 Count: ( {len(accs)} )\n\n"
    for acc in accs:
        session = accs[acc]
        text += f"{acc} - {session}\n"
    fname = str(userid) + ".txt"
    open(fname, "w").write(text)
    text = f"**📋 User** ( `{userid}` ) **Accounts List!**\n\n**💡 Count:** ( `{len(accs)}` )"
    await event.reply(text, file=fname, buttons=main_menu(event))
    os.remove(fname)
    
@Callback(data="addvip")
async def addvip(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**💡 Please Send UserID To Add In Vip Users:**", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    userid = int(response.text)
    if response.text in DB.get_key("CMD_LIST"):
        return
    vipusers = DB.get_key("VIP_USERS") or []
    if userid not in vipusers:
        vipusers.append(userid)
    DB.set_key("VIP_USERS", vipusers)
    await response.reply(f"**✅ User** ( `{userid}` ) **Was Added To Vip Users!**", buttons=main_menu(event))
    await bot.send_message(userid, "**✅ You Are Added To Vip Users By Admin!**", buttons=main_menu(event))

@Callback(data="delvip")
async def delvip(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**💡 Please Send UserID To Delete From Vip Users:**", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
    userid = int(response.text)
    if response.text in DB.get_key("CMD_LIST"):
        return
    vipusers = DB.get_key("VIP_USERS") or []
    if userid in vipusers:
        vipusers.remove(userid)
    DB.set_key("VIP_USERS", vipusers)
    await response.reply(f"**❌ User** ( `{userid}` ) **Was Deleted From Vip Users!**", buttons=main_menu(event))
    await bot.send_message(userid, "**❌ You Are Deleted From Vip Users By Admin!**", buttons=main_menu(event))