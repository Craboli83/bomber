from manager import bot
from manager.events import Cmd
from manager.database import DB
from manager.functions import TClient, get_flag
import re

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
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"**{count} {flag} -** `{acc}` ( `{status}` )\n"
            count += 1
        await event.reply(text)
    else:
        text = f"📋 Your Accounts List:\n💡 Count: ( {len(accs)} )\n\n"
        count = 1
        for acc in accs:
            flag = get_flag(acc)
            client = await TClient(session)
            status = "✅" if client else "❌"
            text += f"{count} {flag} - {acc} ( {status} )\n"
            count += 1
        open(f"{event.sender_id}.txt", "w").write(str(text))
        text = f"**📋 Your Accounts List:**\n\n**💡 Count:** ( `{len(accs)}` )"
        await event.reply(text, file=f"{event.sender_id}.txt")
