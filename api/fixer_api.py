import os
import requests

SUPPORTED_CURRENCIES = {}
FIXER_API_KEY = os.getenv('FIXER_API_KEY')


def fetch_supported_currencies():
    global SUPPORTED_CURRENCIES
    fixer_url = "http://data.fixer.io/api/symbols"
    response = requests.get(fixer_url, params={"access_key": FIXER_API_KEY})

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            SUPPORTED_CURRENCIES = {code: name for code, name in data["symbols"].items() if code != "USD" and code != "RUB"}
        else:
            print("Failed to fetch supported currencies.")
    else:
        print("Failed to connect to Fixer API.")


def get_exchange_rate(base_currency: str, target_currency: str):
    API_KEY = "bde8dfdb2aa37bb425f07c111aabe2b5"
    BASE_URL = "http://data.fixer.io/api/latest"
    response = requests.get(BASE_URL, params={
        "access_key": API_KEY,
        "base": base_currency,
        "symbols": target_currency
    })

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["rates"].get(target_currency)
    return None


def get_supported_currencies():
    return SUPPORTED_CURRENCIES
