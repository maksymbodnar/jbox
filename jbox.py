# External module imports
import RPi.GPIO as GPIO
import time
import subprocess 
from time import sleep

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

movies = ['bandura/bandura.mp4', 'tech/mriya.mp4', 'music/music.mp4', 'secret/for_our_friends.mp4', 'a', 'b']

movieIndex = 0

videoPlayer = None
continueLoop = True 

def movie_run(index):
    global movieIndex
    global videoPlayer
    movieIndex = index
    videoPlayer.terminate()

def movie_loop(index):
    global videoPlayer
    if videoPlayer is not None and not videoPlayer.poll():
        videoPlayer.terminate()
    videoPlayer = subprocess.Popen(['/usr/bin/omxplayer.bin', '-o', 'hdmi', '/home/pi/movies/' + movies[index]], stdout=subprocess.PIPE)
    videoPlayer.wait()

def movie_set_1(channel):
    movie_run(1)

def movie_set_2(channel):
    movie_run(2)

def movie_set_3(channel):
    movie_run(3)

def movie_set_4(channel):
    movie_run(4)

def movie_set_5(channel):
    movie_run(5)

def movie_set_6(channel):
    movie_run(6)

GPIO.add_event_detect(btn1, GPIO.FALLING, callback=movie_set_1, bouncetime=300)
GPIO.add_event_detect(btn2, GPIO.FALLING, callback=movie_set_2, bouncetime=300)
GPIO.add_event_detect(btn3, GPIO.FALLING, callback=movie_set_3, bouncetime=300)
GPIO.add_event_detect(btn4, GPIO.FALLING, callback=movie_set_4, bouncetime=300)
GPIO.add_event_detect(btn5, GPIO.FALLING, callback=movie_set_5, bouncetime=300)
GPIO.add_event_detect(btn6, GPIO.FALLING, callback=movie_set_6, bouncetime=300)


while True:
    movieIndex += 1
    if movieIndex > 4:
        movieIndex = 0

    movie_loop(movieIndex)

