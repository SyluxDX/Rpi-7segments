#!/usr/bin/env python
import sys
import json
import time
import random
import RPi.GPIO as GPIO


pinA = 3
pinB = 7
pinC = 19
pinD = 13
pinE = 11
pinF = 5
pinG = 21
pindot = 15
pin1 = 8
pin2 = 10
pin3 = 12
pin4 = 16

def setup_pins():
    """ setup raspberry pi GPIO """
    GPIO.setmode(GPIO.BOARD)
    # 7 segments
    GPIO.setup(pinA, GPIO.OUT)
    GPIO.setup(pinB, GPIO.OUT)
    GPIO.setup(pinC, GPIO.OUT)
    GPIO.setup(pinD, GPIO.OUT)
    GPIO.setup(pinE, GPIO.OUT)
    GPIO.setup(pinF, GPIO.OUT)
    GPIO.setup(pinG, GPIO.OUT)
    GPIO.setup(pindot, GPIO.OUT)
    # digit selectors
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    # deselect digits
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.HIGH)
    GPIO.output(pin3, GPIO.HIGH)
    GPIO.output(pin4, GPIO.HIGH)


def light_segments(segs):
    """ light up/out segments """
    pins = [pinA, pinB, pinC, pinD, pinE, pinF, pinG, pindot]
    for i, pin in enumerate(pins):
        if segs[i]:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

def light_number(number, dot=False):
    """ light segments to form number """
    for i in range(len(number)):
        x = number[i]
        if x in seg_number.keys():
            segs = list(seg_number[x])
            segs.append(dot)
            light_segments(segs)
            if i != len(number)-1:
                time.sleep(1)
        else:
            print('Unregonized number: {}'.format(x))

### Main
setup_pins()
freq = 0.005
with open('seg_light.json', 'r') as jfp:
    seg_number = json.load(jfp)

try:
    number = ('000' + str(random.randint(0, 9999)))[-4:]
    while True:
        for i, pin in enumerate([pin1, pin2, pin3, pin4]):
            GPIO.output(pin, GPIO.LOW)
            light_number(number[i])
            time.sleep(freq)
            light_segments([0,0,0,0,0,0,0,0])
            GPIO.output(pin, GPIO.HIGH)

except KeyboardInterrupt:
    pass
except Exception as exc:
    print(exc)
finally:
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    GPIO.output(pin3, GPIO.LOW)
    GPIO.output(pin4, GPIO.LOW)
    light_segments([0,0,0,0,0,0,0,0])
    print('\nCleanup GPIO')
    GPIO.cleanup()
