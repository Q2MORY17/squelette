#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:09:01 2020

@author: pi
"""

def position_wait(self, position):
        """Waiting on buffers to complete, must be threaded to stop from the main script"""
        command = [rc.SpeedAccelDeccelPositionM1, rc.SpeedAccelDeccelPositionM2, rc.SpeedM1, rc.SpeedM2]
        while True:
            reset_event.wait()
            while reset_event.is_set():
                _buffers = (0, 0, 0)
                command[self.channel](self.address, config.std_accel, self.speed_pulses, config.std_deccel, position, 1)
                while(_buffers[1]!=0x80):
                    _buffers = rc.ReadBuffers(self.address)
                    if config.stop == True:
                        command[self.channel + 2](self.address, 0)
                        sleep(0.02)
                        print(_buffers)
                        reset_event.clear()
                        return
                sleep(0.02)
                print(test_enc_check()) # Function does not exist
                reset_event.clear()