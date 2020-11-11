# SSRS launcher (Flask free) 

## config.py
all variables are set into dictionnaries for simplicity

| motor | pitch | rotation | lift | launch | case |
| --- | ---: | ---: | ---: | ---: | ---: |
|address|128|128|129|129|130|
|channel|0|1|0|1|NaN|
|puses_min|0|-316 666|0|0|0|
|pulses_max|355 000|316 666|19 000|23 000|6 000|
|length|90.0|120.0|130.0|111.0|5.0|
|pulses_unit|3 944|5 277|146|133|1 200|
|unit|degree(s)|degree(s)|centimeter(s)|centimeter(s)|centimeter(s)|
|speed_pulses|7 000|16 000|420|100 000|1 500|
|speed_pulses_slow|NaN|NaN|NaN|<font color="red">**2 500**</font>|NaN|
|speed_manual|127|15|75|20|NaN|
|ready <br>**PREPARE**<br>(default values)|65.0|5.0|15.0|8000|NaN|
|mount<br>**MOUNT**|NaN|NaN|NaN|17 000|NaN|
|top of case|NaN|NaN|NaN|<font color="red">**14 000**</font>|NaN|
|acceleration<br>**LAUNCH**|NaN|NaN|NaN|500 000|NaN|
|decceleration<br>**LAUNCH**|NaN|NaN|NaN|200 000|NaN|
<br>
There are some inconsistencies in the table, for example, the position function for the launcher requires the speed_pulses_slow value to travel at a safe speed. Why not set it as a speed_pulses and create a speed_pulses_fast for the launch?<br>Top of case is also strange, it should instead be pulses_max and top of case could become launch breakpoint or something. Thus making the prepare function unified over the whole spectrum.<br><br>

<style>
.hl-table-row tbody tr:hover {
  background: #eeeeee;
  font-weight: 600;
}
.hl-table-cell td:hover { /* th:hover also if you wish */
  background: #b5fffd;
}
</style>

<div class="ox-hugo-table hl-table-row sane-table">
<div></div>
<div class="ox-hugo-table hl-table-cell sane-table">
<div></div>

| motor | pitch | rotation | lift | launch | case |
| --- | ---: | ---: | ---: | ---: | ---: |
|address|128|128|129|129|130|
|channel<br><font color='blue'>(M1 = 0, M2 = 1)|0|1|0|1|NaN|
|puses_min|0|-316 666|0|0|0|
|pulses_max|355 000|316 666|19 000|<font color="blue">**14 000**</font>|6 000|
|<font color="blue">pulses_unit|<font color="blue">3 944|<font color="blue">5 277|<font color="blue">146|<font color="blue">133|<font color="blue">1 200|
|<font color="blue">length|<font color="blue">90.0|<font color="blue">120.0|<font color="blue">130.0|<font color="blue">111.0|<font color="blue">5.0|
|unit|degree(s)|degree(s)|centimeter(s)|centimeter(s)|centimeter(s)|
|speed_pulses<br>**QPPS**|7 000|16 000|420|<font color="blue">**2 500**</font>|1 500|
|<font color="blue">**speed_pulses_launch**</font>|NaN|NaN|NaN|<font color="blue">**100 000**</font>|NaN|
|speed_manual|127|15|75|20|NaN|
|ready <br>**PREPARE**<br>(default values)|65.0|5.0|15.0|8000|NaN|
|mount<br>**MOUNT**|NaN|NaN|NaN|17 000|NaN|
|<font color="blue">**overshoot**</font><br>**LAUNCH**|NaN|NaN|NaN|<font color="blue">**23 000**</font>|NaN|
|acceleration<br>**LAUNCH**|NaN|NaN|NaN|500 000|NaN|
|decceleration<br>**LAUNCH**|NaN|NaN|NaN|200 000|NaN|
<br>
</div>

## motor.py
motor class to create motor objects when setting up the launcher<br>
each methods relates to its own motor object
some issues:
+ the position function needs to be customized for the pitch and the launcher (subclasses)
    + *pitch*: have to reverse the counts to come to a sensible position
    + *launch*: max argument needs to be lower than the pulses_max <br>Speed needs to be updated to slow motion

## launcher.py
launcher object, does the moves that require several motors
+ reset encoders
+ stop all
+ prepare
    + prepare should ask for positions
+ standby
+ mount

## main.py
not primed as of yet

## <font color="FFFF00">**notes**</font><hr>
**[ LOG entry 28-10-20 ]**: I successfully built digital motor. The motors are built to count up and down encodre values in parallel to the code, feeding back actual positional value for simulation modes. Some more work needs to go into incorporating those in some simulation interface but having access to such motors (which are built to move at the actual launcher speed) opens up world of opportunity when thinking about transportability. Being able to test/tune the code with actual data feedback BUT without the need for the launcher is a great advantage. They also open doors for realtime launcher visualization. by this, I mean a CAD tool could be maipulated by the python script, giving us realtime visualization feedback on the launcher positionning.


**[ LOG entry 29-10-20 ]**: The threaded/buffered events for launcher motions of the launcher were successful today. I successfully launched a motion and could stop it anytime I liked. It seems the way to do it was to trap the more complex motions (or motions that are dependant on buffers) in an ```Event()``` routine. This works great with one motor but I can already see how it may be a problem with several (or not. but I can only attest to that with further testing).
+ problem #1: All buffers run through one and the same function and update the same variable _buffer to keep track of themselves. This might not be a problem as the calls come from two different objects. it may therefore define instances of _buffer in different parts of the memory. I could check on the id allocation and see that they are all different ```id(_buffer)``` or ```hex(id(_buffer))``` (hex providing a C++ style address but it is left to be proven that id() returns the actual position of a variable in the memory.). Otherwise, I could solve this issue one of two ways:
  + I could create a vector (array/list) that could hold all of the buffer variables. I could initiate it by using the addresses and the channels to place them, as such (I will use lists here):<br>I want a list with 6 slots (0, 1, 2, 3, 4, 5), I have three addresses (128, 129, 130) and two channels per address (0, 1).<br>Using such a vector would enable me to control which position of the vector are allowed to be interacted with and when but as it would be lodged in the config file instead of the motor classes, it might not resolve the problem at all.
  
|address|channel|arithmetic|list|
|--|--|--|--|
|<font color="00FFFF">128|<font color="FF00FF">0|(<font color="00FFFF">128</font> - 128) * 2 + <font color="FF00FF">0|0|
|<font color="00FFFF">128|<font color="FF00FF">1|(<font color="00FFFF">128</font> - 128) * 2 + <font color="FF00FF">1|1|
|<font color="00FFFF">129|<font color="FF00FF">0|(<font color="00FFFF">129</font> - 128) * 2 + <font color="FF00FF">0|2|
|<font color="00FFFF">129|<font color="FF00FF">1|(<font color="00FFFF">129</font> - 128) * 2 + <font color="FF00FF">1|3|
|<font color="00FFFF">130|<font color="FF00FF">0|(<font color="00FFFF">130</font> - 128) * 2 + <font color="FF00FF">0|4|
|<font color="00FFFF">130|<font color="FF00FF">1|(<font color="00FFFF">130</font> - 128) * 2 + <font color="FF00FF">1|5|
|||||
 + The other way to solve the issue is to remove the _buffer variable all together and instead get info straight from the source and by this, I mean:
### old code:
```python
def buffer_arithmetic(self):
  command = [rc.SpeedM1, rc.SpeedM2] # uses self.channel for order
  _buffers = (0, 0, 0)
  while(_buffers[self.channel + 1] != 0x80): # 0x80 == 128
    _buffers = rc.ReadBuffers(self.address)
    if config.stop == True:
      command[self.channel](self.address, 0) # STOP motor
      sleep(0.02)
      print(_buffers)
      return
```
### other (new) code:
```python
def buffer_arithmetic(self):
  command = [rc.SpeedM1, rc.SpeedM2] # uses self.channel for order
  while(rc.ReadBuffers(self.address)[self.channel + 1] != 128): 
    if config.stop == True:
      command[self.channel](self.address, 0)
      sleep(0.02)
      return
```
This would have the benefit of only retrieving a value from the roboclaw and comparing it with a static value saving extra memory space. I would say however that it might mean that several read orders could be placed on the roboclaw, potentially creating a bottle neck. bottle neck = delays. To be tested...

The other issue is an issue of priority and locks. How can I orchestrate the launcher's motion while the column (launcher's slowest attribute) extends in the background.

**I have now** rewritten the code above, loosing the _buffer variable and tested it to work. I also made use of another function that I had already made available and therefore the code looks like this:

```python
def buffer_arithmetic(self):
  command = [rc.SpeedM1, rc.SpeedM2]
  while(self.read_buffers() != 128): 
    if config.stop == True:
      command[self.channel](self.address, 0)
      sleep(0.02)
      return
```
## USING STATUS TO FIND WHEN THE MOTOR IS IN HOME POSITION
One of the features that I ahve long wanted to make use of, is a way for the system to know that it has hit **HOME**. I want this to work for two reasons:
+ Resetting the encoders to 0 (and not some trash values) would benefit greatly from being able to make use of a **HOME** indicator. _you're at home? reset your encoder to 0_
+ Using the launcher belt is tricky and position can vary a bit due to the drone's weight. So something that should be at a position of 60 cm (8000 pulses) could in fact be at 52 cm. so when I as the system to go back to 0 from 60 cm (which is in fact 52 cm), the positions do not add up. When launching the drone though it is very important that the positions be correct, from position 0 to end position. here is the sequence that I would like to see at launch:<br><br>GO BACKWARDS (without looking for a position or distance)<br>STOP WHEN YOU HIT THE SWITCH<br>RECOGNIZE THAT IT IS YOUR HOME<br>wait an appropriate amount of time<br>LAUNCH

Today, I was able to design a code for the test motor performing exactly the described launching sequence. This successful use of **HOME** revives an old idea of mine whereby warning and errors at a roboclaw level could be communicated to the user in normal language mkaing use of a python dictionnary I had already written. I just have to find it .... 

I think it got erased. Here goes:

```python
errorListing = {
  0x000000: 'Normal',
  0x000001: 'E-Stop',
  0x000002: 'Temperature Error',
  0x000004: 'Temperature 2 Error',
  0x000008: 'Main Voltage High Error',
  0x000010: 'Logic Voltage High Error',
  0x000020: 'Logic Voltage Low Error',
  0x000040: 'M1 Driver Fault Error',
  0x000080: 'M2 Driver Fault Error',
  0x000100: 'M1 Speed Error',
  0x000200: 'M2 Speed Error',
  0x000400: 'M1 Position Error',
  0x000800: 'M2 Position Error ',
  0x001000: 'M1 Current Error',
  0x002000: 'M2 Current Error',
  0x010000: 'M1 Over Current Warning',
  0x020000: 'M2 Over Current Warning',
  0x040000: 'Main Voltage High Warning',
  0x080000: 'Main Voltage Low Warning',
  0x100000: 'Temperature Warning',
  0x200000: 'Temperature 2 Warning',
  0x400000: 'S4 Signal Triggered',
  0x800000: 'S5 Signal Triggered',
  0x01000000: 'Speed Error Limit Warning',
  0x02000000: 'Position Error Limit Warning'
}

```
### output:
```python
>>> errorListing[0x800000]
'S5 Signal Triggered'
>>> errorListing[2]
'Temperature Error'
>>> errorListing[4194304]
'S4 Signal Triggered'
>>> errorListing[0x400000]
'S4 Signal Triggered'
```
Now we have a way to process any errors in the system and track Over Currents as being one of the most worrysome issues.

**Now I wonder** if the set up could have an overriding stop button set on S3. like an interconnected, hardwired stop button, that could be physical and/or digital by way of Raspberry Pi. the idea is connect all 3 roboclaws to this and if pressed, all motors stop. This might be overkill but it would provide a new layer of security should a motor fail or the internet platform fail...

**Still unresolved** is the issue of the positionning. But now that I have made some progress in my use of switches, I am confident that this will come to be solved given a little bit more time.t

## **To try**<hr>
+ Set two motors in motion using ION MOTION STUDIO and see if 
  1. You can do that 
  2. If you can STOP ALL using their STOP ALL button. in which case I will have to reach out to them and see if they are willing to reveal some trade secrets.
+ Carry on the work with the GameController (but as a side gig as the code is taking shape nicely without it currently. This could be a nice addition towards the end)
+ Try and see what can be done with Blender and OpenCV (also side gig)
+ Integrate the status dictionnary in the code for feedback
  ```python
  def errorInterpreter(self):
    """ Something like that """
    return errorListing[rc.ReadError(self.address)[1]]
  ```
+ Orchestrate the first complex motion (remember, to do that you need a buffer activation device. maybe with ```Timer()``` or something. But, this might have to wait until I have a second motor available... unless I can figure out how to plug in the digital motors (They currently do not have any buffer information in their code))
  ```python
  def prepare(self):
    """ Obviously, this would have to be set as an event """
    self.lift.position(ready)
    for i in self.motor: 
      # Not true because I would have to remove lift and launch.
      i.position(ready)
      i.buffer_arithmetic()
  ```
+ See if a motion detector can be implemented -> This would make all the work with lights much easier than what it is nowadays. This might however, need to be tried with a single LED while testing and development as the light routine using the 'ring' or 'strip' is a bit more involved and requires more libraries that just the RPi GPIOs.
  ```python
  def lightUpdate(self):
    """ Obviously, this would have to be a thread
        It would probably have to be set outside of the class
        but in the motor.py
        That way it would act as a global watcher. """
    # switch white light on globally - not here!
    while(1):
      while rc.ReadSpeedM1(128) or rc.ReadSpeedM2(128):
        # light a LED..
        sleep(0.5)
      # switch off LED
      sleep(0.5)
  ```

  **[ LOG entry 10-11-20 ]**: I have spent most of my day today trying and failing to set up another motor on a roboclaw with encoder capacities. It did not work for some reason that I can not fathom as the circuitry is correct and was double checked for connection with a multimeter. I also used an oscilloscope to check on the encoder signals and it seems the signals are there but weak and noisy. **I NEED A FUNCTIONNING MOTOR WITH ENCODERS TO MOVE FORWARD WRITING CODES**

  This inadvertably got me thinking about solutions that would not depend on encoders, but rather on time or absolute positions (switches). it is important to remember that I have discovered that the ANT-52 do not have any internal limiters so there is **NO** absolute max and absolute min positions. Rather, the encoder will start to count up bogus values that are probably generated from its own magnetism/noise. (revision: I think there might be limiters in the ANT-52 but it is very weak and testing has shown runaway encoder values on several occasion pointing to a problem of reliability).

  **WHAT DOES THIS MEAN? WHAT DO I LOSE BYPASSING ENCODERS?** 
  + I lose all position functions as I can only use **PWM**<br>This is obviously a great loss as it means that I can no longer get feedback as to **'where'** the motor is. This also means that the entire logics side of the roboclaw is useless and might just as well be uncoupled. <br>The discussions to be had are: Is this really a problem? should we install a max/min switch combo and say bye-bye to all positional values? This would mean always shooting in the same angle but also it would mean the angle of reach to re-install the drone would be inpacted.<br>The motor always moves with the same speed so should we create a timer for it? that way all angle can be reached according to the timer? This obviously presents another issue where displacement can be slower due to wind when the launcher is outdoors and therefore the time to objective ration might be impacted negatively.
  + I would no longer **have access to buffers**. This is a problem for orchestrated motions. although the ANT-52 only draws 5A with max load, it is still a problem that I can not get feedback on when it is in motion and not in motion.

  **POINT IS. I HAVE TO TRY AND FIX THE ENCODER ISSUE IF I CAN. THAT'LL BE THE MISSION TOMORROW.**
  
  Plan of the day:
  1. Set up the _new_ ANT-52 on BasicMicro and test it properly. Maybe get the source from the launcher to run experiments without stops.
  2. Decide wether or not it is good to keep ( _although it is unclear if it can be returned at all_ ) and write an email to Peter.
      + **if it is good to keep**: get all info from it and try out the lnchr.pitch.position(x) to confirm results and a potential integration in the robot.
      + **if it is not good to keep**: I will have to build a **new, fault free** low pass filter. for that I will need to solder and the iron at SSRS is busted but I have plans to go to somewhere where I can use one on friday. Redisgning one will not be an issue but I might need to get a hold of some raw material (i.e: resistors, capacitors, experimental board to solder on.)

  3. **ONLY WHEN 2 HAS BEEN COMPLETED**  ```and```  we decide to carry on with encoders for the pitch, can we integrate the motor to my test motor and run an integration to the whole system. ```if```  **WE DECIDE TO GO WITHOUT THE ENCODERS**, test of my code can be run on the launcher but they will have to be run minding the loads and therefore they will take more time. 