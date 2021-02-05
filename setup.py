"""
setup.py is a one motor test area used in the early stage development of the larger code. 
"""

pitch_raw = {
    'address' : 128,
    'channel' : 0,
    'pulses_min' : 0,        # Minimum position on the encoder (raw) scale - horizontal (90)
    'pulses_max' : 355000,   # Maximum position on the encoder (raw) scale - vertical (0)
    'length' : 90.0,         # Physical measurement between min & max, 1 degree = 3944 pulses
    'pulses_unit' : 3944, # 3944 pulses
    'speed_pulses' : 7000,   # Top encoder (raw) speed - QPPS
    'speed_manual' : 127,    # PWM binary duty cucle from 0 to 127 representing 0% to 100% of 24V output
    'ready' : 65.0 
    }

pitch = [i for i in pitch_raw.values()]
print(pitch)

class motor():

    def __init__(self, address, channel, pulses_min, pulses_max, length, pulses_unit, speed_pulses, speed_manual, ready):
        self.address = address
        self.channel = channel
        self.pulses_min = pulses_min
        self.pulses_max = pulses_max
        self.length = length
        self.pulses_unit = pulses_unit
        self.speed_pulses = speed_pulses
        self.speed_manual = speed_manual
        self.ready = ready

class launcher():
    def __init__(self):
        self.pitch = motor(pitch_raw.values())
        self.lift = motor()
        self.rotation = motor()
        self.launch = motor()
        self.case = [motor(), motor()]

        self.motors = []
        self.motors.add(self.pitch, self.lift, self.rotation, self.launch, self.case)

lnchr = launcher()
print(lnchr.motors)
print(i for i in lnchr.pitcch)