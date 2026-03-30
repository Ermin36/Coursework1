from functools import wraps
import pandas as pd
from typing import Optional
import datetime as dt
from typing import Callable, Any
from pathlib import Path

from src import Operations


def decor_reports(func: Callable) -> Callable:
    """Декоратор записи данных отчётов в файл test.rep"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result: pd.DataFrame = func(*args, **kwargs)
        path = Path('./reports/test.rep')
        path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(path, sep='|', index=False)
        return result
    return wrapper


def decor_reports_arg(file_name: str) -> Callable:
    """
    Декоратор записи данных отчётов в файл
    :param file_name: имя файла
    :return: декоратор
    """
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            result.to_csv(f'../reports/{file_name}.rep', sep='|', index=False)
            return result
        return inner
    return wrapper

@decor_reports
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция сбора трат по категории за заданную дату времени
    :param transactions: список транзакций
    :param category: категория по которой происходит сортировка
    :param date: дата в формате YYYY.MM.DD
    :return: траты по категории
    """

    if date is None:
        end_date = pd.Timestamp.now()
    else:
        datetime_date =  dt.datetime.strptime(date,'%Y.%m.%d')
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


