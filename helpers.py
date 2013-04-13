import datetime

def getWeek():
    week_num = datetime.date.today().isocalendar()[1]
    return week_num

def getMonth():
    now = datetime.datetime.now()
    return now.month
