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
+ **The motors have to be tuned via rc.ReadM1PositionPID and rc.SetM1PositionPID correctly. Otherwise positional requests will not take effect.**
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