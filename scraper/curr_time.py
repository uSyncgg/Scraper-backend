import datetime
import time
from datetime import timedelta

def get_currTime():
    t = datetime.datetime.now()
    current_time = t.strftime('%I:%M %p')
    current_date = time.strftime("%b %d")
    tomorrow = datetime.datetime.now() + timedelta(days=1)
    formatted_tomorrow = tomorrow.strftime("%b %d")

    return current_time, current_date, formatted_tomorrow