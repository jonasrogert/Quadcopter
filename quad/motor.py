import time
import threading

import RPi.GPIO as GPIO
from MPU6050 import axis_dmp

dc = 5
global_dc = 0
dc_stepping = 0.05
simulation = True

if simulation:
    import blessed
    term = blessed.Terminal()
    term.enter_fullscreen()


class InputThread(threading.Thread):

    global global_dc, dc_stepping

    def __init__(self):
        self.running = True
        threading.Thread.__init__(self)

    def run(self):
        while cycling:
            res = raw_input()
            if res == 'a':
                global_dc += dc_stepping
            if res == 'z':
                global_dc -= dc_stepping
            if res == '9':
                cycling = False

    def stop(self):
        self.running = False


def read_sensor_values():
    return axis_dmp.sensor_value


def calculate_dc_for_motor(motor, global_dc, sensor_values):
    adjustment = 0

    # if pitch < 0 => nose points towards the ground
    if sensor_values['pitch'] < 0:
        # We should move the north up, and the south down
        if motor in (0,1):
            adjustment += dc_stepping
        else:
            adjustment -= dc_stepping
    elif sensor_values['pitch'] > 0:
        # We should move the north down, and the south up
        if motor in (0,1):
            adjustment -= dc_stepping
        else:
            adjustment += dc_stepping

    # if roll < 0 => it leans to the left
    if sensor_values['roll'] < 0:
        # We should move the west up, and the east down
        if motor in (0,2):
            adjustment += dc_stepping
        else:
            adjustment -= dc_stepping
    elif sensor_values['roll'] > 0:
        # We should move the west down, and the east up
        if motor in (0,2):
            adjustment -= dc_stepping
        else:
            adjustment += dc_stepping

    new_dc = global_dc + adjustment

    if new_dc > 100:
        new_dc = 100
    elif new_dc < 0:
        new_dc = 0

    return new_dc


def main_loop():

    if not simulation:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        GPIO.setup(36, GPIO.OUT)
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)

        servos = [
            GPIO.PWM(40, 50),
            GPIO.PWM(36, 50),
            GPIO.PWM(32, 50),
            GPIO.PWM(26, 50)
        ]

    # TODO make sure motors are connected in the right order

    '''
    Motor mapping:
    01  (north)
    23  (south)
    '''


    print('Starting sensor thread, sleeping for stabilizing')
    axis_dmp.start_worker()
    time.sleep(5)
    print('Sensor thread started')

    print('Starting input thread')
    it = InputThread()
    it.start()

    if not simulation:
        for s in servos:
            s.start(1)
            time.sleep(1)
            print('Starting motor')

    print('***Connect Battery & Press ENTER to start')
    res = raw_input()

    print ('increase > a | decrease > z | save Wh > n | set Wh > h|quit > 9')

    cycling = True

    try:
        while cycling:
            # read sensor values
            sensor_values = read_sensor_values()
            for motor_index, s in servos.items():
                # calculate each motors value independently
                dc = calculate_dc_for_motor(motor_index, global_dc, sensor_values)

                if not simulation:
                    s.ChangeDutyCycle(dc)
                else:
                    if motor_index in (0,1):
                        y = 0
                        x = motor_index * 10
                    else:
                        y = 10
                        x = (motor_index - 2) * 10
                    with term.location(x,y):
                        print(dc)
    finally:
        # shut down cleanly
        if not simulation:
            for s in servos:
                s.stop()

        # stop input thread
        it.stop()

        print ("dc var setting is: ")
        print (global_dc)

    print('***Press ENTER to quit')
    res = raw_input()

    if not simulation:
        for s in servos:
            s.stop()
        GPIO.cleanup()
    else:
        term.exit_fullscreen()


if __name__ == "__main__":
    main_loop()
