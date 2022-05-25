from bomber import bot
from telethon import events
from bomber.database import DB

@bot.on(events.NewMessage(pattern="(?i)\/myinfo"))
async def start(event):
    info = await bot.get_entity(event.sender_id)
    datainfo = DB.get_key("BOT_USERS")
    await event.reply(f"""
**• Your Information:**

**• ID:** ( `{info.id}` )
**• Coins:** ( `{datainfo.[info.id]["coins"]}` )
**• Invites:** ( `{datainfo.[info.id]["invites"]}` )
**• Rank:** ( `{datainfo.[info.id]["rank"]}` )

**🆔 @MxBomber_Bot**
""")
