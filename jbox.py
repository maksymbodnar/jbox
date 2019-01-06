# External module imports
import RPi.GPIO as GPIO
import time
import subprocess 
import os
from time import sleep
import glob
import logging
import logging.handlers

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)


# Pin Definitons:
btn1 = 14 # Broadcom pin 18 (P1 pin 12)
btn2 = 15 # Broadcom pin 23 (P1 pin 16)
btn3 = 18 # Broadcom pin 17 (P1 pin 11)

btn4 = 16 # Broadcom pin 18 (P1 pin 12)
btn5 = 20 # Broadcom pin 23 (P1 pin 16)
btn6 = 21 # Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # LED pin set as output
GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # PWM pin set as output
GPIO.setup(btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # LED pin set as output
GPIO.setup(btn5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # PWM pin set as output
GPIO.setup(btn6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

dirs   = ['bandura', 'tech', 'music', 'usb', 'tour', 'history']
homeDir = '/home/pi/movies'

currentDir = 'bandura'

videoPlayer     = None
buttonPressed   = False
playList        = []

os.system('clear')

def get_dir(directory):
    global playList
    global homeDir
    curDir = os.path.join(homeDir, directory)
    print curDir
    my_logger.info(curDir)
    if os.path.isdir(curDir):
        playList = glob.glob(curDir + '/*.mp4')
        return playList

def movie_loop(path):
    global videoPlayer
    if videoPlayer is not None and videoPlayer.poll() is None:
        videoPlayer.terminate()
    videoPlayer = subprocess.Popen(['/usr/bin/omxplayer.bin', '-o', 'hdmi', path], stdout=subprocess.PIPE)
    videoPlayer.wait()

def change_dir(newDir):
    global currentDir
    global videoPlayer
    global buttonPressed
    buttonPressed = True
    currentDir = newDir
    if videoPlayer is not None and videoPlayer.poll() is None:
        videoPlayer.terminate()

def movie_set_1(channel):
    print 1
    change_dir('bandura')

def movie_set_2(channel):
    print 2
    change_dir('tour')

def movie_set_3(channel):
    print 3
    change_dir('tech')

def movie_set_4(channel):
    print 4
    change_dir('history')

def movie_set_5(channel):
    print 5
    change_dir('music')

def movie_set_6(channel):
    print 6
    change_dir('usb')

GPIO.add_event_detect(btn1, GPIO.FALLING, callback=movie_set_1, bouncetime=300)
GPIO.add_event_detect(btn2, GPIO.FALLING, callback=movie_set_2, bouncetime=300)
GPIO.add_event_detect(btn3, GPIO.FALLING, callback=movie_set_3, bouncetime=300)
GPIO.add_event_detect(btn4, GPIO.FALLING, callback=movie_set_4, bouncetime=300)
GPIO.add_event_detect(btn5, GPIO.FALLING, callback=movie_set_5, bouncetime=300)
GPIO.add_event_detect(btn6, GPIO.FALLING, callback=movie_set_6, bouncetime=300)


dirIndex = 0
while True:
    if buttonPressed:
        buttonPressed = False
    else:
        currentDir = dirs[dirIndex]
        dirIndex += 1
        if dirIndex > 5:
            dirIndex = 0
    playList = get_dir(currentDir)
    if playList:
        for fileName in playList:
            print fileName
            my_logger.info(fileName)
            try:
                movie_loop(fileName)
                if buttonPressed:
                    break
            except  Exception as e:
                logging.exception(e)
                
        

