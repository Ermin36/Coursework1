from unittest.mock import MagicMock, mock_open
from pytest_mock import MockerFixture
from src.utils import read_json


class TestReadJSON:

    def test_valid_read_json(self, mocker: MockerFixture) -> None:
        """Тест функции чтения файла JSON"""
        file_mock: MagicMock = mocker.patch("builtins.open", new_callable=mock_open, read_data="test")

        read_mock = mocker.patch("src.utils.json.load")
        read_mock.return_value = {"user": 5}

        result = read_json("./tester/data.json")

        assert result["user"] == 5
        file_mock.assert_called_once()
        read_mock.assert_called_once()

    def test_invalid_read_json(self) -> None:
        """Тест при не нахождении файла"""
        result = read_json("./testing/data.json")

        assert result == {}
