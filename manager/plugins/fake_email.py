from manager import bot
from telethon import Button
from manager.events import Cmd, Callback
import requests
import json
import random
import time
import re

class Email:
	def __init__(self,session=None):
		self.session = session			
		self.request = requests.session()		
		
	def Mail(self):
		self.Buildsession =user = str("".join(random.choice("qwertyuiopasdfghjklzxcvbnm0987654321")for i in range(26)))		
		email = self.request.get(f"https://10minutemail.net/address.api.php?new=1&sessionid={self.Buildsession}&_=1661770438359").json()
		
		datajson={"mail":email["permalink"]["mail"],"session":email["session_id"]}		
		return datajson
	def inbox(self,loop=False):
		time.sleep(0.20) 		
		if self.session : 
			sessinbox = self.session	
		elif self.session ==None :
			sessinbox = self.Buildsession
		data = self.request.get(f"https://10minutemail.net/address.api.php?sessionid={sessinbox}&_=1661770438359").json()
		
		if len(data["mail_list"]) !=1:				 
			address =data["mail_list"][0]["subject"]
			id=data["mail_list"][0]["mail_id"]
			box = self.request.get(f"https://10minutemail.net//mail.api.php?mailid={id}&sessionid={sessinbox}").json()
			plain =box["plain_link"]
			datetime=["datetime"]
			to =box["to"]
			name=box["header_decode"]["replylist"][0]["name"]
			amli=box["header_decode"]["replylist"][0]["address"]
			datainbox ={"topic":address,"name":name,"from":amli,"to":to,"message":plain[0],"datetime":datetime}	
			return datainbox
										

async def getemail():
    try:
        mail = Email().Mail()
    except:
        return None
    myemail = mail["mail"]
    if myemail.split("@")[-1] in ["nowni.com"]:
        return mail
    else:
        return await getemail()
    
@Cmd(pattern="\\/Email")
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
        return await event.edit("**❌ Sorry, This Email Is Not Available Now!**")
    msg = inbox["topic"]
    if inbox["from"] == "noreply@telegram.org" and re.search("Your Code \\- (\\d*)", msg):
        code = re.search("Your Code \\- (\\d*)", msg).group(1)
        text = f"**✅ Telegram Code Received!**\n\n**📬 Code:** ( `{code}` )"
        await event.reply(text)
    else:
        await event.answer("❌ Telegram Code Is Not Received!", alert=True)
