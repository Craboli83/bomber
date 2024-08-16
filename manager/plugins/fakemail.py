from manager import bot
from telethon import Button
from manager.events import Cmd, Callback
from manager.database import DB
from fake_email import Email
import re

async def getemail():
    try:
        mail = Email().Mail()
    except:
        return None
    myemail = mail["mail"]
    if myemail.split("@")[-1] not in ["nowni.com"]:
        return mail
    else:
        return await getemail()
    
@Cmd(pattern="Fake Email 📨")
async def fakeemail(event):
    edit = await event.reply("`♻️ Please Wait . . .`")
    mail = await getemail()
    if not mail:
        return await event.edit(f"**❌ Your Email Is Not Created, Try Again!**")
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
        return await event.answer("❌ Telegram Code Is Not Received!", alert=True)
    msg = inbox["topic"]
    if inbox["from"] == "noreply@telegram.org" and re.search("Your Code \\- (\\d*)", msg):
        code = re.search("Your Code \\- (\\d*)", msg).group(1)
        text = f"**✅ Telegram Code Received!**\n\n**📬 Code:** ( `{code}` )"
        await event.reply(text)
    else:
        await event.answer("❌ Telegram Code Is Not Received!", alert=True)