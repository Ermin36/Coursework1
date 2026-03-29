from calendar import month

import pandas as pd
from typing import Optional
import datetime as dt

from src import Operations, Operation


def decor_reports() -> callable:
    pass


def decor_reports_arg() -> callable:
    pass


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция сбора трат по категории за заданную дату времени
    :param transactions: список транзакций
    :param category: категория по которой происходит сортировка
    :param date: дата в формате YYYY.MM
    :return: траты по категории
    """

    if date is None:
        end_date = pd.Timestamp.now()
    else:
        datetime_date =  dt.datetime.strptime(date,'%Y.%m')
        end_date = pd.Timestamp(datetime_date)

    start_date = end_date - pd.DateOffset(months=3) # получение даты за 3 месяца до текущей

    operations = Operations.read_dataframe(transactions) # преобразование в класс Operations
    data_list = operations.operation_list # получение списка операций
    # сортировка списка
    sort_list = [item for item in data_list if item.category == category and (start_date < item.date < end_date)]

    #создание нового класса
    new_operations = Operations(sort_list)
    #возвращение DataFrame
    return new_operations.dataframe


