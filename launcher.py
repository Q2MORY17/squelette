"""
launcher.py is a class that describes the actual launcher and its larger functions. Where more than one motor
is used at a time. Their __init__ is convoluted but it is done so to show the similarities in the setup.
this launcher can be updated with new motors or motors can be removed. 
all codes that contain 'test' are to be seen as test only motors that are not present on the actual launcher
but rather tested on in the lab.
"""

from motor import Motor, case_motors, launch_motor, pitch_motor
import config
from time import sleep
import threading

testEvent = threading.Event()

class Launcher():

    def __init__(self):
        self.pitch = pitch_motor(config.pitch['address'], config.pitch['channel'], config.pitch['pulses_min'], \
            config.pitch['pulses_max'], config.pitch['pulses_unit'], config.pitch['length'], config.pitch['unit'], config.pitch['speed_pulses'], \
                config.pitch['speed_manual'], config.pitch['ready'])

        self.rotation = Motor(config.rotation['address'], config.rotation['channel'], config.rotation['pulses_min'], \
            config.rotation['pulses_max'], config.rotation['pulses_unit'], config.rotation['length'], config.rotation['unit'], config.rotation['speed_pulses'], \
                config.rotation['speed_manual'], config.rotation['ready'])

        self.lift = Motor(config.lift['address'], config.lift['channel'], config.lift['pulses_min'], config.lift['pulses_max'], \
            config.lift['pulses_unit'], config.lift['length'], config.lift['unit'], config.lift['speed_pulses'], config.lift['speed_manual'], config.lift['ready'])

        self._launch = launch_motor(config.launch['address'], config.launch['channel'], config.launch['pulses_min'], \
            config.launch['pulses_max'], config.launch['pulses_unit'], config.launch['length'], config.launch['unit'], config.launch['speed_pulses'], \
                config.launch['speed_manual'], config.launch['ready'], config.launch['speed_pulses_launch'], config.launch['mount'], \
                    config.launch['overshoot'], config.launch['acceleration'], config.launch['decceleration'])

        self.case = case_motors(config.case['address'], config.case['channel'], config.case['pulses_min'], \
            config.case['pulses_max'], config.case['pulses_unit'], config.case['length'], config.case['unit'], config.case['speed_pulses'], \
                config.case['speed_manual'], config.case['ready'], config.case['speed_pulses_open'], config.case['speed_pulses_close'])

        self.test = Motor(config.test['address'], config.test['channel'], config.test['pulses_min'], \
            config.test['pulses_max'], config.test['pulses_unit'], config.test['length'], config.test['unit'], config.test['speed_pulses'], \
                config.test['speed_manual'], config.test['ready'])

        self.wheelL = Motor(config.wheelL['address'], config.wheelL['channel'], config.wheelL['pulses_min'], \
            config.wheelL['pulses_max'], config.wheelL['pulses_unit'], config.wheelL['length'], config.wheelL['unit'], config.wheelL['speed_pulses'], \
                config.wheelL['speed_manual'], config.wheelL['ready'])

        self.wheelR = Motor(config.wheelR['address'], config.wheelR['channel'], config.wheelR['pulses_min'], \
            config.wheelR['pulses_max'], config.wheelR['pulses_unit'], config.wheelR['length'], config.wheelR['unit'], config.wheelR['speed_pulses'], \
                config.wheelR['speed_manual'], config.wheelR['ready'])

        self.motors = [self.pitch, self.rotation, self.lift, self._launch, self.case]

    def stop_all(self):
        for i in self.motors:
            i.stop()
        sleep(0.02)

    def reset_encoders(self):
        """ Drives back all of the motors to reset them to 0 """
        # print(threading.currentThread().getName(), 'Live')
        pass

    def standby(self):
        self.pitch.position(self.pitch.pulses_min)
        self.lift.position(self.pitch.pulses_min)
        self._launch.position(self._launch.ready)

    def prepare(self):
        self.case.up()
        self.pitch.position(self.pitch.ready)
        self.rotation.position(self.rotation.ready)
        self.lift.position(self.lift.ready)
        self._launch.position(self._launch.pulses_min)

    def launch(self):
        """
        for this, the case MUST be open AND the ramp must be checked to be at its minimum
        """
        if config.case_closed == True:
            self.case.up()
            for i in range(5):
                print(5 - i)
                sleep(1)
        return self._launch.launch_drone()

    def mount(self):
        """
        for this the case MUST be opened also. A regular scenario would be to launch ->
        place launcher in standby -> reload when drone is returned later.
        """
        self.case.up()
        self.pitch.position(self.pitch.pulses_max)
        self.rotation.position(self.rotation.pulses_max)
        self.lift.position(self.lift.pulses_min)
        self._launch.position(self._launch.mount)

    def read_encoders(self):
        pass

    def lights(self):
        print(threading.currentThread().getName(), 'Lights live')

    def testBuf(self):
        while testEvent.wait():
            while testEvent.is_set():
                self.test.position(100000)
                print("I asked test to go to 100 000")
                self.test.buffer_arithmetic()
                sleep(0.02)
                print("I waited until I got there")
                print(self.test.read_enc())
                self.wheelL.position(6154)
                print("now, I asked the left wheel to go to 6154")
                self.wheelL.buffer_arithmetic()
                sleep(0.02)
                print("I have arrived")
                print(self.wheelL.read_enc())
                testEvent.clear()
                
                
    def stopTest(self):
        config.stop = True
        testEvent.clear()
        sleep(0.5)
        config.stop = False

    def simulation(self):
        self.test.down()
        while(self.test.status() < 0x400000):
            sleep(0.02)
        self.test.up()
        sleep(5)
        self.test.stop()
