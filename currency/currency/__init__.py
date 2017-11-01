import requests
import json

class CurrencyUnavailableError(Exception):
    # def __init__(self):
    #     self.value = value
    def __str__(self):
        return repr('currency rate unavailable')

class Http_proxy:
    def __init__(self, connect_timeout = 5):
        self._connect_timeout = 5
        self._session = requests.Session()
        self._session.keep_alive = False
    def get(self, uri):
        try:
            response = self._session.get(uri, timeout = self._connect_timeout);
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects):
            raise CurrencyUnavailableErroe()
        else:
            return response

class Yahoo_provider:
    def __init__(self, currency_from, currency_to, connect_timeout = 5):
        self._proxy = Http_proxy(connect_timeout)
        self._currency_from = currency_from
        self._currency_to = currency_to
    
    def __build_uri__(self):
        base_url = "https://query.yahooapis.com/v1/public/yql"
        query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("'+self._currency_from+self._currency_to+'")'
        return base_url + "?q=" + query + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    def get_exchange_rate(self):
        try:
            response = self._proxy.get(self.__build_uri__())
            rate = response.json()['query']['results']['rate']['Rate']
        except (ValueError, KeyError, TypeError, CurrencyUnavailableError):
            raise CurrencyUnavailableError()
        else:
            return response

class Fixer_provider:
    def __init__(self, currency_from, currency_to, connect_timeout = 5):
        self._proxy = Http_proxy(connect_timeout)
        self._currency_from = currency_from
        self._currency_to = currency_to
    
    def __build_uri__(self):
        uri = 'http://api.fixer.io/latest?base={}&symbols={}'
        return uri.format(self._currency_from, self._currency_to)

    def get_exchange_rate(self):
        try:
            response = self._proxy.get(self.__build_uri__())
            rate = response.json()["rates"][self._currency_to]
        except (ValueError, KeyError, TypeError, CurrencyUnavailableError):
            raise CurrencyUnavailableError()
        else:
            return rate

def convert_currency(currency_from, currency_to, amount, connect_timeout = 5):
    converter = fixer_provider(currency_from, currency_to, connect_timeout)
    return amount * converter.get_exchange_rate()
