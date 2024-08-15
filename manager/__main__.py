from . import bot, LOG_GROUP, ADMIN_ID
from manager.functions import load_plugins

async def setup():
    print("• Installing Plugins ...")
    plugs, notplugs = load_plugins("manager/plugins/")
    print(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
    print(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
    send = await bot.send_message(LOG_GROUP, "**• Bot Has Been Start Now!**")
    text = "**✅ Loaded Plugins :**\n\n"
    for plug in plugs:
        text += f"`{plug}`\n"
    await send.reply(text)
    if notplugs:
        text = "**❌ Unloaded Plugins :**\n\n"
        ftext = ""
        for plug in notplugs:
            text += f"`{plug}`\n"
            ftext += f"{notplugs[plug]}\n\n"
        await send.reply(text)
        file = "NotPlugs.txt"
        open(file, "w").write(ftext)
        await send.reply(file=file)
    bot.me = await bot.get_me()
    bot.admin = await bot.get_entity(ADMIN_ID)
    print("• Setup Completed!")

bot.loop.run_until_complete(setup())
bot.run_until_disconnected()
