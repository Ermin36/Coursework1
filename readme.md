# Курсовая работа №1
___

## Установка

- ### Клонировать репозиторий

    `git clone https://github.com/Ermin36/Coursework1.git`

- ### Подключить необходимые зависимости в проекте

    `from src import *` - Импортирует все зависимости
___

## В данном проекте предоставлены следующие функции

| Функция                                                                                                     | Расположение |
|-------------------------------------------------------------------------------------------------------------|--------------|
| get_json_out(date_str: str) -> dict                                                                         | views.py     |
| investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float                        | services.py  |
| decor_reports(func: Callable) -> Callable                                                                   | reports.py   |
| decor_reports_arg(file_name: str) -> Callable                                                               | reports.py   |
| spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | reports.py   |
___
## Далее будет представлено как их использовать

### Модуль views.py

- `get_json_out(date_str)`
    
    - `date_str: str` - Строка даты в формате `ГГГГ.ММ.ДД чч.мм.сс`

    **ВАЖНО!** Для работы требует API с сайтов [apilayer](https://marketplace.apilayer.com/exchangerates_data-api) и 
    [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

    Внести api-ключ **нужно** в файл `.env` в соответствующие строки

    Данная функция возвращает json ответ в формате `dict`:
    ```
    {
        "greeting": str
        "cards": list[dict],
        "top_transactions": list[dict],
        "currency_rates": list[dict],
        "stock_prices": list[dict]
    } 
    ```
    1. `greeting` - Приветствие зависит от времени переданного в переменной `date_str`
    
    2. `cards` - Список карт и общей суммы затрат по ним. Формат:
        ```
        {
            last_digit: str - номер карты
            total_spent: float - сумма трат по карте
            cashback: float - кэшбэк от суммы трат по карте
        }
        ```
  
    3. `top_transactions` - Список из пяти операций с самой большой суммой трат

    4. `currency_rates` - Курс валют описанных в файле `user_settings.json` в переменной `user_currencies`

    5. `stock_prices` - Стоимость акций из S&P500. Названия акций берётся из `user_settings.json` в переменной `user_stocks`

### Модуль services.py

- `investment_bank(month, transactions, limit)`
 
    - `month: str` - Дата в формате `ГГГГ.ММ.ДД`. Диапазон весь месяц
    - `transactions: list[dict]` - список транзакций
    - `limit: int` - Число к которому округляем. 
    
    Данная функция - это автоматическое накопление средств путём округления
    суммы операций в большую сторону и возвращает их разницу. Возвращаемое значение типа `float`
  
    Пример работы функции: Если сумма операции `246`, а `limit = 100`,
    то округляет к `300` и возвращаемое число будет `54`

### Модуль reports.py

- `spending_by_category(transactions, category, date = None)`
    
    - `transactions: pandas.DataFrame` - список транзакций в формате DataFrame
    - `category: str` - Название категории по которой нужно выдать траты
    - `date: str` - Дата в формате `ГГГГ.ММ.ДД`. Если не передано, то берёт текущую дату

    Данная функция возвращает транзакции за 3 месяца от переданной даты по заданной
    категории. Формат возвращаемых данных `pandas.DataFrame`

- `decor_reports()` - декоратор

    Данный декоратор служит дополнением для функции `spending_by_category`.

    Он записывает результат функции в файле формата `.rep`. Формат данных `csv`.
    Путь к файлу: `./reports/test.rep` - название файла по умолчанию

- `decor_reports_arg(file_name)` - декоратор

    - `file_name: str` - название файла
  
    Данный декоратор такой же, как и `decor_reports`, но с аргументом.

    Он тоже записывает результат функции, но через переменную можно задать название файлу через аргумент
___

### Реализация

- Вы можете взглянуть на реализацию всех функций в файле `./src/main.py`