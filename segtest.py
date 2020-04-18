#!/usr/bin/env python
#import sys
import time
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

#Main
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinA, GPIO.OUT)
GPIO.setup(pinB, GPIO.OUT)
GPIO.setup(pinC, GPIO.OUT)
GPIO.setup(pinD, GPIO.OUT)
GPIO.setup(pinE, GPIO.OUT)
GPIO.setup(pinF, GPIO.OUT)
GPIO.setup(pinG, GPIO.OUT)
GPIO.setup(pindot, GPIO.OUT)

GPIO.setup(pin1, GPIO.OUT)

sel = [('A',pinA),('B',pinB),('C',pinC),('D',pinD),('E',pinE),('F',pinF),('G',pinG),('dot',pindot)]
#GPIO.output(pin1, GPIO.LOW)
for x in sel:
    print(x[0])
    GPIO.output(x[1], GPIO.HIGH)
    time.sleep(2)
    GPIO.output(x[1], GPIO.LOW)


GPIO.cleanup()
