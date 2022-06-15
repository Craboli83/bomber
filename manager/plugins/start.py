from manager import bot
from manager.events import Cmd
from . import main_menu

@Cmd(pattern="(?i)^\/start$")
async def start(event):
    info = await event.client.get_entity(event.sender_id)
    await event.reply(f"**👋 Hi {info.mention}!**\n**😘 Welcome To My Acc Manager Robot!**\n\n**💡 Maker: @{bot.admin.username}**", buttons=main_menu)

@Cmd(pattern="⬅️ Back")
async def start(event):
    sstep(event.sender_id, "free")
    await event.reply("**• Successfuly Backed To Home Page!**", buttons=main_menu)
