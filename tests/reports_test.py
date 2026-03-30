import pandas as pd
from pytest_mock import MockerFixture

from src.reports import spending_by_category, decor_reports, decor_reports_arg

test_data = pd.DataFrame(
    {
        "Дата операции": ["12.03.2021 15:14:03", "15.01.2021 00:00:00", "14.02.2021 00:00:00"],
        "Номер карты": ["*5432", "*7492", "*5432"],
        "Статус": ["OK", "OK", "OK"],
        "Сумма операции": [-135.1, -124.2, -523.1],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Кэшбэк": [0.0, 0.0, 0.0],
        "Категория": ["Магазин", "Магазин", "Test"],
        "MCC": [44.0, 51.1, 15.2],
        "Описание": ["testing", "Покупка продуктов", "Прочее"],
        "Бонусы (включая кэшбэк)": [0, 0, 0],
    }
)


class TestModuleReports:

    def test_spending_by_category(self) -> None:
        """Тестирование функции сортировки трат по категории"""
        result = spending_by_category(test_data, "Магазин", "2021.03.29")

        assert result.shape[0] == 2
        assert result["Категория"][0] == "Магазин"
        assert result["Описание"][0] == "testing"
        assert result["Описание"][1] == "Покупка продуктов"

    def test_decor_reports(self, mocker: MockerFixture) -> None:
        """Тест декоратора без аргументов"""
        write_mock = mocker.patch('pandas.DataFrame.to_csv')
        write_mock.return_value = 0
        @decor_reports
        def func() -> pd.DataFrame:
            return pd.DataFrame({
                'arg1': [4, 1],
                'arg2': [2, 3]
            })

        result = func()
        assert result['arg1'][0] == 4
        write_mock.assert_called_once()

    def test_decor_reports_arg(self, mocker: MockerFixture) -> None:
        """Тест декоратора с аргументами"""
        write_mock = mocker.patch('pandas.DataFrame.to_csv')
        write_mock.return_value = 0

        @decor_reports_arg('data')
        def func() -> pd.DataFrame:
            return pd.DataFrame({
                'arg1': [4, 1],
                'arg2': [2, 3]
            })

        result = func()
        assert result['arg1'][0] == 4
        write_mock.assert_called_once_with('../reports/data.rep', sep='|', index=False)

