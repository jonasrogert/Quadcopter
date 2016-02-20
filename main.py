from time import sleep
from motor import motor
import atexit

motors = None


def main_loop():
    motors = [motor(40), motor(36), motor(32), motor(26)]

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
    print('die')

if __name__ == '__main__':
    main_loop()
