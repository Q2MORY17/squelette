pitch = {
    'address' : 128, #don't forget to change back to 128
    'channel' : 0,
    'pulses_min' : 0,      
    'pulses_max' : 355000,
    'pulses_unit' : 3944,   
    'length' : 90.0,         
    'unit' : 'degree(s)',
    'speed_pulses' : 7000,   
    'speed_manual' : 127, 
    'ready' : 256360 # 25.0 degrees
    }

test = {
    'address' : 133,
    'channel' : 0,
    'pulses_min' : 0,      
    'pulses_max' : 20000, #100000 AT 12v
    'pulses_unit' : 2000,   
    'length' : 50.0,         
    'unit' : 'centimeter(s)',
    'speed_pulses' : 6000,   
    'speed_manual' : 75, 
    'ready' : 10000  #75000 # 25.0 degrees
    }          

rotation = {
    'address' : 128,
    'channel' : 1,
    'pulses_min' : -316666,
    'pulses_max' : 316666,
    'pulses_unit' : 5277,
    'length' : 120.0, 
    'unit' : 'degree(s)',
    'speed_pulses' : 16000, 
    'speed_manual' : 15,    
    'ready' : 26385 # 5.0 cm 
    }

lift = {
    'address' : 129,
    'channel' : 0,
    'pulses_min' : 0,    
    'pulses_max' : 19000,
    'pulses_unit' : 146, 
    'length' : 130.0,    
    'unit' : 'centimeter(s)',
    'speed_pulses' : 420, 
    'speed_manual' : 75,  
    'ready' : 2190 # 15 cm 
    }

launch = {
    'address' : 129,
    'channel' : 1,
    'pulses_min' : 0,     
    'pulses_max' : 14000,
    'pulses_unit' : 133, 
    'length' : 111.0,    
    'unit' : 'centimeter(s)', 
    'speed_pulses' : 2500, 
    'speed_pulses_launch' : 100000,
    'speed_manual' : 20,
    'ready' : 8000, # 60 cm
    'mount' : 17000,
    'overshoot' : 23000,
    'acceleration' : 400000, 
    'decceleration' : 200000
    }

case = {
    'address' : 130,
    'channel' : None,
    'pulses_min' : 0,    
    'pulses_max' : 6000,
    'pulses_unit' : 1200,
    'length' : 5.0,    
    'unit' : 'centimeter(s)', 
    'speed_pulses' : None, 
    'speed_manual' : None,  
    'ready' : None, 
    'speed_pulses_open' : 1500,
    'speed_pulses_close' : -500
    }

wheelL = { 
    'address' : 132,
    'channel' : 0,
    'pulses_min' : 0,      
    'pulses_max' : 6154, # 10 turns
    'pulses_unit' : 25,   
    'length' : 250.0,         
    'unit' : 'centimeter(s)',
    'speed_pulses' : 500,   
    'speed_manual' : 15, 
    'ready' : 3000 # 25.0 degrees
    }          

wheelR = {
    'address' : 132,
    'channel' : 1,
    'pulses_min' : 0,
    'pulses_max' : 6154, # 10 turns
    'pulses_unit' : 25,
    'length' : 250.0, 
    'unit' : 'centimeter(s)',
    'speed_pulses' : 500, 
    'speed_manual' : 15,    
    'ready' : 3000 # 5.0 cm 
    }

std_accel = 500000          # Max accel = 655359. This variable is a dampened accel
std_deccel = 300000         # Max deccel = 655359. This variable is a dampened deccel

case_closed = True             # Open/close index
stop = False

if pitch['channel'] == rotation['channel']:
    raise PermissionError("Picth and rotation are mistakenly set to the same channel")

if lift['channel'] == launch['channel']:
    raise PermissionError("Picth and rotation are mistakenly set to the same channel")

if rotation['speed_pulses'] > 16000 or rotation['speed_manual'] > 15:
    rotation['speed_pulses'] = 16000
    rotation['speed_manual'] = 15
    raise Warning("Rotation speeds are reset to original.\nIncreased speed = danger\nUpdate this security if sure you can increase speed.")

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