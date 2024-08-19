from manager import bot
from telethon import Button
from . import list_menu
from manager.events import Cmd, Callback
from manager.database import DB
from manager.functions import TClient, get_flag
import re
import os

@Cmd(pattern="Accounts List 📋")
async def myaccs(event):
    accs = DB.get_key("USER_ACCS")[event.sender_id]
    edit = await event.reply("`♻️ Please Wait . . .`")
    if len(accs) == 0:
        return await edit.edit("**❗ You Account List Is Empty, Please Added Account To Bot!**")
    elif len(accs) < 100:
        text = f"**📋 Your Accounts List:**\n**💡 Count:** ( `{len(accs)}` )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            text += f"**{count} - {flag}** `{acc}`\n"
            count += 1
        await edit.reply(text, buttons=list_menu(event))
        await edit.delete()
    else:
        text = f"📋 Your Accounts List:\n💡 Count: ( {len(accs)} )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            text += f"{count} - {flag} {acc}\n"
            count += 1
        open(f"{event.sender_id}.txt", "w").write(str(text))
        text = f"**📋 Your Accounts List:**\n\n**💡 Count:** ( `{len(accs)}` )"
        await edit.reply(text, file=f"{event.sender_id}.txt", buttons=list_menu(event))
        await edit.delete()
        
@Callback(data="getaccs:(.*)")
async def getaccs(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    accs = DB.get_key("USER_ACCS")[userid]
    text = f"💡 Count: ( {len(accs)} )\n\n"
    for acc in accs:
        session = accs[acc]
        text += f"{acc} - {session}\n\n"
    fname = str(userid) + ".txt"
    open(fname, "w").write(text)
    text = f"**📋 Your Accounts Sessions List!**\n\n**💡 Count:** ( `{len(accs)}` )"
    await event.reply(text, file=fname)
    os.remove(fname)

@Callback(data="checkaccs:(.*)")
async def checkaccs(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    accs = DB.get_key("USER_ACCS")[userid]
    edit = await event.reply("`♻️ Please Wait . . .`")
    if len(accs) < 100:
        text = f"**📋 Your Accounts List With Status:**\n**💡 Count:** ( `{len(accs)}` )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            session = accs[acc]
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"**{count} - {flag}** `{acc}` ( `{status}` )\n"
            count += 1
        await edit.edit(text)
    else:
        text = f"📋 Your Accounts List With Status:\n💡 Count: ( {len(accs)} )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            session = accs[acc]
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"{count} - {flag} {acc} ( {status} )\n"
            count += 1
        open(f"{event.sender_id}.txt", "w").write(str(text))
        text = f"**📋 Your Accounts List With Status:**\n\n**💡 Count:** ( `{len(accs)}` )"
        await edit.reply(text, file=f"{event.sender_id}.txt")
        await edit.delete()
        
@Callback(data="removedels:(.*)")
async def removedels(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    allaccs = DB.get_key("USER_ACCS")
    edit = await event.reply("`♻️ Please Wait . . .`")
    text = f"**🚫 Your Removed Accounts List:**\n\n"
    count = 0
    for acc in allaccs[userid].copy():
        client = await TClient(allaccs[userid][acc])
        if not client:
            flag = get_flag(acc)
            allaccs[userid].pop(acc, None)
            count += 1
            text += f"**{count} - {flag}** `{acc}`\n"
    if count >= 1:
        accscount = DB.get_key("USER_ACCS_COUNT")
        accscount[userid] -= count
        DB.set_key("USER_ACCS_COUNT", accscount)
        DB.set_key("USER_ACCS", allaccs)
        await edit.edit(text)
    else:
        text = "**♨️ Nothing Account Is Not Deleted From Your Accounts!**"
        await edit.edit(text)