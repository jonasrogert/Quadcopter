import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

dc = 5

servos = [
    GPIO.PWM(40,50),
    GPIO.PWM(36,50),
    GPIO.PWM(32,50),
    GPIO.PWM(26,50)
]
for s in servos:
    s.start(10)
    time.sleep(5)
    print('Starting motor')
	

print('***Connect Battery & Press ENTER to start')
res = raw_input()
for s in servos:
    s.ChangeDutyCycle(5)
    time.sleep(5)
    print('changecuty cycle for motor')

print('***Press ENTER to start')
res = raw_input()

print ('increase > a | decrease > z | save Wh > n | set Wh > h|quit > 9')

cycling = True
try:
    while cycling:
        for s in servos:
	    s.ChangeDutyCycle(dc)
        res = raw_input()
        if res == 'a':
            dc = dc + 0.05
        if res == 'z':
            dc = dc - 0.05
        if res == 'h':
            mymotor.setWh()
        if res == '9':
            cycling = False
finally:
    # shut down cleanly
    for s in servos:
        s.stop()

    print ("dc var setting is: ")
    print (dc)


print('***Press ENTER to quit')
res = raw_input()
for s in servos:
    s.stop()
GPIO.cleanup()
