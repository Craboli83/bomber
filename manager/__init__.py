from telethon import TelegramClient
from telethon.sessions import StringSession
import sys

API_ID = 26909317
API_HASH = "bae2fc6f671b02f9bea0473ed369a95f"
BOT_SESSION = "1BJWap1wBuyC5s2IhBjW3T-mSwB48QThF8MqJj8DC5VHPu0QlSS4LCP7WXOEAswUhE6gpyFDVE0SQQcbu7QsyFx0Bt_xcRUig1uqXzp4DNoqSWfbR5hgD0dqwkHgKHwF7XFWEGLaQ0A9sTYuK5UXaPZomVxOrIbSiu5NIY0e06xQGcDLxvN3aCL-WWD96ecIrWwrDGAJsMOm12H5TYpKQFAQ1K1Er9VehtvroI_ohjMId54Elwr74niTo_9nzYMvXgf5lZ-CL1_ZT8H2dBk0fFz87KarPGGQBNvTBu9IiTdgpR34onl2sB2RErCq1uPKIQvn6WZAyBjryFN8RCWf2uBB5o9L412U="
LOG_GROUP = "GroupFidoTemp"
CHANNEL = "BackUpFidoTemp"
ADMIN_ID = 5889107490

try:
    bot = TelegramClient(
        session=StringSession(BOT_SESSION),
        api_id=API_ID,
        api_hash=API_HASH,
    ).start()
except Exception as e:
    print(f"• Error: {e}")
    sys.exit()
