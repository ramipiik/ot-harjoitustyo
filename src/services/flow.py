from .day import start_day
from ui.text_ui import new_period
import datetime

# START_DATE='2021-10-01'
first_year=2021
first_month=10
first_day=1
date = datetime.datetime(first_year, first_month, first_day).date()


def move_forward():
    global date
    i=0
    while i<10:
        start_day(date)
        new_period(date)
        date += datetime.timedelta(days=1)
        i+=1
