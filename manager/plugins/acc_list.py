from manager import bot
from telethon import Button
from manager.events import Cmd, Callback
from manager.database import DB
from manager.functions import TClient, get_flag
import re
import os

@Cmd(pattern="Accounts List 📋")
async def myaccs(event):
    accs = DB.get_key("USER_ACCS")[event.sender_id]
    if len(accs) == 0:
        return await event.reply("**❗ You Account List Is Empty, Please Added Account To Bot!**")
    elif len(accs) < 100:
        text = f"**📋 Your Accounts List:**\n**💡 Count:** ( `{len(accs)}` )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            session = accs[acc]
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"**{count} - {flag}** `{acc}` ( `{status}` )\n"
            count += 1
        buttons = [[Button.inline("❌ No ❌", data=f"getaccs:{event.sender_id}")]]
        await event.reply(text, buttons=buttons)
    else:
        text = f"📋 Your Accounts List:\n💡 Count: ( {len(accs)} )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            session = accs[acc]
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"{count} - {flag} {acc} ( {status} )\n"
            count += 1
        open(f"{event.sender_id}.txt", "w").write(str(text))
        text = f"**📋 Your Accounts List:**\n\n**💡 Count:** ( `{len(accs)}` )"
        buttons = [[Button.inline("❌ No ❌", data=f"getaccs:{event.sender_id}")]]
        await event.reply(text, file=f"{event.sender_id}.txt", buttons=buttons)

@Callback(data="getaccs\:(.*)")
async def yesedit(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    accs = DB.get_key("USER_ACCS")[userid]
    text = f"💡 Count: ( {len(accs)} )\n\n"
    for acc in accs:
        session = accs[acc]
        text += f"{acc} - {status}\n"
    fname = str(userid) + ".txt"
    open(fname, "w").write(text)
    text = text = f"**📋 Your Accounts Sessions List!**\n\n**💡 Count:** ( `{len(accs)}` )"
    await event.reply(text, file=fname)
    os.remove(fname)
