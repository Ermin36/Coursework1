import datetime as dt
import math
import pandas as pd
from collections import Counter


class Operation:
    """Класс одной операции"""
    __slots__ = ('date', 'card_number', 'status', 'amount', 'currency_name', 'cashback', 'category', 'mcc', 'description', 'bonus')
    date: dt.datetime
    card_number: str
    status: str
    amount: float
    currency_name: str
    cashback: float
    category: str
    mcc: float
    description: str
    bonus: int

    def __init__(self, date: dt.datetime, card_number: str, status: str, amount: float,
                 currency_name: str, cashback: float, category: str, mcc: float, description: str, bonus: int):
        self.date = date
        self.card_number = card_number
        self.status = status
        self.amount = amount
        self.currency_name = currency_name
        self.cashback = round(amount / 100, 2) + cashback
        self.category = category
        self.mcc = mcc
        self.description = description
        self.bonus = bonus
        pass

    @property
    def json(self) -> dict:
        """
        Возвращает первоначальный словарь
        :return: dict
        """
        return {
            'Дата операции': self.date.strftime("%d.%m.%Y %H:%M:%S"),
            'Номер карты': self.card_number,
            'Статус': self.status,
            'Сумма операции': -self.amount,
            'Валюта операции': self.currency_name,
            'Кэшбэк': self.cashback,
            'Категория': self.category,
            'MCC': self.mcc,
            'Описание': self.description,
            'Бонусы (включая кэшбэк)': self.bonus
        }

    @classmethod
    def new_operation_as_dict(cls, operation_dict: dict) -> 'Operation':
        date = operation_dict.get("Дата операции", "")
        data = {
            'date': dt.datetime.strptime(date, "%d.%m.%Y %H:%M:%S") if date != "" else dt.datetime.now(),
            'card_number': str(operation_dict.get("Номер карты", "nan")),
            'status': operation_dict.get("Статус", "None"),
            'amount': round(operation_dict.get("Сумма операции", 0.0) * -1, 2),
            'currency_name': operation_dict.get("Валюта операции", ""),
            'cashback': operation_dict.get("Кэшбэк", 0.0) if not math.isnan(float(operation_dict.get("Кэшбэк", 0.0))) else 0.0,
            'category': operation_dict.get("Категория", ""),
            'mcc': operation_dict.get("MCC", 0.0),
            'description': operation_dict.get("Описание", ""),
            'bonus': operation_dict.get("Бонусы (включая кэшбэк)", 0)
        }
        return cls(**data)

    @property
    def info(self) -> dict:
        """Функция возвращает краткую информацию об операции"""
        return {
            "date": self.date.strftime("%d.%m.%Y"),
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

class Operations:
    """Класс списка операций со всеми функциями"""
    __operation_list: list[Operation] = []

    def __init__(self, data_list: list[Operation] | 'Operations' | None = None):
        if data_list is not None:
            if isinstance(data_list, list):
                self.__operation_list = data_list
            elif isinstance(data_list, Operations):
                self.__operation_list = data_list.operation_list

    def __len__(self) -> int:
        return len(self.__operation_list)

    def __getitem__(self, item: int) -> Operation:
        return self.__operation_list[item]

    @classmethod
    def read_xlsx(cls, path: str) -> 'Operations':
        """
        Чтение операций из файла xlsx
        :param path: Путь к файлу
        :return: Класс Operations
        """
        try:
            file = pd.read_excel(path)
            columns = file.columns
            data_list = Operations()
            for index in range(len(file)):
                item = {}
                for column in columns:
                    item[column] = file[column][index]

                data_list.add(Operation.new_operation_as_dict(item))

            return data_list
        except FileNotFoundError:
            data = Operations()
            return data

    @classmethod
    def read_dataframe(cls, operations: pd.DataFrame) -> 'Operations':
        columns = operations.columns
        data_list = Operations()
        for index in range(len(operations)):
            item = {}
            for column in columns:
                item[column] = operations[column][index]
            data_list.add(Operation.new_operation_as_dict(item))
        return data_list

    def add(self, operation: Operation) -> None:
        """Добавляет операцию в массив"""
        self.__operation_list.append(operation)

    @property
    def operation_list(self) -> list[Operation]:
        """Возвращает список операций"""
        return self.__operation_list

    @property
    def dataframe(self) -> pd.DataFrame:
        """Получение DataFrame из данных"""
        data_list: list[dict] = [item.json for item in self.__operation_list]

        return pd.DataFrame(data_list)

    def sort_by_status(self, status: str) -> None:
        """Сортировка массива по параметру status"""
        sort_list = [item for item in self.__operation_list if item.status == status]

        self.__operation_list = sort_list

    def sort_by_date(self, date: str | None = None) -> None:
        """Сортировка массива по параметру date с начала месяца по текущую дату"""
        date_obj = dt.datetime.strptime(date, "%Y.%m.%d %H:%M:%S") if date is not None else dt.datetime.now()
        date_start = date_obj.replace(day=1)
        sort_list = [item for item in self.__operation_list if date_start <= item.date <= date_obj]

        self.__operation_list = sort_list

    def sort_by_amount(self, reverse: bool = False) -> None:
        """
        Сортировка массива по параметру amount
        :param reverse: по убыванию или возрастанию. По умолчанию сортирует по убыванию
        """
        sort_list = sorted(self.__operation_list, key=lambda x: x.amount, reverse=reverse)

        self.__operation_list = sort_list

    def sort_by_number_card(self, card_number: str) -> None:
        """Сортировка операции по номеру карты"""
        sort_list = [item for item in self.__operation_list if item.card_number == card_number]

        self.__operation_list = sort_list

    @property
    def cards(self) -> list[str]:
        """Получения списка всех карт из операций"""
        data_list = Counter(item.card_number for item in self.operation_list if item.card_number != "nan")

        out = []
        for _, (card, _) in enumerate(data_list.items()):
            out.append(card)

        return out