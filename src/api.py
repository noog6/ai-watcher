import os
import socket
import time
from flask                           import Flask, jsonify, request, render_template, render_template_string, send_from_directory
import threading
from event_handler                   import AudioEventHandler, CameraEventHandler, ServoEventHandler
from controllers.sensor_service      import SensorService
from hardware.ServoRegistry          import ServoRegistry
from hardware.AudioController        import AudioController
from controllers.storage_controller  import StorageController
from controllers.data_controller     import DataController
from controllers.imu_controller      import IMUController
from controllers.config_controller   import ConfigController

#################################
# Event Handlers Initialization #
#################################

audio_event_handler = AudioEventHandler()
camera_event_handler = CameraEventHandler()
servo_event_handler = ServoEventHandler()

# Start event processing threads
threading.Thread(target=audio_event_handler.process_events, daemon=True).start()
threading.Thread(target=camera_event_handler.process_events, daemon=True).start()
threading.Thread(target=servo_event_handler.process_events, daemon=True).start()
# Some ASCII Art thanks to https://www.asciiart.eu/text-to-ascii-art
#################################

def display_ascii_title():
    print("")
    print("    _     ___     __        __      _         _                 ")
    print("   / \   |_ _|    \ \      / /__ _ | |_  ___ | |__    ___  _ __ ")
    print("  / _ \   | | _____\ \ /\ / // _` || __|/ __|| '_ \  / _ \| '__|")
    print(" / ___ \  | ||_____|\ V  V /| (_| || |_| (__ | | | ||  __/| |   ")
    print("/_/   \_\|___|       \_/\_/  \__,_| \__|\___||_| |_| \___||_|   ")
    print("")
    
#################################
# Controllers ###################
#################################

display_ascii_title()
app               = Flask("ai-watcher")
hostname          = socket.gethostname()
storage_service   = StorageController.get_instance()
sensor_service    = SensorService()
data_service      = DataController.get_instance()
servo_reg         = ServoRegistry.get_instance()
imu_service       = IMUController.get_instance()
audio_service     = AudioController.get_instance()
config_controller = ConfigController.get_instance()
config            = config_controller.get_config()

#################################
# Endpoints - Sensor Data #######
#################################

@app.route('/pressure_sensor')
def get_pressure_sensor_data():
    data = sensor_service.get_pressure_sensor_data()
    if isinstance(data, Exception):
        return jsonify({'error': str(data)}), 500
    storage_service.add_data_sample( data )
    return jsonify(data)

@app.route('/analog_input_sensor')
def get_analog_input_sensor_data():
    data = sensor_service.get_analog_input_sensor_data()
    storage_service.add_data_sample( data )
    return jsonify(data)

@app.route('/battery_voltage')
def get_battery_voltage_data():
    data = data_service.get_battery_voltage()
    storage_service.add_data("battery_voltage", data )
    return jsonify(data)

@app.route('/imu_sensor')
def get_imu_data():
    data = imu_service.get_imu()
    #storage_service.add_data("imu", data )
    return jsonify(data)

@app.route('/uptime')
def get_uptime_data():
    data = data_service.get_uptime()
    storage_service.add_data("uptime", data )
    return jsonify(data)

@app.route('/service_status')
def get_service_status():
    data = data_service.get_service_status()
    storage_service.add_data("service_status", data )
    return jsonify(data)

#################################
# Endpoints - Audio #############
#################################

@app.route('/audio/play', methods=['POST'])
def play_audio():
    filename = request.json.get('filename')
    #audio_controller = AudioController.get_instance()
    #audio_controller.play(filename)
    storage_service.add_log('warn', f'Someone asked us to play this audio file - {filename}')
    return 'Audio played successfully', 200

@app.route('/audio/record', methods=['POST'])
def record_audio():
    duration = request.json.get('duration')
    filename = request.json.get('filename')
    #audio_controller = AudioController.get_instance()
    #audio_controller.record(duration, filename)
    storage_service.add_log('warn', f'Someone asked us to record to this audio file - {filename}')
    return 'Audio recorded successfully', 200

#################################
# Endpoints - UI Screens ########
#################################

@app.route('/')
def dashboard():
    with open('templates/dashboard.html', 'r') as f:
        dashboard = f.read()
    return render_template_string(dashboard, hostname=hostname)

#@app.route('/remote')
#def remote():
#    return render_template('remote.html', hostname=hostname)

#################################
# Error Handling ################
#################################

@app.errorhandler(Exception)
def handle_exception(e):
    # pass the exception to the storage service
    storage_service.log_exception(e)
    # return a JSON response with the error details
    return jsonify({'error': str(e)}), 500

#################################
# Main Application ##############
#################################

if __name__ == '__main__':
    storage_service.add_log('info', f'AI-Watcher started on host ({hostname})')
    
    data_service.start_low_speed_data_thread()
    
    imu_service.start_imu_thread()
    print("")
    print("IMU Data:")
    imu_service.print_imu()
    print("")
        
    app.run(host='0.0.0.0', debug=False)

