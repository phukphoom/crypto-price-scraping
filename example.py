from module import CryptoScrapDriver, exchange_base_url

scrap_driver = CryptoScrapDriver()

crypto_price_datas = []
for exchange in exchange_base_url.keys():
    crypto_price_datas.append(
        {"exchange": exchange, "data": scrap_driver.get_all_price_by_exchange(exchange)})

print(crypto_price_datas)