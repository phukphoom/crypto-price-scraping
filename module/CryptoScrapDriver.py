import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# add other support exchange on this dict
exchange_base_url = {"BITKUB": "https://www.bitkub.com",
                     "SATANG": "https://satangcorp.com",
                     "BINANCE": "https://www.binance.com",
                     "BITAZZA": "https://trade.bitazza.com"}


class CryptoScrapDriver:
    def __init__(self) -> None:
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)

    def __price_to_float__(self, price_string: str) -> float:
        return float(price_string.replace(',', ''))

    def __log_html_on_file__(self, html_string: str) -> None:
        log_file = open("fetch_source.html", "w")
        log_file.write(html_string)
        log_file.close()

    def get_all_price_by_exchange(self, exchange: str) -> list or dict:
        if exchange.upper() not in exchange_base_url.keys():
            raise Exception(f'Exchange({exchange}) is not support')

        fetch_url = exchange_base_url[exchange]
        if exchange == "BITKUB":
            self.driver.get(fetch_url)

            coin_names = re.findall(
                'data-currency="[(0-9)|(A-Z)]+"', self.driver.page_source)
            coin_names = re.findall('[(0-9)|(A-Z)]+', ''.join(coin_names))

            coin_prices = re.findall(
                '>[0-9,.]+ \(<i class="fa fa-caret', self.driver.page_source)
            coin_prices = re.findall(
                '[0-9,.]+', ''.join(coin_prices))

        elif exchange == "SATANG":
            fetch_url += '/exchange/en'
            self.driver.get(fetch_url)

            coin_names = re.findall(
                '>[(0-9)|(A-Z)]+/</span>', self.driver.page_source)
            coin_names = re.findall('[(0-9)|(A-Z)]+', ''.join(coin_names))

            coin_prices = re.findall(
                'NKpQ">[0-9,.]+</span>', self.driver.page_source)
            coin_prices = re.findall(
                '[0-9,.]+', ''.join(coin_prices))

        elif exchange == "BINANCE":
            fetch_url += '/en/markets'
            self.driver.get(exchange_base_url[exchange])
            self.driver.add_cookie(
                {"name": "userPreferredCurrency", "value": "THB_USD", "path": "/", "domain": ".binance.com"})
            self.driver.get(fetch_url)

            coin_names = re.findall(
                'rgv">[(0-9)|(A-Z)]+</div>', self.driver.page_source)
            coin_names = re.findall('[(0-9)|(A-Z)]+', ''.join(coin_names))

            coin_prices = re.findall(
                'css-ovtrou">฿[0-9,.]+</div>', self.driver.page_source)
            coin_prices = re.findall(
                '[0-9,.]+', ''.join(coin_prices))

        elif exchange == "BITAZZA":
            fetch_url += '/th/exchange'
            self.driver.get(fetch_url)
            self.driver.implicitly_wait(3)
            element = self.driver.find_element_by_css_selector(
                "button.instrument-selector__trigger")
            element.click()
            self.driver.implicitly_wait(3)

            coin_names = re.findall(
                '">[(0-9)|(A-Z)]+/', self.driver.page_source)
            coin_names = re.findall('[(0-9)|(A-Z)]+', ''.join(coin_names))

            coin_prices = re.findall(
                '<div class="flex-table__column instrument-selector-popup__column instrument-selector-popup__column--price"><div>[0-9,.]+</div></div>', self.driver.page_source)
            coin_prices = re.findall(
                '[0-9,.]+', ''.join(coin_prices))

        ########################################
        # implement other exchange logic here #
        ########################################

        if len(coin_names) != len(coin_prices):
            raise Exception(
                f"({exchange}) : bug on regEx \(!!˚☐˚)/")

        coin_datas = []
        for i in range(0, len(coin_names)):
            coin_datas.append(
                {"symbol": coin_names[i], "price": self.__price_to_float__(coin_prices[i])})

        return coin_datas

    def get_all_crypto_datas(self) -> list or dict:
        crypto_datas = []
        for exchange in exchange_base_url.keys():
            try:
                crypto_datas.append(
                    {"exchange": exchange, "data": self.get_all_price_by_exchange(exchange)})
            except Exception:
                crypto_datas.append(
                    {"exchange": exchange, "data": []})

        return crypto_datas

    def get_all_support_symbols(self) -> list or dict:
        support_symbols_datas = []
        for exchange in exchange_base_url.keys():
            try:
                crypto_list = self.get_all_price_by_exchange(exchange)
            except Exception:
                crypto_list = []

            for data in crypto_list:
                if data['symbol'] not in support_symbols_datas:
                    support_symbols_datas.append(data['symbol'])

        return support_symbols_datas
