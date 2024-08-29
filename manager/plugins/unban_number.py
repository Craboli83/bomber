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
<p><a href="mailto:recover@telegram.org?subject=Banned phone number: {phone}&body=I'm trying to use my mobile phone number: {phone}%0ABut Telegram says it's banned. Please help.%0A%0AApp version: 11.0.0 (51439)%0AOS version: SDK {osver}%0ADevice Name: {device}%0ALocale: en%0AHello,%0AIt was a mistake, please release my account!%0AI need the account!">Send Email</a></p>
</font>

</body>
</html>
"""

def mobile():
    MOBILES = [
        "POCO X5 Pro 5G",
        "POCO X6 Pro 5G",
        "Redmi K70 Ultra 5G",
        "Xiaomi 15 Ultra 5G",
        "IPhone 15 Pro Max",
        "IPhone 14 Pro Max",
        "Samsung Galaxy S24 Ultra 5G",
        "Samsung Galaxy S23 Ultra 5G",
        "Samsung Galaxy S22 Ultra 5G",
    ]
    return random.choice(MOBILES)

@Cmd(pattern="/unban (.*)")
async def unbannumber(event):
    phone = str(event.pattern_match.group(1))
    flag = get_flag(phone)
    osver = random.randint(20, 90)
    htext = HTML.format(phone=phone.replace("+", ""), osver=osver, device=mobile())
    hfile = str(event.sender_id) + "-" + phone + ".html"
    open(hfile, "w").write(htext)
    text = f"**💯 UnBan Text Email File For:** ( {flag} `{phone}` {flag} )\n\n**💠 Open This On Your Browser And Click To Send Email!**"
    await event.reply(text, file=hfile)
    os.remove(hfile)