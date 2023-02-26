from datetime import datetime

def convert_timestamp_to_timestr(timestamp):
    time = datetime.fromtimestamp(timestamp)
    hours = time.hour
    minutes = time.minute

    if hours < 10:
        hours = f'0{hours}'
    if minutes < 10:
        minutes = f'0{minutes}'

    return f'{hours}:{minutes}'