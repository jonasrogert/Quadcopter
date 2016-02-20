# import RPi.GPIO as GPIO


class motor():
    servo = None
    _duty_cycle = 0

    def __init__(self, gpio):
        '''Initialization of motor
        '''
        # GPIO.setup(gpio, GPIO.OUT)
        # self.servo = GPIO.PWM(gpio, 50)
        # self.servo.start(10)
        # self.servo.ChangeDutyCycle(self._duty_cycle)
        pass

    def shutdown(self):
        # self.servo.stop()
        print('shuting down engine')
        pass

    @property
    def duty_cycle(self):
        return int(self._duty_cycle*1000)

    @duty_cycle.setter
    def duty_cycle(self, value):
        '''Setting motor duty cycle
        '''
        if value < 10000:
            self._duty_cycle = value/1000
            print(self._duty_cycle)

        else:
            self._duty_cycle = 10

        #self.servo.ChangeDutyCycle(self._duty_cycle)
