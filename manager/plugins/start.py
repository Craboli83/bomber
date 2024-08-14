from manager import bot
from manager.events import check_subs
from . import main_menu, manage_menu
from manager.events import Cmd, Callback
from . import main_menu
import re

@Cmd(pattern="/start")
async def start(event):
    info = await bot.get_entity(event.sender_id)
    await event.reply(f"**👋 Hi {info.first_name}!**\n**😘 Welcome To Acc Manager Robot!**\n\n**💡 Maker: @{bot.admin.username}**", buttons=main_menu(event))

@Cmd(pattern="🔙")
async def back(event):
    await event.reply("**♻️ Im Backed To Main Menu!**", buttons=main_menu(event))

@Callback(data="checkjoin\:(.*)")
async def checkjoin(event):
    userid = int(event.pattern_match.group(1).decode('utf-8'))
    notsubs = check_subs(id)
    if not notsubs:
        info = await bot.get_entity(userid)
        await event.reply(f"**👋 Hi {info.first_name}!**\n**😘 Welcome To Acc Manager Robot!**\n\n**💡 Maker: @{bot.admin.username}**", buttons=main_menu(event))
        await event.delete()
    else:
        await event.answer("❌ You Are Not Joined To All Channels!", alert=True)
