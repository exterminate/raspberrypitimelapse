import os
import time
import emails
from usernamedetails import Und
details = Und()
FRAMES = 10
FPS_IN = 10
FPS_OUT = 24
TIMEBETWEEN = 6
FILMLENGTH = float(FRAMES / FPS_IN)


frameCount = 0
while frameCount < FRAMES:
    imageNumber = str(frameCount).zfill(7)
    os.system("raspistill -o image%s.jpg"%(imageNumber))
    frameCount += 1
    time.sleep(TIMEBETWEEN - 6) #Takes roughly 6 seconds to take a picture

os.system("avconv -r %s -i image%s.jpg -r %s -vcodec libx264 -crf 20 -g 15 -vf crop=2592:1458,scale=1280:720 timelapse.mp4"%(FPS_IN,'%7d',FPS_OUT))

thefilename = ""
message = emails.html(html="<p>Hi!<br>Here is your image...",
                       subject="Image",
                       mail_from=('Ian', details.email))
message.attach(data=open(thefilename), filename="timelapse.mp4")
r = message.send(to=details.email, smtp={"host": "smtp.gmail.com", "port": 465, "ssl": True, "user": details.user, "password": details.password, "timeout": 5})
assert r.status_code == 250
