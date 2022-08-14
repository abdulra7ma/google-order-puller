from datetime import datetime


def convert_date(date_sting):
    """
    Converts the date string format of 12.09.2022 to 2022-09-12
    """
    return datetime.strptime(
        date_sting.replace(".", "/"), "%d/%m/%Y"
    ).strftime("%Y-%m-%d")
