import pandas as pd
from set_time import datetime_string
import time
import requests
import threading
import json
import paho.mqtt.client as mqtt
host = "mqtt.thingsboard.cloud"
port = 1883
topic = "v1/devices/me/telemetry"
username = "XFuMjyQwX11DvLJjjLYz"
def filter_data(data):
    name_col= data.iloc[4]
    rows_to_drop = data.index[0:5]
    # Xóa 4 hàng đầu tiên
    data_cleaned = data.drop(rows_to_drop)
    data_cleaned.columns = [name_col]
    return data_cleaned
def send_data(df):
    # url = 'https://thingsboard.cloud/api/v1/XFuMjyQwX11DvLJjjLYz/telemetry'

    # # Tạo header cho request
    # headers = {'Content-Type': 'application/json'}

    # # Định nghĩa dữ liệu JSON sẽ gửi đi
    # # data = '{"temperature": 25, "hem": 60}'
    # for index, row in df.iterrows():
    #     a=time.time()
    #     ts=datetime_string(row['TIME'])
    #     send_data= {"time": f"{ts}", "sound_value": f"{row['SOUND']}"}
    #     print(send_data)
    #     # json_data = json.dumps(send_data)
    #     # data_response.append(send_data)
    #     # Gửi POST request
    #     b=time.time()
    #     response = requests.post(url, headers=headers, data=f'{send_data}')
    #     print('response ',time.time()-b)
    #     print(f"Status Code: {response.status_code}")
    #     print(f"Response: {response.text}")
    #     print('Time',time.time()-a)
        # In ra status code và phản hồi từ server
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            send_next_message(client)  # Begin sending messages
        else:
            print("Connection failed, error code:", rc)
            
    def on_publish(client, userdata, mid):
        print("Message sent with ID:", mid)
        if hasattr(send_next_message, 'last_send_time'):
            elapsed = time.time() - send_next_message.last_send_time
            print('elapsed',elapsed)
            if elapsed > 0.3:
                print("Timeout, skipping to next message.")
                # send_next_message.index += 1
                send_next_message(client)
            else:
                send_next_message(client)
    def send_next_message(client):
        if not hasattr(send_next_message, 'index'):
            send_next_message.index = 0  # Initialize index if it doesn't exist
        if send_next_message.index < df.shape[0]:
            datetime = datetime_string(df.iloc[send_next_message.index]["TIME"])
            sound_value = df.iloc[send_next_message.index]["SOUND"]
            message = json.dumps({"time": datetime,"sound_value": sound_value})
            # print(time.timestamp())
            # breakpoint()
            send_next_message.last_send_time = time.time()  # Record sending time
            client.publish(topic, message, qos=1)
            print(f"Sending: {message}", send_next_message.index)
            send_next_message.index += 1
        else:
            client.disconnect()
            print("All messages sent and disconnected.")
    # Tạo MQTT client
    client = mqtt.Client()
    client.username_pw_set(username)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to MQTT broker
    client.connect(host, port, 60)
    client.loop_forever()  # Start the network processing loop


if __name__ == '__main__':
    df=pd.read_excel(r'D:\vinergy\Ned Spice Sound test report (July-2022).xlsx',sheet_name='Shop 1-(07-31.07.2022)') # uploading data
    df= filter_data(df)
    send_data(df)

# Định nghĩa URL của API
    
        

    