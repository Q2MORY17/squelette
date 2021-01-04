# from flask import Flask, render_template, request, jsonify
from roboclaw import Roboclaw
import socket
from time import sleep
import config
import threading

rc = Roboclaw("COM3", 115200)
# rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()

testEvent = threading.Event()

class Motor():

    def __init__(self, address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready):
        self.address = address
        self.channel = channel
        self.pulses_min = pulses_min
        self.pulses_max = pulses_max
        self.pulses_unit = pulses_unit
        self.length = length
        self.unit = unit
        self.speed_pulses = speed_pulses
        self.speed_manual = speed_manual
        self.ready = ready
    
    def up(self):
        command = [rc.ForwardM1, rc.ForwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(command[self.channel])
    
    def down(self):
        command = [rc.BackwardM1, rc.BackwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(f"{command[self.channel]}")
            
    def stop(self):
        command = [rc.ForwardM1, rc.ForwardM2]
        try:
            command[self.channel](self.address, 0)
        except AttributeError:
            print(f"{command[self.channel]}")
  
    def position_absolute(self):
        """Immediate order, can be stopped at anytime"""
        command = [rc.SpeedAccelDeccelPositionM1, rc.SpeedAccelDeccelPositionM2]
        test_target = int(input("type in a destination between {} and {} {}: ".format(round(self.pulses_min/self.pulses_unit), round(self.pulses_max/self.pulses_unit), self.unit)))
        test_target_raw = (test_target * self.pulses_unit)
        if test_target_raw < self.pulses_min or test_target_raw > self.pulses_max:
            return('Bad input')
        else:
            try:
                command[self.channel](self.address, config.std_accel, self.speed_pulses, config.std_deccel, test_target_raw, 1)
            except AttributeError:
                print("test motor proceeds to {}".format(test_target_raw))
                print(command[self.channel], self.address, self.speed_pulses)
            return('target: {} {}'.format(test_target, self.unit))

    def position(self, position):
        command = [rc.SpeedAccelDeccelPositionM1, rc.SpeedAccelDeccelPositionM2]
        try:
            command[self.channel](self.address, config.std_accel, self.speed_pulses, config.std_deccel, position, 1)
        except AttributeError:
            print("Motor proceeds to {}".format(position))
            print(command[self.channel], self.address, self.speed_pulses)
        return('target: {} {}'.format(position/self.pulses_unit, self.unit))

    def buffer_arithmetic(self):
        command = [rc.SpeedM1, rc.SpeedM2]
        while(self.read_buffers()!=0x80):
            if config.stop == True:
                command[self.channel](self.address, 0)
                sleep(0.02)
                return

    def reset_enc(self):
        command = [rc.SetEncM1, rc.SetEncM2]
        return (command[self.channel](self.address, 0))

    def read_enc(self):
        command = [rc.ReadEncM1, rc.ReadEncM2]
        return (command[self.channel](self.address)[1])

    def read_speed(self):
        command = [rc.ReadSpeedM1, rc.ReadSpeedM2]
        return (command[self.channel](self.address)[self.channel + 1])

    def read_buffers(self):
        return (rc.ReadBuffers(self.address)[self.channel + 1])

    def position_setting(self):
        command = [rc.ReadM1PositionPID, rc.ReadM2PositionPID]
        return (command[self.channel](self.address))

    def velocity_setting(self):
        command = [rc.ReadM1VelocityPID, rc.ReadM2VelocityPID]
        return (command[self.channel](self.address))

    def read_temperature(self):
        command = [rc.ReadTemp, rc.ReadTemp2]
        return (command[self.channel](self.address)[1]/10)

    def read_current(self):
        return (rc.ReadCurrents(self.address)[self.channel + 1]/100)

    def read_voltage(self):
        return (rc.ReadMainBatteryVoltage(self.address)[1]/10)

    def status(self):
        # return (config.errorListing(rc.ReadError(self.address)[self.channel + 1]))
        return (rc.ReadError(self.address)) # removed the [1]        

class case_motors(Motor):

    def __init__(self, address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready, speed_pulses_open, speed_pulses_close):
        super().__init__(address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready)
        self.speed_pulses_open = speed_pulses_open
        self.speed_pulses_close = speed_pulses_close

    def up(self):
        try:
            rc.SpeedDistanceM1M2(self.address, self.speed_pulses_open, self.pulses_max, self.speed_pulses_open, self.pulses_max, 1)
        except AttributeError:
            print("Opening case")
            config.case_closed = False
        return config.case_closed, self.speed_pulses_open

    def down(self):
        try:
            rc.SpeedDistanceM1M2(self.address, self.speed_pulses_close, self.pulses_max, self.speed_pulses_close, self.pulses_max, 1)
        except AttributeError:
            print("Closing case")
            config.case_closed = True
        return config.case_closed, self.speed_pulses_close

    def stop(self):
        try:
            rc.SpeedDistanceM1M2(self.address, 0, 0, 0, 0, 1)
        except AttributeError:
            print("Stopped case")

class launch_motor(Motor):

    def __init__(self, address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready, speed_pulses_launch, mount, overshoot, acceleration, decceleration):
        super().__init__(address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready)
        self.speed_pulses_launch = speed_pulses_launch
        self.mount = mount
        self.overshoot = overshoot
        self.acceleration = acceleration
        self.decceleration = decceleration

    def up(self):
        command = [rc.SpeedM1, rc.SpeedM2]
        try:
            command[self.channel](self.address, self.speed_pulses)
        except AttributeError:
            print(command[self.channel])
    
    def down(self):
        command = [rc.SpeedM1, rc.SpeedM2]
        try:
            command[self.channel](self.address, self.speed_pulses)
        except AttributeError:
            print(command[self.channel])

    def launch_drone(self):
        try:
            rc.SpeedAccelDeccelPositionM1(self.address, self.acceleration, self.speed_pulses_launch, self.decceleration, self.overshoot, 1)
        except AttributeError:
            print("launchd")

class pitch_motor(Motor):

    def __inti__(self, address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready):
        super().__init__(address, channel, pulses_min, pulses_max, pulses_unit, length, unit, speed_pulses, speed_manual, ready)

    def up(self):
        command = [rc.BackwardM1, rc.BackwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(command[self.channel])
    
    def down(self):
        command = [rc.ForwardM1, rc.ForwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(f"{command[self.channel]}")

    def position_absolute(self):
        command = [rc.SpeedAccelDeccelPositionM1, rc.SpeedAccelDeccelPositionM2]
        test_target = int(input("type in a destination between {} and {} {}: ".format(round(self.pulses_min/self.pulses_unit), round(self.pulses_max/self.pulses_unit), self.unit)))
        test_target_raw = self.pulses_max - (test_target * self.pulses_unit)
        if test_target_raw < self.pulses_min or test_target_raw > self.pulses_max:
            return('Bad input')
        else:
            try:
                command[self.channel](self.address, config.std_accel, self.speed_pulses, config.std_deccel, test_target_raw, 1)
            except AttributeError:
                print("test motor proceeds to {}".format(test_target_raw))
                print(command[self.channel], self.address, self.speed_pulses)
            return('target: {} {}'.format(test_target, self.unit))
