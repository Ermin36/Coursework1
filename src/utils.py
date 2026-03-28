import json


def read_json(path: str) -> dict:
    """
    Чтение json файла
    :param path: путь к файлу
    :return: возвращает словарь
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            data: dict = json.load(file)
            return data
    except FileNotFoundError as err:
        print(f"Файл не найден {path}\n {err}")
        return {}