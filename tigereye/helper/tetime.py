from datetime import datetime


def now():
    # strftime()时间格式化
    return datetime.now().strftime('%Y%m%d%H%M%S')
