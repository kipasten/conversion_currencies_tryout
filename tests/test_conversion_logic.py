import pytest
from unittest.mock import MagicMock
from app.conversion import (
    simulate_buy_with_quote,
    simulate_sell_base,
    find_intermediaries,
    find_best_conversion,
)

# --- simulate_buy_with_quote ---

def test_simulate_buy_with_quote_full_fill():
    order_book = {"asks": [[100, 2], [110, 3]]}  # precios, cantidades
    amount_quote = 200  # CLP
    result = simulate_buy_with_quote(order_book, amount_quote)
    # Se compra 2 unidades a 100
    assert pytest.approx(result, 0.001) == 2.0

def test_simulate_buy_with_quote_partial_fill():
    order_book = {"asks": [[100, 1], [200, 1]]}
    amount_quote = 150  # alcanza para 1 en 100 y 0.25 en 200
    result = simulate_buy_with_quote(order_book, amount_quote)
    assert pytest.approx(result, 0.001) == 1.25

def test_simulate_buy_with_quote_empty_book():
    result = simulate_buy_with_quote({"asks": []}, 100)
    assert result == 0.0


# --- simulate_sell_base ---

def test_simulate_sell_base_full_fill():
    order_book = {"bids": [[100, 2], [90, 3]]}
    amount_base = 1.5
    result = simulate_sell_base(order_book, amount_base)
    assert pytest.approx(result, 0.001) == 150.0

def test_simulate_sell_base_partial_fill():
    order_book = {"bids": [[100, 1], [90, 1]]}
    amount_base = 1.5
    result = simulate_sell_base(order_book, amount_base)
    assert pytest.approx(result, 0.001) == 145.0

def test_simulate_sell_base_empty_book():
    assert simulate_sell_base({"bids": []}, 10) == 0.0


# --- find_intermediaries ---

def test_find_intermediaries_found():
    mock_client = MagicMock()
    mock_client.markets = {
        "CLP": {"BTC": 100, "ETH": 200},
        "PEN": {"BTC": 90}
    }
    result = find_intermediaries("CLP", "PEN", mock_client)
    assert result == ["BTC"]

def test_find_intermediaries_none():
    mock_client = MagicMock()
    mock_client.markets = {
        "CLP": {"ETH": 200},
        "PEN": {"BTC": 90}
    }
    result = find_intermediaries("CLP", "PEN", mock_client)
    assert result == []


# --- find_best_conversion ---

def test_find_best_conversion_returns_best(monkeypatch):
    mock_client = MagicMock()
    mock_client.markets = {
        "CLP": {"BTC": 100},
        "PEN": {"BTC": 90}
    }

    # Mock refresh_tickers (no hace nada)
    mock_client.refresh_tickers = MagicMock()

    # Mock get_order_book: mercado BTC-CLP y BTC-PEN
    mock_client.get_order_book.side_effect = lambda m: {
        "BTC-CLP": {"asks": [[100, 1]], "bids": []},
        "BTC-PEN": {"bids": [[90, 1]], "asks": []}
    }.get(m, None)

    dest_amt, inter, markets = find_best_conversion("CLP", "PEN", 100, mock_client)

    assert inter == "BTC"
    assert markets == ["BTC-CLP", "BTC-PEN"]
    assert pytest.approx(dest_amt, 0.001) == 90.0

def test_find_best_conversion_no_books(monkeypatch):
    mock_client = MagicMock()
    mock_client.markets = {"CLP": {"BTC": 100}, "PEN": {"BTC": 90}}
    mock_client.refresh_tickers = MagicMock()
    mock_client.get_order_book.return_value = None

    result = find_best_conversion("CLP", "PEN", 100, mock_client)
    assert result == (0, None, [])