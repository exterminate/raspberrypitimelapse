############ working
import os
import time
import emails
from usernamedetails import Und
details = Und()
FRAMES = 24
FPS_IN = 12
FPS_OUT = 12
TIMEBETWEEN = 12
FILMLENGTH = float(FRAMES / FPS_IN)


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

os.system("avconv -r %s -i image%s.jpg -r %s -vcodec libx264 -crf 20 -g 15 -vf crop=1296:729,scale=1280:720 timelapse.mp4"%(FPS_IN,'%7d',FPS_OUT))

message.attach(data=open(thefilename), filename="timelapse.mp4")
r = message.send(to=details.email, smtp={"host": "smtp.gmail.com", "port": 465, "ssl": True, "user": details.user, "password": details.password, "timeout": 5})
assert r.status_code == 250
