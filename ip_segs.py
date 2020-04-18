#!/usr/bin/env python
import sys
import json
import time
import random
import threading
import subprocess
import RPi.GPIO as GPIO


class seven_segments(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Rpi Gpio
        self.pinA = 3
        self.pinB = 7
        self.pinC = 19
        self.pinD = 13
        self.pinE = 11
        self.pinF = 5
        self.pinG = 21
        self.pindot = 15
        self.pin1 = 8
        self.pin2 = 10
        self.pin3 = 12
        self.pin4 = 16
        # 7 segments numbers
        with open('seg_light_full.json', 'r') as jfp:
            self.seg_number = json.load(jfp)
        # thread variables
        self.freq = 0.005
        self.run_flag = True
        self.display = '    '

    def run(self):
        self.setup_pins()
        i = 0
        j = 0
        while self.run_flag:
            pins =[self.pin1, self.pin2, self.pin3, self.pin4]
            GPIO.output(pins[j], GPIO.LOW)
            if i+1 != len(self.display) and self.display[i+1] == '.':
                self.light_number(self.display[i], True)
                i += 1
            else:
                self.light_number(self.display[i])
            time.sleep(self.freq)
            self.light_segments([0,0,0,0,0,0,0,0])
            GPIO.output(pins[j], GPIO.HIGH)
            i += 1
            j += 1
            if j == len(pins):
                i = 0
                j = 0

        # clean up
        self.clean_pins()

    def setup_pins(self):
        """ setup raspberry pi GPIO """
        GPIO.setmode(GPIO.BOARD)
        # 7 segments
        GPIO.setup(self.pinA, GPIO.OUT)
        GPIO.setup(self.pinB, GPIO.OUT)
        GPIO.setup(self.pinC, GPIO.OUT)
        GPIO.setup(self.pinD, GPIO.OUT)
        GPIO.setup(self.pinE, GPIO.OUT)
        GPIO.setup(self.pinF, GPIO.OUT)
        GPIO.setup(self.pinG, GPIO.OUT)
        GPIO.setup(self.pindot, GPIO.OUT)
        # digit selectors
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.setup(self.pin3, GPIO.OUT)
        GPIO.setup(self.pin4, GPIO.OUT)
        # deselect digits
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.HIGH)
        GPIO.output(self.pin3, GPIO.HIGH)
        GPIO.output(self.pin4, GPIO.HIGH)

    def clean_pins(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)
        GPIO.output(self.pin4, GPIO.LOW)
        self.light_segments([0,0,0,0,0,0,0,0])

        print('\nCleanup GPIO')
        GPIO.cleanup()

    def light_segments(self, segs):
        """ light up/out segments """
        pins = [self.pinA, self.pinB, self.pinC, self.pinD, self.pinE, self.pinF, self.pinG, self.pindot]
        for i, pin in enumerate(pins):
            if segs[i]:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)

    def light_number(self, number, dot=False):
        """ light segments to form number """
        if number in self.seg_number.keys():
            segs = list(self.seg_number[number])
            segs.append(dot)
        else:
            segs = list(self.seg_number['e'])
            segs.append(False)
        self.light_segments(segs)

def get_ip():
    """ get ip"""
    rst = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
    rst = rst.stdout.decode().strip()
    if rst:
        return rst.split('.')
    # return local
    return ['127','0','0','1']

### Main
display = seven_segments()
ip = get_ip()
display.start()
try:
    i = 0
    while True:
        display.display = '{}.{}'.format(i+1, ip[i].rjust(3))
        i += 1
        if i == len(ip):
            i = 0
        time.sleep(1.5)
except KeyboardInterrupt:
    pass
except Exception as exc:
    print(exc)
finally:
    display.run_flag = False
    display.join()
