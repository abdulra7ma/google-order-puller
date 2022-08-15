from copy import deepcopy
from os.path import join

import gspread
from django.conf import settings
from stats.models import Order
from stats.services.order import create_orders, delete_orders, update_orders


def initiate_work_spreedsheet(
    credentials_file, main_sheet, working_sheet
) -> gspread.Worksheet:
    """
    Инициировать клиент Google SpreadSheet и вернуть объект Worksheet
    """

    client = gspread.service_account(credentials_file)
    sheet = client.open(main_sheet)
    return sheet.worksheet(working_sheet)


def orders_puller(work_sheet: gspread.Worksheet) -> None:
    all_sheet_recorders = iter(work_sheet.get_all_records())
    records_count = sum(1 for _ in deepcopy(all_sheet_recorders))

    orders_numbers = list(Order.objects.all().values_list("number", flat=True))

    create_objests = []
    update_objects = []
    create_update_orders_numbers = []

    for _ in range(records_count):
        order = next(all_sheet_recorders)

        if order["заказ №"] in orders_numbers:
            update_objects.append(
                {"order_number": order["заказ №"], "order_data": order}
            )
        else:
            print("Created new order -> order number:", order["заказ №"])
            create_objests.append(order)

        create_update_orders_numbers.append(order["заказ №"])

    if len(create_objests) > 1:
        # create new orders
        create_orders(create_objests)

    if len(update_objects) > 1:
        # update existing orders
        update_orders(update_objects)

    delete_recorders = {
        num
        for num in orders_numbers
        if num not in create_update_orders_numbers
    }
    if len(delete_recorders) > 1:
        # delete orders
        delete_orders(delete_recorders)

    print("finished")

    return


def puller_initiator() -> None:
    """
    Функция задания Cron, которая инициирует рабочий лист и передает его функции orders_pullers.
    Работает: каждые две минуты
    """

    wk_sheet = initiate_work_spreedsheet(
        credentials_file=join(
            settings.CORE_APP,
            "google-cred.json",
        ),
        main_sheet="my test",
        working_sheet="Sheet1",
    )
    orders_puller(wk_sheet)
    return True
