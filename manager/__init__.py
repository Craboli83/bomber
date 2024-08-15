from telethon import TelegramClient
from telethon.sessions import StringSession
from manager.config import *
import sys

try:
    bot = TelegramClient(
        session=StringSession(BOT_SESSION),
        api_id=API_ID,
        api_hash=API_HASH,
    ).start()
except Exception as e:
    print(f"• Error: {e}")
    sys.exit()