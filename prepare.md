```python
def prepare(self):
        self.case.up()
        for i in self.motors[:-1]:
            i.position(i.ready)
        """ self.pitch.position(self.pitch.ready)
        self.rotation.position(self.rotation.ready)
        self.lift.position(self.lift.ready)
        self._launch.position(self._launch.ready) """
```
# What am I trying to do here?<hr>
the purpose of '**prepare**' is to:
+ get the **column** to its '**ready**' position
+ get the **pitch** to its '**ready**' position
+ get the **rotation** to its '**ready**' position
+ get the **case open**
+ get the **drone holder** to it's '**min_pulse**' position

Is that right though? Should all this be supported by 'prepare'?<br>
Let 's make a table of positions and see what seems logical:

|**MOTOR**|**STANDBY**|**PREPARE**|**LAUNCH**|**MOUNT**|**STOP_ALL**|
| --- | --- | --- | --- | --- | --- |
|**PITCH**<br>slow|To pulses_min<br> position. **SWITCH**|To 'ready'|---|Horizontal|Event.clear()|
|**ROTATION**<br>best when<br>lift low|To 0 degrees<br>position|To 'ready'|---|To 180<br>degrees|Event.clear()
|**LIFT**<br>slowest|To pulses_min<br> position. **SWITCH**|To 'ready'|---|To 'pulses_min'|Stop|
|**LAUNCH**<br>draws high<br>current|To 'ready'<br> position|To 0|Check for 0<br>shoot forward|To 'Mount'|Event.clear()|
|**CASE**<br>no buffers<br>available|Close|Open|Check for<br>open|Open|Event.clear()|

Does this table make sense?<br>
<font color="FFFF00">The **questions** to ask ourselves are: how do I orchestrate the motion so that it looks cool, intuitive BUT manages large currents better? We know, from data and tests that the launcher motor demands a fair amount of current even at low speeds. Too much in fact to be used along with another motor if that can be helped. We know that the pitch, lift and rotation all use about 5A when in motion BUT they have a peak at start and stop so, as a motor stops and the other one starts, we could be experiencing very large peak currents which could be harmful for the system and/or the motors. The lift motor and the picth are the two slowest motors, taking about a minute to reach max position. Is it, in that case, right that the lift would extend to its maximum position for shoots? maybe there could be a lower value that works just as well</font>

<font color="FF2669">**SIDE NOTE:** when driving the motors from a position back to their origins, is it wise to use the position function? it offers us an optimization towards breaking before hitting a position, which is great for current managment BUT what if it is a little bit off? We ideally, would like the robot to always retract to its switches so we can get a clean base position. Could the answer be: </font>
```python
self.lift.position(self.lift.pulse_min) # Go to 0
self.lift.buffer_arithmetic # Hold until you get there
sleep(0.5) # Wait until stop position has settled
if self.lift.status <= 0x80000: # If the motor hasn't hit the switch
    self.lift.down() # Go down until you eventually hit the switch

"""
self.lift.down() will do the job but it runs at full speed, making more demands on the system.
"""
```
Otherwise, when it comes to the 'STANDBY' function, we could send all the motors to proceed backwards until they hit their switches, so it could be untied to their position. something like this: **BUT THEN I LOOSE CONTROL OVER THE BUFFERS, MEANING THAT i CAN NO LONGER ORCHESTRATE MOVEMENTS, UNLESS I SEND THE MOTOR TO COVER A DISTANCE LARGER THAN THEIR MAX POSITION... THEN I COULD USE THE BUFFERS AS I WISH...**
```python
# Absolute order:
self.pitch.down()
self.lift.down()
self.launch.down()
self.case.down()

# Distance order:
self.launch.full_down() # Call rc.SpeedDistanceM2(129, 2500, 25000, 1)
self.launch.buffer_arithmetic()
self.case.down()
self.lift.full_down() # Call rc.SpeedDistanceM2(128, 120, 20000, 1)
self.pitch.full_down() # Call rc.SpeedDistanceM1(128, 7000, 355000, 1)
self.pitch.buffer_arithmetic()
# self.rotation.position(0)
# self.rotation.buffer_arithmetic()
self.lift.buffer_arithmetic() # Wrap motor stops with lift timeline
self.launch.position(self.launch.ready) # Travel back to 8000
```