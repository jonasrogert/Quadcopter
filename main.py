from time import sleep
from motor import Motor
import atexit

motors = None


def main_loop():
    motors = [Motor(40), Motor(36), Motor(32), Motor(26)]

    run = True
    try:
        while run is True:
            # check sensors
            # controls motors
            sleep(1)
            for m in motors:
                m.duty_cycle = m.duty_cycle+200
            print(motors[1].duty_cycle)
    finally:
        for m in motors:
            m.shutdown()
        print('bye')


@atexit.register
def shutdown():
    '''Shuting down
    '''
    print('die')
    for m in motors:
        if m:
            m.shutdown()

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('Shuting down from manual interupt')
