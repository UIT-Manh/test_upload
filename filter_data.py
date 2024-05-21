import pandas as pd
from set_time import datetime_string
import time
import requests
def filter_data(data):
    name_col= data.iloc[4]
    rows_to_drop = data.index[0:5]
    # Xóa 4 hàng đầu tiên
    data_cleaned = data.drop(rows_to_drop)
    data_cleaned.columns = [name_col]
    return data_cleaned
def send_data(df):
    url = 'https://thingsboard.cloud/api/v1/XFuMjyQwX11DvLJjjLYz/telemetry'

    # Tạo header cho request
    headers = {'Content-Type': 'application/json'}

    # Định nghĩa dữ liệu JSON sẽ gửi đi
    # data = '{"temperature": 25, "hem": 60}'
    for index, row in df.iterrows():
        a=time.time()
        ts=datetime_string(row['TIME'])
        send_data= {"time": f"{ts}", "sound_value": f"{row['SOUND']}"}
        print(send_data)
        # json_data = json.dumps(send_data)
        # data_response.append(send_data)
        # Gửi POST request
        b=time.time()
        response = requests.post(url, headers=headers, data=f'{send_data}')
        print('response ',time.time()-b)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print('Time',time.time()-a)
        # In ra status code và phản hồi từ server
if __name__ == '__main__':
    df=pd.read_excel(r'D:\vinergy\Ned Spice Sound test report (July-2022).xlsx',sheet_name='Shop 1-(07-31.07.2022)') # uploading data
    df= filter_data(df)
    send_data(df)

# Định nghĩa URL của API
    
        

    