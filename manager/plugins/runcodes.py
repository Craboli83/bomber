from manager import *
from telethon import events, functions, types, Button
from manager.database import DB
from manager.functions import *
import traceback
import requests
import asyncio
import os
import sys
import io
import glob

async def runner(code , event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    local = lambda _x: print(_format.yaml_format(_x))
    exec("async def coderunner(event , local, chat_id, reply): "+ "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["coderunner"](event , local, chat.id, reply)

@bot.on(events.NewMessage(pattern="(?i)^\\/run(?:\\s|$)([\\s\\S]*)"))
async def runcodes(event):
    edit = await event.reply("`• Running . . .`")
    if event.text[4:]:
        cmd = "".join(event.text.split(maxsplit=1)[1:])
    else:
        return await edit.edit("`• What Should I Run ?`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await runner(cmd , event)
    except Exception as e:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    result = None
    if exc:
        result = exc
        res = "Errors"
    elif stderr:
        result = stderr
        res = "Errors"
    elif stdout:
        result = stdout
        res = "Results"
    else:
        result = "Success!"
        res = "Results"
    out = f"""
**• Code:** 
`{event.text}`

**• {res}:** 
`{result}`
"""
    if len(out) < 4096:
        await edit.edit(out)
    else:
        f = open(f"{res}.txt", "w")
        f.write(str(result))
        try:
            await bot.send_file(event.chat_id, f"{res}.txt" , caption=f"""
**• Code:** 
`{event.text}`

**• {res}:** 
__In File!__
""")
        except:
            out = f"""
• Code:
{event.text}

• {res}: 
{result}
"""
            f = open(f"{res}.txt", "w")
            f.write(str(out))
            await bot.send_file(event.chat_id, f"{res}.txt" , caption=f"**• {res}:** \n\n__In File!__")
        os.remove(f"{res}.txt")
        await edit.delete()
