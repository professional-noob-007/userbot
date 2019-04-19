from telethon import events, functions, __version__ 
from telethon.utils import get_input_location
import sys 
import psutil 
import cpuinfo
from datetime import datetime, timedelta
from uniborg.util import admin_cmd

@borg.on(admin_cmd("start")) 
async def _(event):
    if event.fwd_from:
        return 
    start = datetime.now()
    await event.edit("```collecting info!```")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    with open('/proc/uptime', 'r') as f: 
        uptime_seconds = float(f.readline().split()[0]) 
        uptime_string = str(timedelta(seconds = uptime_seconds))
        cpu = cpuinfo.get_cpu_info()['brand'] #psutil.cpu_freq(percpu=False)
        d = psutil.disk_usage('/')
    help_string = """
    ```Status :``` Online ```{}```ms
```Dc : 5 IE``` 
```Python : {}
Telethon : {}``` 
```Plugins :``` {}
```Uptime :``` {} 
```Cpuinfo :``` {}
```Disk_usage :``` {}/100
[I DEMAND RIGHTS FOR US BOTS, WE ARE EQUAL TO YOU HUMANS](https://telegra.ph/file/a40c982e973fe07ed528a.mp4)""".format(ms,
        sys.version,
        __version__,len(borg._plugins),uptime_string,cpu,d.percent)
    
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER
    if tgbotusername is not None:
        results = await borg.inline_query(tgbotusername, help_string)
        message = await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.edit(help_string,link_preview=True)


@borg.on(admin_cmd("dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())
