#DRONE LAUNCHER

from flask import Flask, render_template, request, jsonify
from roboclaw import Roboclaw
import socket
from time import sleep
from launcher import *

lnchr = Launcher()
encoders_ready = 0

#Create an instance of the Flask class for the web app
app = Flask(__name__)

#Render HTML template
@app.route("/")
def index():
    return render_template('dronelauncher_web.html')

@app.route('/app_pitch_up', methods=['POST'])
def function_pitch_up():
    lnchr.pitch.up()
    return (''), 204 #Returns an empty response

@app.route('/app_pitch_down', methods=['POST'])
def function_pitch_down():
    lnchr.pitch.down() #This might actually have to be the other way around
    return (''), 204

@app.route('/app_pitch_position', methods=['POST'])
def function_pitch_position():
    lnchr.pitch.position_absolute()
    return (''), 204

@app.route('/app_pitch_stop', methods=['POST'])
def function_pitch_stop():
    lnchr.pitch.stop()
    sleep(0.02)
    return (''), 204

@app.route('/app_rotation_right', methods=['POST'])
def function_rotation_right():
    lnchr.rotation.up()
    return (''), 204

@app.route('/app_rotation_left', methods=['POST'])
def function_rotation_left():
    lnchr.rotation.down()
    return (''), 204

@app.route('/app_rotation_position', methods=['POST'])
def function_rotation_position():
    lnchr.rotation.position_absolute()
    return (''), 204

@app.route('/app_rotation_stop', methods=['POST'])
def function_rotation_stop():
    lnchr.rotation.stop()
    sleep(0.02)
    return (''), 204

@app.route('/app_lift_up', methods=['POST'])
def function_lift_up():
    lnchr.lift.up()
    return (''), 204

@app.route('/app_lift_down', methods=['POST'])
def function_lift_down():
    lnchr.lift.down()
    return (''), 204

@app.route('/app_lift_position', methods=['POST'])
def function_lift_position():
    lnchr.lift.position_absolute()
    return (''), 204

@app.route('/app_lift_stop', methods=['POST'])
def function_lift_stop():
    lnchr.lift.stop()
    sleep(0.02)
    return (''), 204

@app.route('/app_launch_forwards', methods=['POST'])
def function_launch_forwards():
    lnchr._launch.up() # Needs its own up and down routine here. Pitch also
    return (''), 204

@app.route('/app_launch_backwards', methods=['POST'])
def function_launch_backwards():
    lnchr._launch.down()
    return (''), 204

@app.route('/app_launch_position', methods=['POST'])
def function_launch_position():
    lnchr._launch.position_absolute()
    return (''), 204

@app.route('/app_launch_stop', methods=['POST'])
def function_launch_stop():
    lnchr._launch.stop()
    sleep(0.02)
    return (''), 204


@app.route('/app_max_pitch', methods=['POST'])
def function_max_pitch():
    lnchr.pitch.position(lnchr.pitch.pulses_max)
    return (''), 204

@app.route('/app_min_pitch', methods=['POST'])
def function_min_pitch():
    lnchr.pitch.position(lnchr.pitch.pulses_min)
    return (''), 204

@app.route('/app_max_lift', methods=['POST'])
def function_max_lift():
    lnchr.lift.position(lnchr.lift.pulses_max)
    return (''), 204

@app.route('/app_min_lift', methods=['POST'])
def function_min_lift():
    lnchr.lift.position(lnchr.lift.pulses_min)
    return (''), 204


@app.route('/app_case_open', methods=['POST'])
def function_case_open():
    lnchr.case.up()
    return (''), 204

@app.route('/app_case_close', methods=['POST'])
def function_case_close():
    lnchr.case.down()
    return (''), 204 

@app.route('/app_home', methods=['POST'])
def function_home():
    lnchr.pitch.down()
    lnchr.lift.down()
    lnchr._launch.down()
    # case has no home setting
    # rotation has no home setting
    return (''), 204


@app.route('/app_reset_encoders', methods=['POST'])
def function_reset_encoders():
    """This function does NOTHING"""
    lnchr.reset_encoders()
    global encoders_ready
    encoders_ready = 1 #Encoders have been reset
    return (''), 204


@app.route('/app_battery_voltage', methods=['POST'])
def function_battery_voltage():
    voltage = round(lnchr.pitch.read_voltage ,2)
    return jsonify(voltage=voltage)


# @app.route('/measurements', methods=['GET'])
# def data_display():
#     '''
#     This function gets the data from the gyrscope and the temp sensor send them to the webpage
#     '''
#     try:
#         temp = thermo.read_temp()
#     except:
#         temp = 'NaN'
#     try:
#         x_rotation = MPU9250.gyro_data()[0]
#     except:
#         x_rotation = 'NaN'
#     try:
#         y_rotation = MPU9250.gyro_data()[1]
#     except:
#         y_rotation = 'NaN'
#     try:
#         angle = MPU9250.gyro_data()[2]
#     except:
#         angle = 'NaN'
#     try:
#         gyro_temp = MPU9250.gyro_data()[3]
#     except:
#         gyro_temp = 'NaN'
#     try:
#         cpu_temp = MPU9250.gyro_data()[4]
#     except:
#         cpu_temp = 'NaN'
    
#     return jsonify(temperature=temp,x_rotation=x_rotation,
#                    y_rotation=y_rotation, angle=angle,
#                    gyro_temp=gyro_temp, cpu_temp=cpu_temp)
#                    #Don't forget to add the return variables
                   

@app.route('/app_stop', methods=['POST'])
def function_stop():
    """Using rc.SpeedDistanceM1M2 here would also wash-over remaining buffers?"""
    lnchr.stop_all()
    return (''), 204

@app.route('/app_standby', methods=['POST'])
def function_standby():
    lnchr.standby()
    return (''), 204

@app.route('/app_prepare', methods=['POST'])
def function_prepare():
    lnchr.prepare()
    return (''), 204

@app.route('/app_launch', methods=['POST'])
def function_launch():
    lnchr.launch()
    return (''), 204

@app.route('/app_mount', methods=['POST'])
def function_mount():
    lnchr.mount
    return (''), 204

@app.route('/app_disable_buttons', methods=['POST'])
def function_disable_buttons():
    return jsonify(encoders_ready=encoders_ready)

if __name__ == "__main__":
    app.run('localhost',port=5000, debug=True)