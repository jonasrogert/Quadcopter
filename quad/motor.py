import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

dc = 5
global_dc = 0
dc_stepping = 0.05

# TODO make sure motors are connected in the right order

'''
Motor mapping:
01  (north)
23  (south)
'''
servos = [
    GPIO.PWM(40, 50),
    GPIO.PWM(36, 50),
    GPIO.PWM(32, 50),
    GPIO.PWM(26, 50)
]
for s in servos:
    s.start(1)
    time.sleep(1)
    print('Starting motor')

print('***Connect Battery & Press ENTER to start')
# res = raw_input()
# for s in servos:
#     s.ChangeDutyCycle(5)
#     time.sleep(5)
#     print('change duty cycle for motor')
#
# print('***Press ENTER to start')
res = raw_input()

print ('increase > a | decrease > z | save Wh > n | set Wh > h|quit > 9')

cycling = True


def read_sensor_values():
    pass


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


try:
    while cycling:
        # TODO read sensor values
        sensor_values = read_sensor_values()
        for motor_index, s in servos.items():
            # TODO calculate each motors value independently
            dc = calculate_dc_for_motor(motor_index, global_dc, sensor_values)
            s.ChangeDutyCycle(dc)
finally:
    # shut down cleanly
    for s in servos:
        s.stop()

    # TODO stop input thread

    print ("dc var setting is: ")
    print (global_dc)

print('***Press ENTER to quit')
res = raw_input()
for s in servos:
    s.stop()
GPIO.cleanup()


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