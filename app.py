from flask import Flask, render_template, Response, stream_with_context, jsonify,request
from flask_mqtt import Mqtt
import sqlite3
import json
import time
from datetime import datetime
import random
import csv
import pandas as pd
from io import StringIO,BytesIO
import io
from filter_data import filter_data
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'M3ExGxt4y2DmCkvN8CAqK0tYyUD4GLEgD9D7uV0TNt3dCoRAOfPo58brRCkncOrF'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0 
mqtt = Mqtt(app)

def get_db_connection():
    conn = sqlite3.connect('sensors_data.db')
    conn.row_factory = sqlite3.Row
    return conn
send_data=''
@app.route('/')
def index():
    return render_template('index.html')

data_response = []

@app.route('/chart-data', methods=['GET', 'POST'])
def chart_data():
    global data_response
    extra=data_response
    if request.method == 'GET':
        print('get')
        def get_database_data():
            try:
                
                if extra is not None:
                    a=0
                    for i in extra:
                        a+=1
                        json_data = json.dumps(i)
                        print('json_data',json_data)
                        yield f"data:{json_data}\n\n"
                        time.sleep(0.01)
                    
            except UnboundLocalError:
                pass  # Xử lý ngoại lệ UnboundLocalError bằng cách bỏ qua
            return
        response = Response(stream_with_context(get_database_data()), mimetype="text/event-stream")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Accel-Buffering"] = "no"
        # return jsonify(data_response), 200
        data_response=None
        return response
    
    elif request.method == 'POST':
        file = request.files.getlist('file')
        print('files_csv_post',file)
        if file[0] and file[0].filename.endswith('.csv'):
            data = file[0].read().decode('utf-8').splitlines()
            df = pd.read_csv(StringIO('\n'.join(data)))
        if file[0] and file[0].filename.endswith('.xlsx'):
        # Read the Excel file directly from the FileStorage object
            df = pd.read_excel(file[0], sheet_name='Shop 1-(07-31.07.2022)', engine='openpyxl')            
            df=filter_data(df)
        data_response=[]
        for index, row in df.iterrows():
            send_data= {'temp_time': f"{row['TIME']}", 'temp_value': f"{row['SOUND']}"}
            print(send_data)
            json_data = json.dumps(send_data)
            data_response.append(send_data)
            #yield f"data:{json_data}\n\n"
            
        # data_response = f"data:{json_data}\n\n"
        print(data_response, "-------", send_data)

        dataReturn = {"temp_time": "2024-05-07 15:30:01.997301", "temp_value": "22", "humi_time": "2024-05-07 15:30:01.997301", "humi_value": "21"}
        
        return jsonify(dataReturn), 200
        
 

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	mqtt.subscribe('Temp')
	mqtt.subscribe('Humi')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()
    """
    cursor.execute("DELETE FROM temp_data \
            WHERE id <= (SELECT MAX(id) FROM temp_data) - 100")
    cursor.execute("DELETE FROM humi_data \
            WHERE id <= (SELECT MAX(id) FROM humi_data) - 100")
    """
    if message.topic == 'Temp':
        cursor.execute("INSERT INTO temp_data (data) VALUES (?)",
                (message.payload.decode(),)
                )
    elif message.topic == 'Humi':
        cursor.execute("INSERT INTO humi_data (data) VALUES (?)",
                (message.payload.decode(),)
                )
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
	app.run(debug=True, port=5000, host='0.0.0.0')