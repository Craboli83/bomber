from manager import bot
from manager.events import Callback
from manager.database import DB
import re

@Callback(data="block:(.*)")
async def block(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    blocks = DB.get_key("BLOCK_USERS")
    if not userid in blocks:
        blocks.append(userid)
        DB.set_key("BLOCK_USERS", blocks)
        await event.edit(f"**🚫 This User:** ( `{userid}` ) **Successfuly Blocked From Bot!**")
        await bot.send_message(userid, "**🚫 You Have Blocked From Bot, Don't Use From Bot!**")
    else:
        await event.edit(f"**🚫 This User** ( `{userid}` ) **Already Blocked From Bot!**")

@Callback(data="unblock:(.*)")
async def block(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    blocks = DB.get_key("BLOCK_USERS")
    if userid in blocks:
        blocks.remove(userid)
        DB.set_key("BLOCK_USERS", blocks)
        await event.edit(f"**✅ This User:** ( `{userid}` ) **Successfuly UnBlocked From Bot!**")
        await bot.send_message(userid, "**✅ You Have UnBlocked From Bot, Use This Bot!**")
    else:
        await event.edit(f"**✅ This User** ( `{userid}` ) **Already UnBlocked From Bot!**")
