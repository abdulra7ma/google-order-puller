import xmltodict
import requests

from datetime import date


def get_usd_ruble_today_exchange():
    """
    Отправьте запрос в ЦБ РФ, чтобы получить актуальные курсы обмена с другими валютами
    на рубли и вернуть обменный курс доллара США.

    Returns:
        -> usd_value (float)
    """
    query_date = date.today().strftime("%d/%m/%Y")
    uri = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={query_date}"

    response = requests.get(uri)
    data = xmltodict.parse(response.content)

    usd_obj = [
        obj for obj in data["ValCurs"]["Valute"] if obj["CharCode"] == "USD"
    ]

    usd_value = float(usd_obj[0]["Value"].replace(",", "."))

    return usd_value
