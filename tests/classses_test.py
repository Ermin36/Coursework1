from src.classes import Operations, Operation
from pytest_mock import MockerFixture
import pytest
import datetime as dt
import pandas as pd


class TestClassOperation:

    @pytest.fixture
    def operation(self) -> Operation:
        return Operation(
            dt.datetime(year=2021, month=12, day=5), "Test", "OK", 1200.0, "RUB", 0.0, "Test", 53, "testing", 2
        )

    def test_init(self, operation: Operation) -> None:
        """Тест инициализации функции"""
        assert operation.date == dt.datetime(year=2021, month=12, day=5)
        assert operation.card_number == "Test"
        assert operation.status == "OK"
        assert operation.amount == 1200
        assert operation.currency_name == "RUB"
        assert operation.cashback == 12
        assert operation.category == "Test"
        assert operation.mcc == 53
        assert operation.description == "testing"
        assert operation.bonus == 2

    def test_json(self, operation: Operation) -> None:
        """Тест функции получения json данных"""
        data_dict = {
            "Сумма операции": -1200.0,
            "Бонусы (включая кэшбэк)": 2,
            "Номер карты": "Test",
            "Кэшбэк": 12.0,
            "Категория": "Test",
            "Валюта операции": "RUB",
            "Дата операции": "05.12.2021 00:00:00",
            "Описание": "testing",
            "MCC": 53,
            "Статус": "OK",
        }
        assert operation.json == data_dict

    def test_operation_as_dict(self) -> None:
        """Тест создание класса из словаря"""
        data_dict = {
            "Сумма операции": -120,
            "Бонусы (включая кэшбэк)": 3,
            "Номер карты": "*7197",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "Валюта операции": "RUB",
            "Дата операции": "07.12.2021 00:00:00",
            "Описание": "Колхоз",
            "MCC": 5411.0,
            "Статус": "OK",
        }
        operation = Operation.new_operation_as_dict(data_dict)
        assert operation.date == dt.datetime(year=2021, month=12, day=7)
        assert operation.card_number == "*7197"
        assert operation.status == "OK"
        assert operation.amount == 120.0
        assert operation.currency_name == "RUB"
        assert operation.cashback == 1.2
        assert operation.category == "Супермаркеты"
        assert operation.mcc == 5411.0
        assert operation.description == "Колхоз"
        assert operation.bonus == 3

    def test_get_info(self, operation: Operation) -> None:
        """Тест получения информации об операции"""
        result = operation.info

        assert result == {'amount': 1200.0,
                          'category': 'Test',
                          'date': '05.12.2021',
                          'description': 'testing'}


class TestClassOperations:

    @pytest.fixture
    def operations(self) -> Operations:
        data_dict = {
            "Сумма операции": -120,
            "Бонусы (включая кэшбэк)": 3,
            "Номер карты": "*7197",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "Валюта операции": "RUB",
            "Дата операции": "07.12.2021 00:00:00",
            "Описание": "Колхоз",
            "MCC": 5411.0,
            "Статус": "OK",
        }
        data_dict2 = {
            "Сумма операции": -715,
            "Бонусы (включая кэшбэк)": 3,
            "Номер карты": "*7192",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "Валюта операции": "RUB",
            "Дата операции": "24.12.2021 00:00:00",
            "Описание": "Колхоз",
            "MCC": 5411.0,
            "Статус": "TEST",
        }
        operation1 = Operation.new_operation_as_dict(data_dict)
        operation2 = Operation.new_operation_as_dict(data_dict2)
        return Operations([operation1, operation2])

    def test_init(self, operations: Operations) -> None:
        """Тест функции инициализации"""
        result1 = Operations()
        assert result1._Operations__operation_list == []

        assert len(operations._Operations__operation_list) == 2

        test = Operations(operations)

        assert len(test) == 2

    def test_len(self, operations: Operations) -> None:
        """Тест получения длины"""
        assert len(operations) == 2

        new_operations = Operations()

        assert len(new_operations) == 0

    def test_getitem(self, operations:Operations) -> None:
        """Тест получения объекта"""
        operation = operations[0]
        assert isinstance(operation, Operation)
        assert operation.card_number == "*7197"

    def test_read_xlsx(self, mocker: MockerFixture) -> None:
        """Тест функции чтения xlsx файла"""

        result1 = Operations.read_xlsx('test/1.xlsx')

        assert len(result1) == 0
        assert isinstance(result1, Operations)

        data_file_df = pd.DataFrame(
            {
                'Дата операции':['12.03.2021 15:14:03'],
                'Номер карты':['*5432'],
                'Статус':['OK'],
                'Сумма операции':[135.1],
                'Валюта операции':['RUB'],
                'Кэшбэк': [0.0],
                'Категория': ['test'],
                'MCC': [0.0],
                'Описание': ['testing'],
                'Бонусы (включая кэшбэк)':[0]
            }
        )
        read_mock = mocker.patch('pandas.read_excel')
        read_mock.return_value = data_file_df

        result2 = Operations.read_xlsx('./data/test.xlsx')

        assert isinstance(result2, Operations)
        assert len(result2) == 1
        assert isinstance(result2[0], Operation)
        read_mock.assert_called_once_with('./data/test.xlsx')

    def test_read_dataframe(self) -> None:
        """Тест функции преобразования DataFrame в Operations"""
        data_file_df = pd.DataFrame(
            {
                'Дата операции': ['12.03.2021 15:14:03'],
                'Номер карты': ['*5432'],
                'Статус': ['OK'],
                'Сумма операции': [135.1],
                'Валюта операции': ['RUB'],
                'Кэшбэк': [0.0],
                'Категория': ['test'],
                'MCC': [0.0],
                'Описание': ['testing'],
                'Бонусы (включая кэшбэк)': [0]
            }
        )
        operations = Operations.read_dataframe(data_file_df)
        assert len(operations) == 1
        assert isinstance(operations[0], Operation)
        assert operations[0].card_number == '*5432'

    def test_add_operation(self, operations: Operations) -> None:
        """Тест функции добавления операции"""
        data_dict = {
            "Сумма операции": -120,
            "Бонусы (включая кэшбэк)": 3,
            "Номер карты": "*7195",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "Валюта операции": "RUB",
            "Дата операции": "07.12.2021 00:00:00",
            "Описание": "Колхоз",
            "MCC": 5411.0,
            "Статус": "OK",
        }
        result = Operations(operations.operation_list)
        assert len(result) == 2

        operation1 = Operation.new_operation_as_dict(data_dict)
        result.add(operation1)
        assert len(result) == 3

    def test_get_operation_list(self, operations: Operations) -> None:
        """Тест функции получения списка операций"""
        result = operations.operation_list

        assert isinstance(result, list)
        assert isinstance(result[0], Operation)

    def test_dataframe(self) -> None:
        """Тест функции получения DataFrame"""
        data_file_df = pd.DataFrame(
            {
                'Дата операции': ['12.03.2021 15:14:03'],
                'Номер карты': ['*5432'],
                'Статус': ['OK'],
                'Сумма операции': [135.1],
                'Валюта операции': ['RUB'],
                'Кэшбэк': [0.0],
                'Категория': ['test'],
                'MCC': [0.0],
                'Описание': ['testing'],
                'Бонусы (включая кэшбэк)': [0]
            }
        )
        operations = Operations.read_dataframe(data_file_df)
        result = operations.dataframe

        assert list(result.columns) == list(data_file_df.columns)

    def test_sort_by_status(self, operations: Operations) -> None:
        """Тест функции сортировки по статусу"""
        result1 = Operations(operations.operation_list)
        result1.sort_by_status('TEST')

        assert len(result1) == 1
        del result1

        result1 = Operations(operations.operation_list)
        result1.sort_by_status('OK')

        assert len(result1) == 1
        assert isinstance(result1[0], Operation)

    def test_sort_by_date(self, operations: Operations) -> None:
        """Тест функции сортировки по дате"""
        result1 = Operations(operations)
        result1.sort_by_date('2021.12.15 00:00:00')

        assert len(result1) == 1
        del result1

        result1 = Operations(operations)
        result1.sort_by_date('2021.12.03 00:00:00')

        assert len(result1) == 0

    def test_sort_by_amount(self, operations: Operations) -> None:
        """Тест сортировки по сумме операции"""
        result = Operations(operations)
        result.sort_by_amount(True)

        assert len(result) == 2
        assert result[0].card_number == '*7192'

    def test_sort_by_number_card(self, operations: Operations) -> None:
        """Тест сортировки по дате"""
        result = Operations(operations)
        result.sort_by_number_card('*7197')

        assert len(result) == 1
        assert result[0].card_number == '*7197'

    def test_get_cards(self, operations: Operations) -> None:
        """Тест получения номеров карт"""
        test_operations = Operations(operations)

        result = test_operations.cards

        assert isinstance(result, list)
        assert len(result) == 2
        assert result == ['*7197', '*7192']