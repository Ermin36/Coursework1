from src import Operations, Operation
import datetime as dt
from typing import Any
import pandas as pd


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """
    Получение суммы для инвест-копилки по операциям за месяц
    :param month: Дата в формате YYYY-MM
    :param transactions: операции
    :param limit: лимит округления
    :return: сумма в инвест-копилку
    """
    date = dt.datetime.strptime(month, '%Y.%m') # получение даты
    end_date = pd.Period(date, freq='M').end_time.date() # вычисление последнего дня месяца
    operations = Operations([Operation.new_operation_as_dict(item) for item in transactions]) # создание класса
    operations.sort_by_date(end_date.strftime('%Y.%m.%d %H:%M:%S')) # сортировка по дате
    data_list = operations.operation_list # получение списка

    def diff(number: float, step: int) -> float: # вычисление суммы в копилку
        round_up = ((number + step - 1) // step) * step # получение округлённого числа
        return round_up - number

    count = 0.0
    for item in data_list: # сбор суммы в копилку со всех операций в списке
        count += diff(item.amount, limit)

    return count
