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

## EXTRA CONTROLS

  **ANSWER THIS QUESTION:** if you have pressed on 'PREPARE' and then you press on 'MOUNT' what happens? since they are both threaded events, they could be accessing the same values at the same time and they would be unaware that the other routine is currently ongoing. This could lead to -at best- strange motions as the orders compete with each other or -at worst- a logical race that could damage the circuits and/or make them completely unpredictable. 
  
  **THOUGHTS:** This might call for a **state machine** or an **array** so that functions can not be triggered so long as another is **flagged**.<br>As we use **threaded events**, this might call for the use of **Locks**. something to look into.

[Entry log 20-11-12]: Today I have started the day by testing the new ANT-52 actuator. Unfortunately with very inconclusive results. It seems the problem of noise offered by the other ANT-52 was resolved but a new issue has arisen where the speed pulse reading is unreliable. it has a somewhat 'floating' quality. I have written a mail to Peter at Sito Motors to report this and wait to see if they have any advice.<br>In the meantime I have to turm back to the original ANT-52. The problem of noise is more promising to solve than the problem of speed pulses. I have reinvestigated the problem of the Low Pass filter that originally triggered the ordfer of the new ANT-52. My belief was that it was busted and therefore we should get a better hardware not to have to rely on Low Pass anymore and have a system that was more robust. In investigating the Low Pass closer I realised that the issue that had me believe it was busted was in fact resistors embedded in the actual wires. I went back to the original thesis paper and could not find any notice of such components.<br>The details of the low pass are as such:
+ Noise frequency to shut out: 20kHz
+ Capacitor on board: 1nF
+ Resistor available: 8200 ohm
+ actual shut off frequency = 1/(2 pi RC) = 19409 Hz

But in finding the resistors in the cables, I actually have two resistance in serie coming into this Low Pass filter (the embedded resistor value is 12kohm) and their total value is 22.2kohm. this means that the **actual shut off frequency** is actually **7169Hz** which may or may not be a problem but by all accounts, if the noise frequency is up towards 20kHz the low pass should work towards that frequency. Earlier in th season, when I assessed and developped a functionning Low Pass filter for the ANT-52, I was able to get some good results even if (or specially because) these resistors weren't in my design. retesting the ANT-52 is primordialand so I will design a back up filter all the whilst we can re-test the current Low Pass without the added resistors and see what results we can get.
(I should add that although I can't quite figure out what the resistors were for, I am suspecting that there are more in more parts of the system. They could have been a way to try and simulate a a pull up resistor but if so, it is not how that is designed. a Pull up delivers extra current coming from a constant power source so that it is reliable)

**AD HOC OBSERVED IN THE DAY**<br> In coming in, I noticed that the column was not turning as expected. I pointed that out and when we ran some tests on the motors, it was clear that the rotation motor had some trouble proceeding around. it could do it but it was far from flowless and given a PWM it would not be able to proceed effectively. trying it out with speed pulses commands would be more reliable.

**DISCUSSIONS** <br>I pointed out today that the axel situated between the column and the base of the case if floating and that could be a problem if left unchecked. I also explained how the downwards motion of the pitch offers and slight angle due to the changing center of gravity in the case (when it is lowered and sent back up) this usually becomes visible as some screws being looser than usual in the back panel but now with the new cover, it might translate to some physical bending and as the screws are not easily reachable I recommended that checking screws as part of routine should take place every now and again.<br>We laso talked about the rotation and potential stoppers being installed later to keep the rotation from doing a full rotation. Which is of great interest when thinking about safety. so long as we can have physical stops, the system is safer than not.<br>

**PITCH** physical max and min<br>
**ROTATION** unbound<br>
**LIFT** physical max and min<br>
**LAUNCH** physical min but no bound max<br>
**CASE** physical max and min<br>

What is then left to try:<br>
1. A solution has to be found as to what we can do with the ANT-52. 
2. Manually tune all of the motors.
3. Correct the launching code on the launcher using position
4. See what can be done about my code and the launcher itself.

[**ENTRY LOG 2020-11-24**]: What did I see today?
+ I have put together two motors on one roboclaw and was able to use the position() method as well as the buffer_arithmetic() to run motors one after the other. I have videos of their execution as well as a print out of the python shell session.<br>It is interesting to note that I did not get satisfying resuts last week when testing this as I trying to set a control with two buffers did not seem to translate well to the routine I wanted to see. videos of this are also available..
+ after that success I attached another Roboclaw with another motor to try and repeat the earlier test with hopefully the same results. **wheelR** motor's encoders stopped responding during the setup (not sure why but the motors are very cheap, so...).<br>Anyways, with the same codeing style as on one robclaw, I was able to observe **a good routine of one motor after the other with no delay in communication whatsoever**. I also have a video of that.
+ Following this, I tested a threaded event routine (**GIVING ME ACCESS TO STOP FUNCTION**) and I was able to observe a good set up with stops that were immediate. BUT also when the Event was set again, it would pick up where the previous left off. So that was good

PROBLEMS STILL AFOOT:
1. THE THREADS ARE NOT SAFE. OTHER FUNCTIONS CAN BE ACCESSED WHILE A THREAD IS ONGOING, POTENTIALLY LEADING TO A CLASH IN ORDERS.
2. ALL MOTORS (except case) NEED POSITION SETTINGS TO BENEFIT FROM THE NEW CODES.<br>so far, the following motors have position settings:<br>PITCH<br>LAUNCH
3. THE ANT-52 WILL NEED SOME EXTRA CARE.

[**ENTRY LOG 2020-12-08**]: 
1. Set up the new switches on the launcher. went well except for the base switch holder which I damaged. New one on the way.
2. Follow up test of the ANT-52. I got very good results using the position function but must now find out if that impacts the Speed functions in anyway before I start using the entire launcher. These could cause some problems so it is important that gets checked ahead of time as the code used by Daniel uses SpeedDistance for the positon and more advanced functions but my ANT-52 currently has no Velocity PID... They seemed to make it behave strangely so I bypassed them.
3. The ANT-52 was reinstalled and the switch was alos installed and they stand to be tested next time I come in (planned for tomorrow)
4. On checks I was able to see that the rotation motor will come off easily so that I can tune it without risking the whole platform moving out of control. This is only relevant to my code as Daniel's does not make use of any position settings. again, upon tests, we must be able to report that the motor behaves well with the PID for Velocity and Position tuned correctly.

**TOMORROW'S PLAN:**
1. Test the ANT-52 **ON** the system (We keep in mind that with a busy set of wires, some of the unwanted behaviours could be generated by surrounding noise and magnetic fields). BASICMICRO + IDLE
2. If the tests pass, test from the GUI
3. If the tests pass, test the rest of the motors.
4. AT THIS POINT, check the SD card **OR** run test from the testpi/computer. Keep the case **OPEN**
5. Now test the functions. start with **HOME**
6. Test **PREPARE**
8. Test **MOUNT**
7. Test **STANDBY**
9. Maybe switch at this point to the computer so that you can run a smooth **LAUNCH** and attempt (video documented), **PREPARE**, **LAUNCH**, **STANDBY**. Best would probably be if we test that from the testPi rather than the Computer. Then it is time to compare the code from the testPi and the one found in the LauncherPi. 
10. Think about how your code could be implemented in this system, take out the rotation motor and tune it, start to look at adding a servo motor and what that would mean for the system or how it would be done.

[**ENTRY LOG 2020-12-14**]: All systems are a go.<br>
One problem left, with the launcher. here are the tests that must be ran to determine if I am right:
+ Go look at the home set up on Motion Studio. Check the encoder box and try to run a Speed command. What happens then?
+ I believe that the issue lies there. it is basically an encoder alignment issue. Test real quick at home to establish viability and then run again on system on friday.
+ I have also realised that I have been wrong for a while about something. It is the Launcher motor that has damaged the old 129 roboclaw... Something to keep in mind.