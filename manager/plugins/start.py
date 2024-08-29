from manager import bot
from manager.events import check_subs
from . import main_menu, manage_menu
from manager.events import Cmd, Callback
from . import main_menu
import re

@Cmd(pattern="/start")
async def start(event):
    info = await bot.get_entity(event.sender_id)
    await event.reply(f"**👋 Hi {info.first_name}!**\n**😘 Welcome To Acc Manager Robot!**\n\n**💡 Maker: @TheaBoLi**", buttons=main_menu())

@Cmd(pattern="Back 🔙")
async def back(event):
    await event.reply("**♻️ Backed To Main Menu!**", buttons=main_menu(event))