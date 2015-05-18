############ working
import os
from datetime import datetime
import time
import emails
from usernamedetails import Und
details = Und()
FRAMES = 36
FPS_IN = 6
FPS_OUT = 12
TIMEBETWEEN = 12
FILMLENGTH = float(FRAMES / FPS_IN)

date_now = datetime.now()
date_now_f = "{}-{}".format(date_now.day, date_now.month)

frameCount = 0
while frameCount < FRAMES:
    imageNumber = str(frameCount).zfill(7)
    os.system("raspistill -o image%s.jpg"%(imageNumber))
    frameCount += 1
    time.sleep(TIMEBETWEEN - 6) #Takes roughly 6 seconds to take a picture

message = emails.html(html="<p>Hi!<br>Here is your image...",
                       subject="Image",
                       mail_from=('Ian', details.email))
thefilename = "timelapse.mp4"
#message.attach(data=open(thefilename), filename="timelapse.mp4")

os.system("avconv -r %s -i image%s.jpg -r %s -vcodec libx264 -crf 20 -g 15 -vf crop=1296:729,scale=1280:720 timelapse%s.mp4"%(FPS_IN,'%7d',FPS_OUT,date_now_f))

message.attach(data=open(thefilename), filename="timelapse{}.mp4".format(date_now_f))
r = message.send(to=details.email, smtp={"host": "smtp.gmail.com", "port": 465, "ssl": True, "user": details.user, "password": details.password, "timeout": 5})
assert r.status_code == 250
