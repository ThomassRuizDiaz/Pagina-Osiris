import requests
import json

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = 'e69333c6-484c-4456-87e9-0f8c9f51b9b1'
        self.base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"
        self.headers = {"X-CMC_PRO_API_KEY": 'e69333c6-484c-4456-87e9-0f8c9f51b9b1'}
    
    def get_data(self, symbol, start_date, end_date):
        url = f"{self.base_url}/ohlcv/historical"
        params = {"symbol": symbol, "time_start": start_date, "time_end": end_date}
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            return data["data"]
        else:
            raise Exception("Error en la solicitud de datos")
            
    def get_info(self, symbol):
        url = f"{self.base_url}/info"
        params = {"symbol": symbol}
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            info = data["data"][symbol]
            market_cap = info["quote"]["USD"]["market_cap"]
            volume_24h = info["quote"]["USD"]["volume_24h"]
            circulating_supply = info["circulating_supply"]
            total_supply = info["total_supply"]
            return {"market_cap": market_cap, "volume_24h": volume_24h, "circulating_supply": circulating_supply, "total_supply": total_supply}
        else:
            raise Exception("Error en la solicitud de datos")

fetcher = DataFetcher(api_key='e69333c6-484c-4456-87e9-0f8c9f51b9b1')

