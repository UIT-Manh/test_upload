from datetime import datetime
def datetime_string(datetime_str):
    # Define the format of the datetime string
    datetime_format = "%d-%m-%y/%H:%M:%S"
    # Convert the string to datetime object
    date_time = datetime.strptime(datetime_str, datetime_format)
    # Convert datetime to timestamp in milliseconds
    timestamp = int(date_time.timestamp() * 1000)
    return timestamp

# Example usage:
datetime_str = "21-07-22/21:20:46"
timestamp_in_milliseconds = datetime_string(datetime_str)




date = datetime.fromtimestamp(timestamp_in_milliseconds // 1000)

def datetime_to_timestamp1(date_time):
    # Convert datetime to timestamp in milliseconds
    timestamp = int(date_time.timestamp() * 1000)
    return timestamp

# Example usage:31-07-22/23:59:46
# date_time = datetime(2024, 5, 10, 12, 0)  # Example datetime object