from manager import bot
from manager.events import Cmd
from manager.database import DB
from . import main_menu, back_menu
from manager.functions import get_flag
import os
import random

HTML = """
<!DOCTYPE html>
<html>
<body>

<font size="+10">
<p><a href="mailto:recover@telegram.org?subject=Banned phone number: {phone}&body=I'm trying to use my mobile phone number: {phone}%0ABut Telegram says it's banned. Please help.%0A%0AApp version: 11.0.0 (51439)%0AOS version: SDK {osver}%0ADevice Name: Xiaomi22101320G%0ALocale: en%0AHello,%0AIt was a mistake, please release my account!%0AI need the account!">Send Email</a></p>
</font>

</body>
</html>
"""

@Cmd(pattern="UnBan Number ♻️")
async def unbannumber(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**🔆 Ok, Send Your Phone Number To Get UnBan Text Email For This:**\n\n__• Ex: +19307777777 __", buttons=back_menu)
        response = await conv.get_response(send.id, timeout=60)
        phone = response.text
    if phone in DB.get_key("CMD_LIST"):
        return
    flag = get_flag(phone)
    osver = random.randint(20, 90)
    htext = HTML.format(phone=phone.replace("+", ""), osver=osver)
    hfile = str(event.sender_id) + "-" + phone + ".html"
    open(hfile, "w").write(htext)
    text = f"**💯 UnBan Text Email File For:** ( {flag} `{phone}` {flag} )\n\n**💠 Open This On Your Browser And Click To Send Email!**"
    await event.reply(text, file=hfile)
    os.remove(hfile)
    await event.respond("**♻️ Main Menu:**", buttons=main_menu(event))