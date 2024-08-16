from manager import bot
from telethon import Button
from manager.events import Cmd, Callback
from manager.database import DB
from fake_email import Email
import re

@Cmd(pattern="Fake Email 📨")
async def fakeemail(event):
    edit = await event.reply("`♻️ Please Wait . . .`")
    mail = Email().Mail()
    myemail = mail["mail"]
    session = mail["session"]
    text = f"**#FakeEmail**\n\n**✅ Your Email Was Created!**\n\n**💡 Email:** ( `{myemail}` )"
    buttons = [[Button.inline("• Get Code 📬", data=f"getemailcode:{session}")]]
    await edit.edit(text, buttons=buttons)
        
@Callback(data="getemailcode:(.*)")
async def getemailcode(event):
    session = str(event.pattern_match.group(1).decode('utf-8'))
    inbox = Email(session).inbox()
    if not inbox:
        return await event.answer("❌ Nothing Email Is Not Received!", alert=True)
    msg = inbox["topic"]
    if match:=re.search("Your Code \\- (\\d*)", msg):
        code = match.group(1)
        text = f"**✅ Telegram Email Code Received!**\n\n**📬 Code:** ( `{code}` )"
        await event.reply(text)
    else:
        await event.answer("❌ Telegram Email Code Is Not Received!", alert=True)