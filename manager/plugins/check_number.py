from manager import bot
from manager.events import Cmd
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

@Cmd(pattern="\\/unban (.*)")
async def myaccs(event):
    phone = str(event.pattern_match.group(1))
    osver = random.randint(20, 90)
    htext = HTML.format(phone=phone.replace("+", ""), osver=osver)
    hfile = str(event.sender_id) + "-" + phone + ".html"
    open(hfile, "w").write(htext)
    text = f"**• UnBan Text Email For:** ( `{phone}` )"
    await event.reply(text, file=hfile)
    os.remove(hfile)