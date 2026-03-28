import pytest
from pytest_mock import MockerFixture

from src.classes import Operation, Operations
from src.views import get_greeting, get_card_data, get_currency_rates, get_stock_prices, get_json_out


class TestFuncGetGreeting:

    @pytest.mark.parametrize(
        "date_str, out",
        [
            ("2021.12.17 11:44:15", "Доброе утро!"),
            ("2021.12.12 13:15:00", "Добрый день!"),
            ("2021.12.21 19:00:00", "Добрый вечер!"),
        ],
    )
    def test_get_greeting(self, date_str: str, out: str) -> None:
        """Тест правильной выдачи приветствия"""
        result = get_greeting(date_str)
        assert result == out


class TestFuncGetCardData:

    def test_get_main_data_operations(self, mocker: MockerFixture) -> None:
        """Тест нормально отработки получения данных об операциях"""

        read_mock = mocker.patch("src.views.Operations.read_xlsx")
        read_mock.return_value = read_mock.return_value = Operations(
            [
                Operation.new_operation_as_dict(
                    {
                        "Сумма операции": -160.89,
                        "Бонусы (включая кэшбэк)": 3,
                        "Номер карты": "*7197",
                        "Кэшбэк": 0,
                        "Категория": "Супермаркеты",
                        "Валюта операции": "RUB",
                        "Дата операции": "07.12.2021 16:44:00",
                        "Описание": "Колхоз",
                        "MCC": 5411.0,
                        "Статус": "OK",
                    }
                ),
                Operation.new_operation_as_dict(
                    {
                        "Сумма операции": -235.12,
                        "Бонусы (включая кэшбэк)": 2,
                        "Номер карты": "*7267",
                        "Кэшбэк": 0,
                        "Категория": "Супермаркеты",
                        "Валюта операции": "RUB",
                        "Дата операции": "11.12.2021 16:44:00",
                        "Описание": "Колхоз",
                        "MCC": 5411.0,
                        "Статус": "OK",
                    }
                ),
            ]
        )

        result1, result2 = get_card_data("2021.12.21 19:00:00", "../data/operations.xlsx")

        assert result1 == [
            {"cashback": 1.61, "last_digits": "*7197", "total_spent": 160.89},
            {"cashback": 2.35, "last_digits": "*7267", "total_spent": 235.12},
        ]
        assert result2 == [
            {"amount": 235.12, "category": "Супермаркеты", "date": "11.12.2021", "description": "Колхоз"},
            {"amount": 160.89, "category": "Супермаркеты", "date": "07.12.2021", "description": "Колхоз"},
        ]
        read_mock.assert_called_once_with('../data/operations.xlsx')


class TestFuncGetCurrencyRates:

    def test_valid_get_currency_rates(self, mocker: MockerFixture) -> None:
        """Тест функции, если запрос прошёл"""
        os_mock = mocker.patch("os.getenv")
        os_mock.return_value = "5534"
        read_mock = mocker.patch("src.views.read_json")
        read_mock.return_value = {"user_currencies": ["5", "3"]}
        get_mock = mocker.patch("requests.get")
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = {"rates": {"test": 3, "code": 5}}

        result = get_currency_rates("../user_settings.json")

        assert result[0]["currency"] == "test"
        assert result[1]["rate"] == 5
        os_mock.assert_called_once_with("API_KEY_CURRENCY")
        read_mock.assert_called_once_with("../user_settings.json")
        get_mock.assert_called_once()

    def test_invalid_get_currency_rates(self, mocker: MockerFixture) -> None:
        """Тест функции, если запрос не прошёл"""
        os_mock = mocker.patch("os.getenv")
        os_mock.return_value = "5534"
        read_mock = mocker.patch("src.views.read_json")
        read_mock.return_value = {"user_currencies": ["5", "3"]}
        get_mock = mocker.patch("requests.get")
        get_mock.return_value.status_code = 100

        result = get_currency_rates("../user_settings.json")

        assert result == []
        os_mock.assert_called_once_with("API_KEY_CURRENCY")
        read_mock.assert_called_once_with("../user_settings.json")
        get_mock.assert_called_once()


class TestFuncGetStockPrices:

    def test_valid_get_stock_prices(self, mocker: MockerFixture) -> None:
        """Тест функции, если запрос прошёл"""
        os_mock = mocker.patch("os.getenv")
        os_mock.return_value = "5534"
        read_mock = mocker.patch("src.views.read_json")
        read_mock.return_value = {"user_stocks": ["HTR"]}
        get_mock = mocker.patch("requests.get")
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = {"Time Series (Daily)": {"TESTER": {"1. open": 15.2}}}

        result = get_stock_prices("../user_settings.json")

        assert result == [{"stock": "HTR", "price": 15.2}]
        os_mock.assert_called_once_with("API_KEY_STOCK")
        read_mock.assert_called_once_with("../user_settings.json")
        get_mock.assert_called_once()

    def test_invalid__get_stock_prices(self, mocker: MockerFixture) -> None:
        """Тест функции, если запрос не прошёл"""
        os_mock = mocker.patch("os.getenv")
        os_mock.return_value = "5534"
        read_mock = mocker.patch("src.views.read_json")
        read_mock.return_value = {"user_stocks": ["HTR"]}
        get_mock = mocker.patch("requests.get")
        get_mock.return_value.status_code = 100

        result = get_stock_prices("../user_settings.json")

        assert result == []
        os_mock.assert_called_once_with("API_KEY_STOCK")
        read_mock.assert_called_once_with("../user_settings.json")
        get_mock.assert_called_once()


class TestFuncGetJsonOut:

    def test_get_json_out(self, mocker: MockerFixture) -> None:
        """Тест правильной работы функции получения json ответа"""
        greeting_mock = mocker.patch('src.views.get_greeting')
        greeting_mock.return_value = '5'

        card_mock = mocker.patch('src.views.get_card_data')
        card_mock.return_value = ([2, 1], [3, 4])

        currency_mock = mocker.patch('src.views.get_currency_rates')
        currency_mock.return_value = [1, 1]

        stock_mock = mocker.patch('src.views.get_stock_prices')
        stock_mock.return_value = [7, 7]

        result = get_json_out("2021.12.21 19:00:00")

        assert result == {
        "greeting": '5',
        "cards": [2, 1],
        "top_transactions": [3, 4],
        "currency_rates": [1, 1],
        "stock_prices": [7, 7]
        }

        greeting_mock.assert_called_once()
        card_mock.assert_called_once()
        currency_mock.assert_called_once()
        stock_mock.assert_called_once()
