import pytz
from datetime import datetime

def get_view_date(date):
    timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.now().astimezone(timezone).date()
    if date.date() == today:
        return str(date.hour) + ":" + str(date.minute)
    else:
        return str(date.month) + "/" + str(date.day)