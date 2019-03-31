from datetime import datetime
import time


def ts_to_str(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def ts_ago(ts):
    sec = int(time.time() - ts)
    if sec < 120:
        return '%d sec ago' % sec
    minutes = sec / 60
    if minutes < 120:
        return '%d min ago' % minutes
    return '%d hours ago' % (sec / 3600)
