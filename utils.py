from datetime import datetime, date


def get_past_recent_date(date_string) -> str:
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    date_object_recent = date_object.replace(year=date.today().year - 1)
    return date_object_recent.strftime('%Y-%m-%d')