import math
import threading

from MPU6050 import mpu6050

global sensor_value


def start_worker():
    t = threading.Thread(target=sensor_worker)
    t.start()


def sensor_worker():
    # global sensor values dict
    global sensor_value
    # Sensor initialization
    mpu = mpu6050.MPU6050()
    mpu.dmpInitialize()
    mpu.setDMPEnabled(True)

    # get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize()

    while True:
        # Get INT_STATUS byte
        mpuIntStatus = mpu.getIntStatus()

        if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
            # get current FIFO count
            fifoCount = mpu.getFIFOCount()

            # check for overflow (this should never happen unless our code is too inefficient)
            if fifoCount == 1024:
                # reset so we can continue cleanly
                mpu.resetFIFO()
                print('FIFO overflow!')


            # wait for correct available data length, should be a VERY short wait
            fifoCount = mpu.getFIFOCount()
            while fifoCount < packetSize:
                fifoCount = mpu.getFIFOCount()

            result = mpu.getFIFOBytes(packetSize)
            q = mpu.dmpGetQuaternion(result)
            g = mpu.dmpGetGravity(q)
            ypr = mpu.dmpGetYawPitchRoll(q, g)

            sensor_value = {k: value*180/math.pi for k, value in ypr.items()}

            # track FIFO count here in case there is > 1 packet available
            # (this lets us immediately read more without waiting for an interrupt)
            fifoCount -= packetSize
