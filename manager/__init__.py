from telethon import TelegramClient
import sys

API_ID = 26909317
API_HASH = "bae2fc6f671b02f9bea0473ed369a95f"
BOT_TOKEN = "6069204518:AAEDwif5aO8hw6f8-axXY1R2Dd9H5va5RwY"
LOG_GROUP = "GroupFidoTemp"
CHANNEL = "BackUpFidoTemp"
ADMIN_ID = 5889107490

print("• Starting Bot . . .")

try:
    bot = TelegramClient(
        session="AccManagerBot",
        api_id=API_ID,
        api_hash=API_HASH,
    ).start(bot_token=BOT_TOKEN)
except Exception as e:
    print(f"• Error On Create Bot: {e}")
    sys.exit()
