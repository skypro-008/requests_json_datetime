import json
import os
from datetime import datetime

import requests

CURRENCY_RATES_FILE = "currency_rates.json"
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')


def get_currency_rate(currency: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={'apikey': API_KEY})
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def save_to_json(data: dict) -> None:
    """Сохраняет данные в json файл"""

    with open(CURRENCY_RATES_FILE, "a") as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data_list, json_file)


def main():
    """
    Основная функция программы. Получает от пользователя название валюты USD или EUR,
    получает и выводит на экран текущий курс валюты от API. Записывает данные в json файл.
    """
    while True:
        currency = input("Введите название валюты (USD или EUR): ").upper()
        if currency not in ["USD", "EUR"]:
            print("Некорректный ввод")
            continue

        rate = get_currency_rate(currency)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Курс {currency} к рублю: {rate:.2f}")
        data = {"currency": currency, "rate": rate, "timestamp": timestamp}
        save_to_json(data)

        choice = input("Выберите действие: (1 - продолжить, 2 - выйти) ")
        if choice == "1":
            continue
        elif choice == "2":
            break
        else:
            print("Некорректный ввод")


if __name__ == "__main__":
    main()
