import datetime as dt
import os

import requests
from dotenv import load_dotenv

from src.classes import Operations, Operation
from src.utils import read_json


def get_greeting(date_str: str) -> str:
    """
    Возвращает приветствие в зависимости от даты
    :param date_str: дата в формате ГГ.ММ.ДД ЧЧ.ММ.СС
    :return: приветствие
    """

    date_obj = dt.datetime.strptime(date_str, "%Y.%m.%d %H:%M:%S")

    if date_obj.hour < 12:
        date_msg = "Доброе утро!"
    elif date_obj.hour < 18:
        date_msg = "Добрый день!"
    else:
        date_msg = "Добрый вечер!"

    return date_msg

def get_card_data(date_str: str, path: str) -> tuple[list[dict], list[dict]]:
    """
    Функция получения данных о картах и топ операций
    :param date_str: время
    :param path: путь к файлу с транзакциями
    :return: информация по картам, топ операций
    """

    operations = Operations.read_xlsx(path)
    operations.sort_by_status("OK")
    operations.sort_by_date(date_str)
    cards = operations.cards

    cards_data: list[dict] = []
    for card in cards:
        card_operations = Operations(operations.operation_list)
        card_operations.sort_by_number_card(card)
        card_list = card_operations.operation_list
        card_sum: float = round(sum(item.amount for item in card_list), 2)
        card_cashback: float = round(card_sum / 100, 2)
        out_dict: dict = {"last_digits": card, "total_spent": card_sum, "cashback": card_cashback}
        if card_sum > 0.0:
            cards_data.append(out_dict)
        del card_operations

    top_operations = Operations(operations.operation_list)
    top_operations.sort_by_amount(True)
    top_list = [item.info for item in top_operations.operation_list[:5]]

    return cards_data, top_list


def get_currency_rates(path: str) -> list[dict]:
    """
    Внутренняя функция для получения данных о курсе валют
    :return: возвращаете список стоимости валют
    """
    load_dotenv()
    api_key = os.getenv("API_KEY_CURRENCY")
    data = read_json(path)
    currency = data.get("user_currencies", [])
    currency = [str(item) for item in currency]

    input_data = ",".join(currency)
    http_request = f"https://api.apilayer.com/exchangerates_data/live?base=USD&symbols={input_data}"
    header_data = {"apikey": api_key}

    response = requests.get(http_request, headers=header_data)
    status_code = response.status_code
    if status_code != 200:
        return []

    result_json: dict = response.json()
    rates = result_json.get("rates", {})
    out_data = []
    for _, (code, amount) in enumerate(rates.items()):
        out = {"currency": code, "rate": amount}
        out_data.append(out)

    return out_data


def get_stock_prices(path: str) -> list[dict]:
    """
    Внутренняя функция получения стоимости акций
    :return: список стоимости акций
    """
    load_dotenv()
    api_key = os.getenv("API_KEY_STOCK")
    list_stock = read_json(path)
    stocks = list_stock.get("user_stocks", [])

    http_server = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey={api_key}&symbol="
    out_data = []
    for stock in stocks:
        server = http_server + str(stock)
        response = requests.get(server)

        data_json: dict = response.json()
        status_code = response.status_code

        if status_code != 200:
            continue

        item_list = data_json.get("Time Series (Daily)", {})
        key_list = list(item_list.keys())
        if len(key_list) == 0:
            continue

        key = key_list[0]
        price = item_list.get(key, {}).get("1. open", 0.0)
        out = {"stock": stock, "price": price}
        out_data.append(out)

    return out_data


def get_json_out(date_str: str) -> dict:
    """
    Функция возвращает json ответ по данным операция с начала месяца даты по саму дату
    :param date_str: строка даты в формате ГГ.ММ.ДД ЧЧ.ММ.СС
    :return: json ответ
    """

    data_path = "../data/operations.xlsx"
    user_path = "../user_settings.json"

    card_data, top_operation = get_card_data(date_str, data_path)

    return {
        "greeting": get_greeting(date_str),
        "cards": card_data,
        "top_transactions": top_operation,
        "currency_rates": get_currency_rates(user_path),
        "stock_prices": get_stock_prices(user_path)
    }
