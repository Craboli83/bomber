from manager import bot
from . import main_menu
from manager.events import Cmd, Callback
from manager.database import DB
from time import gmtime, strftime
import re

@Cmd(pattern="/start")
async def start(event):
    info = await bot.get_entity(event.sender_id)
    await event.reply(f"**👋 Hi {info.first_name}!**\n**😘 Welcome To Acc Manager Robot!**\n\n**💡 Maker: @TheaBoLi**", buttons=main_menu())

@Cmd(pattern="Back 🔙")
async def back(event):
    await event.reply("**♻️ Backed To Main Menu!**", buttons=main_menu())
    
@Cmd(pattern="My Info 📝")
async def info(event):
    info = await bot.get_entity(event.sender_id)
    acc_count = len(DB.get_key("USER_ACCS")[event.sender_id])
    date = strftime("%Y/%m/%d - %H:%M:%S", gmtime())
    text = f"""
**📝 Your Information:**

**✏️ Name:** ( `{info.first_name}` )
**🆔 UserID:** ( `{info.id}` )

**💡 Accounts Count:** ( `{acc_count}` )

__💠 {date}__
"""
    await event.reply(text)