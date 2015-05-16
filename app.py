import time 
from time import sleep, strftime, gmtime, localtime
import picamera 
import emails

message = emails.html(html="<p>Hi!<br>Here is your image...",
                       subject="Image",
                       mail_from=('Ian', 'ian.coates@gmail.com'))

counter = 0

with picamera.PiCamera() as camera:
    camera.start_preview()
    sleep(2)
    for thefilename in camera.capture_continuous('img{counter:03d}.jpg'):
        print(strftime("%H",localtime()))
        print('Captured %s' % thefilename)
        message.attach(data=open(thefilename), filename=thefilename)
	counter += 1
        if counter > 3:
            r = message.send(to='ian.coates@gmail.com', smtp={"host": "smtp.gmail.com", "port": 465, "ssl": True, "user": "ian.coates", "password": "Gm5Warbler", "timeout": 5})
            assert r.status_code == 250
            break   
        sleep(30) 
