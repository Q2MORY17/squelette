pitch = {
    'address' : 131, #don't forget to change back to 128
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
    'address' : 128,
    'channel' : 0,
    'pulses_min' : 0,      
    'pulses_max' : 100000,
    'pulses_unit' : 2000,   
    'length' : 50.0,         
    'unit' : 'centimeter(s)',
    'speed_pulses' : 10000,   
    'speed_manual' : 75, 
    'ready' : 75000 # 25.0 degrees
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
    'acceleration' : 500000, 
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

std_accel = 400000          # Max accel = 655359. This variable is a dampened accel
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
