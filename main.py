from time import sleep
from motor import Motor
import atexit
from sensors.mpu6050 import MPU6050

motors = None
mpu6050 = MPU6050()

def main_loop():
<<<<<<< HEAD
    motors = [Motor(40), Motor(36), Motor(32), Motor(26)]
=======
    # motors = [motor(40), motor(36), motor(32), motor(26)]
    motors = []
>>>>>>> 8bd35e52fd9a5900c62af323328ecdf5459cd064

    run = True
    try:
        while run is True:
            # check sensors
            # controls motors
            sleep(1)
            for m in motors:
                m.duty_cycle = m.duty_cycle+200
            print(motors[1].duty_cycle)

            gyro_data = mpu6050.get_gyro_scaled()
            accelerometer_data = mpu6050.get_accelerometer_scaled()
            rotation = mpu6050.get_rotation()

            print(gyro_data)
            print(accelerometer_data)
            print(rotation)
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
