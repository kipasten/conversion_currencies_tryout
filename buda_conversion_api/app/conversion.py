def simulate_buy_with_quote(order_book, amount_quote):
    total_base = 0.0
    for price, qty in order_book.get("asks", []):
        trade_qty_quote = min(amount_quote, price * qty)
        total_base += trade_qty_quote / price
        amount_quote -= trade_qty_quote
        if amount_quote <= 0:
            break
    return total_base

def simulate_sell_base(order_book, amount_base):
    total_quote = 0.0
    for price, qty in order_book.get("bids", []):
        trade_qty_base = min(amount_base, qty)
        total_quote += trade_qty_base * price
        amount_base -= trade_qty_base
        if amount_base <= 0:
            break
    return total_quote

def find_intermediaries(source,dest,client):
    possible_buys = client.markets[source].keys()
    possible_sells = client.markets[dest].keys()
    intermediaries = list(set(possible_buys).intersection(set(possible_sells)))
    return intermediaries

def find_best_conversion(source, dest, amount,  client):
    best_result = (0, None, [])
    client.refresh_tickers()
    intermediaries = find_intermediaries(source,dest, client)

    for inter in intermediaries:
        market1 = f"{inter}-{source}"
        market2 = f"{inter}-{dest}"
        book1 = client.get_order_book(market1)
        book2 = client.get_order_book(market2)
        if not book1 or not book2:
            continue
        base_amt = simulate_buy_with_quote(book1, amount)
        dest_amt = simulate_sell_base(book2, base_amt)
        if dest_amt > best_result[0]:
            best_result = (dest_amt, inter, [market1, market2])
    return best_result
