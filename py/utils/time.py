from datetime import datetime


def ts_to_str(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %I:%M:%S")
