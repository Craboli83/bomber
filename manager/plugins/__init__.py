from manager import bot
from telethon import Button
from manager.database import DB

def main_menu(event):
    menu = [
        [Button.text("Add Account 📥", resize=True)],
        [Button.text("Add Session 🔗", resize=True)],
        [Button.text("Account Settings ⚙️", resize=True), Button.text("Accounts List 📋", resize=True)],
        [Button.text("Account Panel 🛠️", resize=True), Button.text("My Info 📝", resize=True)],
        [Button.text("Guide 💡", resize=True), Button.text("Support 🧒", resize=True)],
    ]
    if event.sender_id == bot.admin.id:
        menu.append([Button.text("Admin Panel 🔐", resize=True)])
    return menu

back_menu = [
    [Button.text("🔙", resize=True)],
]

def manage_menu(phone):
    menu = [
        [Button.inline("❗ LogOut Bot ❗", data=f"logout:{phone}"), Button.inline("🚫 Delete 🚫", data=f"delacc:{phone}")],
        [Button.inline("❌ Reset Authorizations ❌", data=f"resauths:{phone}")],
        [Button.inline("🧾 Get Authorizations 🧾", data=f"getauths:{phone}"), Button.inline("📋 Get Telegram Codes 📋", data=f"getcodes:{phone}")],
        [Button.inline("📝 Get Telethon Session 📝", data=f"sestel:{phone}")],
    ]
    return menu

def panel_menu():
    status = "✅" if DB.get_key("BOT_STATUS") == "on" else "❌"
    sbtime = DB.get_key("SPAM_BAN_TIME")
    menu = [
        [Button.inline(f"{status} Bot Status {status}", data="onoff")],
        [Button.inline("📤 Send To All 📤", data="sendtoall"), Button.inline("📤 Send To User 📤", data="sendtouser")],
        [Button.inline("📝 Get Users 📝", data="getusers")],
        [Button.inline("✅ Add Vip 👑", data="addvip"), Button.inline("❌ Del Vip 👑", data="delvip")],
    ]
    return menu

def setting_menu(event):
    ch_fname = "✅" if DB.get_key("CHANGE_ACCS_FNAME")[event.sender_id] == "yes" else "❌"
    ch_lname = "✅" if DB.get_key("CHANGE_ACCS_LNAME")[event.sender_id] == "yes" else "❌"
    ch_bio = "✅" if DB.get_key("CHANGE_ACCS_BIO")[event.sender_id] == "yes" else "❌"
    ch_flag = "✅" if DB.get_key("CHANGE_ACCS_FLAG")[event.sender_id] == "yes" else "❌"
    ch_photo = "✅" if DB.get_key("CHANGE_ACCS_PHOTO")[event.sender_id] == "yes" else "❌"
    menu = [
        [Button.inline(f"{ch_fname} First Name {ch_fname}", data=f"ch_fname:{event.sender_id}"), Button.inline(f"{ch_lname} Last Name {ch_lname}", data=f"ch_lname:{event.sender_id}")],
        [Button.inline(f"{ch_bio} Bio {ch_bio}", data=f"ch_bio:{event.sender_id}"), Button.inline(f"{ch_flag} Flag {ch_flag}", data=f"ch_flag:{event.sender_id}")],
        [Button.inline(f"{ch_photo} Photo {ch_photo}", data=f"ch_photo:{event.sender_id}")],
    ]
    return menu
