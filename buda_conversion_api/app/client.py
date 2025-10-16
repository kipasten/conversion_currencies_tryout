from abc import ABC, abstractmethod
import requests
from datetime import datetime, timedelta

class BudaClient(ABC):
    @abstractmethod
    def get_order_book(self, market: str):
        pass

class InMemoryBudaClient(BudaClient):
    def __init__(self, markets):
        self.markets = markets

    def get_order_book(self, market: str):
        return self.markets.get(market)

class RealBudaClient(BudaClient):
    """
    Cliente real que consulta la API pública de Buda.com
    para obtener tickers y libros de órdenes.
    """
    BASE_URL = "https://www.buda.com/api/v2"

    def __init__(self):
        self.markets = {}
        self.last_update = 0


    def request_tickers(self, timeout):
        url = f"{self.BASE_URL}/tickers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        self.last_update = datetime.now()
        
        data = response.json()
        tickers = data.get("tickers", [])
        return tickers

    def refresh_tickers(self):
        """
        Carga todos los tickers desde Buda.com y los transforma en un formato manejable.
        """
        if self.check_time_passed():
            return self.markets
        
        tickers = self.request_tickers(timeout=10)

        self.update_markets(tickers)

        return self.markets
   
    def get_order_book(self, market: str):
        """
        Devuelve el libro de órdenes para un mercado específico.
        """
        url = f"{self.BASE_URL}/markets/{market}/order_book"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "asks": [[float(p), float(q)] for p, q in data["order_book"]["asks"]],
            "bids": [[float(p), float(q)] for p, q in data["order_book"]["bids"]],
        }
    
    def update_markets(self, tickers):
        for t in tickers:
            market_id = t["market_id"]
            last_price, quote_currency = t["last_price"]
            base_currency = market_id.replace(f"-{quote_currency}", "")
            if quote_currency not in self.markets:
                self.markets[quote_currency] = {}
            self.markets[quote_currency][base_currency] = float(last_price)
        return 

    def check_time_passed(self):
        return self.last_update and ((self.last_update - datetime.now()) > timedelta(hours=2))

if __name__ == "__main__":
    client = RealBudaClient()
    client.refresh_tickers()
    print(client.markets['CLP'])
    print(client.markets['CLP'].keys())

