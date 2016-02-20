import time
from motor import Motor
import atexit
from sensors.sensor import sensor


motors = None
sensor = sensor()

def main_loop():
    # motors = [motor(40), motor(36), motor(32), motor(26)]
    motors = []
    sensor.start()

    run = True
    i = 0
    start = time.time()
    try:
        while run is True:

            i += 1
            # check sensors
            # controls motors
            for m in motors:
                m.duty_cycle = m.duty_cycle+200
                print(m.duty_cycle)


            print(sensor.roll, sensor.pitch, sensor.yaw)
            print(sensor.x_acc, sensor.y_acc, sensor.z_acc)
            print(sensor.r_rate, sensor.p_rate, sensor.y_rate)
            # print('Gyro', gyro_data)
            # print('Accelerometer', accelerometer_data)
            # print('Rotation', rotation)

            if i == 1000:
                end = time.time()
                seconds = end-start
                print(seconds)
                print('iterations', 1000/seconds)

                i = 0
                start = end
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
