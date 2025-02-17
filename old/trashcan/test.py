from investpy import stocks


class Engine:


    def __init__(
        self: 'Engine'
    ) -> None:
        pass

    def get_stocks(
        self: 'Engine'
    ) -> None:

    
# Get B3 tickers
b3_stocks = stocks.get_stocks(country='brazil')
tickers = b3_stocks['symbol'].to_list()

print(f"Total B3 Tickers: {len(tickers)}")
print('IVVB11' in tickers)