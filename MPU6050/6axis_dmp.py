import time
import math
import mpu6050

from blessed import Terminal


# Sensor initialization
mpu = mpu6050.MPU6050()
mpu.dmpInitialize()
mpu.setDMPEnabled(True)

# get expected DMP packet size for later comparison
packetSize = mpu.dmpGetFIFOPacketSize()

term = Terminal()

with term.fullscreen(), term.position():
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

            with term.position(0,1):
                print(ypr['yaw'] * 180 / math.pi),
            with term.position(0,2):
                print(ypr['pitch'] * 180 / math.pi),
            with term.position(0,3):
                print(ypr['roll'] * 180 / math.pi)

            # track FIFO count here in case there is > 1 packet available
            # (this lets us immediately read more without waiting for an interrupt)
            fifoCount -= packetSize
