import subprocess
from datetime import datetime


c = True
while c:
    status = subprocess.Popen(["python", "/root/Telegram/alarm_bot/alarm_bot.py"], shell=False)

    status.wait()

    f = open('crash_time.txt', 'a')
    current_datetime = datetime.now()
    f.write(str(current_datetime) + '\n')
    f.close()


