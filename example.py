from module import CryptoScrapDriver, exchange_base_url

scrap_driver = CryptoScrapDriver()

print(scrap_driver.get_all_support_symbols())
print(scrap_driver.get_all_crypto_datas())