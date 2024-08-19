from telethon import TelegramClient
from telethon.sessions import StringSession
from manager.config import *
from traceback import format_exc

try:
    bot = TelegramClient(
        session=StringSession(BOT_SESSION),
        api_id=API_ID,
        api_hash=API_HASH,
    ).start()
except:
    error = format_exc()
    print(f"• Error: {error}")
    
try:
    client = TelegramClient(
        session=StringSession(SESSION),
        api_id=API_ID,
        api_hash=API_HASH,
    ).start()
except:
    error = format_exc()
    print(f"• Error: {error}")