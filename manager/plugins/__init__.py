from manager import bot
from telethon import Button
from manager.database import DB

def main_menu():
    menu = [
        [Button.text("Add Account 📥", resize=True)],
        [Button.text("Add Session 🔗", resize=True)],
        [Button.text("Accounts List 📋", resize=True), Button.text("Account Panel 🛠️", resize=True)],
        [Button.text("Account Settings ⚙️", resize=True), Button.text("My Info 📝", resize=True)],
    ]
    return menu

back_menu = [
    [Button.text("🔙", resize=True)],
]

def manage_menu(phone):
    menu = [
        [Button.inline("✏️ Edit Account ✏️", data=f"editacc:{phone}")],
        [Button.inline("❗ LogOut Bot ❗", data=f"logout:{phone}"), Button.inline("🚫 Delete 🚫", data=f"delacc:{phone}")],
        [Button.inline("❌ Reset Authorizations ❌", data=f"resauths:{phone}")],
        [Button.inline("🧾 Get Authorizations 🧾", data=f"getauths:{phone}"), Button.inline("📋 Get Telegram Codes 📋", data=f"getcodes:{phone}")],
        [Button.inline("📝 Get Telethon Session 📝", data=f"sestel:{phone}")],
    ]
    return menu

def panel_menu():
    status = "✅" if DB.get_key("BOT_STATUS") == "on" else "❌"
    menu = [
        [Button.inline(f"{status} Bot Status {status}", data="onoff")],
        [Button.inline("📝 Get Users 📝", data="getusers")],
        [Button.inline("📤 Send To All 📤", data="sendtoall"), Button.inline("📤 Send To User 📤", data="sendtouser")],
        [Button.inline("🧬 Get Accounts 🧬", data="getuaccs")],
        [Button.inline("✅ Add Vip 👑", data="addvip"), Button.inline("❌ Del Vip 👑", data="delvip")],
    ]
    return menu

def setting_menu(event):
    ch_name = "✅" if DB.get_key("CHANGE_ACCS_NAME")[event.sender_id] == "yes" else "❌"
    ch_bio = "✅" if DB.get_key("CHANGE_ACCS_BIO")[event.sender_id] == "yes" else "❌"
    ch_photo = "✅" if DB.get_key("CHANGE_ACCS_PHOTO")[event.sender_id] == "yes" else "❌"
    ch_birth = "✅" if DB.get_key("CHANGE_ACCS_BIRTH")[event.sender_id] == "yes" else "❌"
    ch_flag = "✅" if DB.get_key("CHANGE_ACCS_FLAG")[event.sender_id] == "yes" else "❌"
    menu = [
        [Button.inline(f"• Name {ch_name}", data=f"ch_name:{event.sender_id}"), Button.inline(f"• Bio {ch_bio}", data=f"ch_bio:{event.sender_id}")],
        [Button.inline(f"• Photo {ch_photo}", data=f"ch_photo:{event.sender_id}"), Button.inline(f"• Birthday {ch_birth}", data=f"ch_birth:{event.sender_id}")],
        [Button.inline(f"• Flag {ch_flag}", data=f"ch_flag:{event.sender_id}")],
    ]
    return menu

def list_menu(event):
    menu = [
        [Button.inline("• Check Accounts 🧮", data=f"checkaccs:{event.sender_id}"), Button.inline("• Get Sessions 📜", data=f"getaccs:{event.sender_id}")],
        [Button.inline("• Remove Deletes ⛔️", data=f"removedels:{event.sender_id}")]
    ]
    return menu