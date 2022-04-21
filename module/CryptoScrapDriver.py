import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# add other support exchange on this dict
exchange_base_url = {"BITKUB": "https://www.bitkub.com"}


class CryptoScrapDriver:
    def __init__(self) -> None:
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)

    def __is_coin_listed_on_exchange__(self, exchange: str, symbol: str) -> bool:
        exchange = exchange.upper()
        if exchange == "BITKUB":
            self.driver.get(exchange_base_url[exchange])
            return len(re.findall(symbol, self.driver.page_source)) != 0

        ########################################
        # implement other exchange logic here #
        ########################################

        return False

    def __price_to_float__(self, price_string: str) -> float:
        return float(price_string.replace(',', ''))

    def get_price_by_exchange(self, exchange: str, symbol: str) -> dict:
        try:
            if exchange.upper() not in exchange_base_url.keys():
                raise Exception(f'Exchange({exchange}) is not support')
            if not self.__is_coin_listed_on_exchange__(exchange, symbol):
                raise Exception(f'Symbol({symbol}) is not found')

            fetch_url = exchange_base_url[exchange]
            if exchange == "BITKUB":
                fetch_url += f"/market/{symbol}"
                self.driver.get(fetch_url)
                currentcy_tag = re.findall(
                    f'<span>(THB|USD)/{symbol}', self.driver.page_source)[0]
                currency = re.findall('(THB|USD)', currentcy_tag)[0]
                price_tag = re.findall(
                    '<div class="textright market__stat-value text--green"><span>[0-9,.]+', self.driver.page_source)[0]
                price = re.findall('[0-9,.]+', price_tag)[0]
                return {'symbol': symbol, 'price': self.__price_to_float__(price), 'currency': currency, 'exchange': exchange}

            ########################################
            # implement other exchange logic here #
            ########################################

        except Exception as error:
            return {'error': str(error)}
