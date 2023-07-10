import yfinance as yf

def check_engulfing_pattern(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        historical_data = stock.history(period="2y")
    except Exception:
        return "Invalid symbol or symbol not found."

    # Calculate the candle size (difference between high and low)
    historical_data['CandleSize'] = historical_data['High'] - historical_data['Low']

    # Check for bullish engulfing pattern
    bullish_engulfing = (
        (historical_data['Open'].shift(1) > historical_data['Close'].shift(1))
        & (historical_data['Open'] < historical_data['Close'])
        & (historical_data['Open'] > historical_data['Low'].shift(1))
        & (historical_data['Close'] < historical_data['Open'].shift(1))
    )

    # Check for bearish engulfing pattern
    bearish_engulfing = (
        (historical_data['Open'].shift(1) < historical_data['Close'].shift(1))
        & (historical_data['Open'] > historical_data['Close'])
        & (historical_data['Open'] < historical_data['Open'].shift(1))
        & (historical_data['Close'] > historical_data['Low'].shift(1))
    )

    bullish_count = bullish_engulfing.sum()
    bearish_count = bearish_engulfing.sum()

    # Add other metrics for consideration
    current_price = historical_data.iloc[-1]['Close']
    moving_average_50 = historical_data['Close'].rolling(window=50).mean().iloc[-1]
    moving_average_200 = historical_data['Close'].rolling(window=200).mean().iloc[-1]
    rsi = calculate_rsi(historical_data)

    # Make investment decision based on metrics
    if bullish_count > bearish_count and current_price > moving_average_50 and current_price > moving_average_200 and rsi < 70:
        decision = f"<br>{symbol}: More probable pattern - Bullish Engulfing ({bullish_count} occurrences).<br>Investment Decision: It's a potential buying opportunity for short-term investment."
    elif bearish_count > bullish_count or current_price < moving_average_50 or current_price < moving_average_200 or rsi > 70:
        decision = f"<br>{symbol}: More probable pattern - Bearish Engulfing ({bearish_count} occurrences).<br>Investment Decision: It's not a favorable time to buy for short-term investment."
    else:
        decision = f"<br>{symbol}: No engulfing pattern found.<br>Investment Decision: No clear pattern or metrics for buying."

    # Make selling decision based on metrics
    if current_price > moving_average_50 and current_price > moving_average_200 and rsi > 70:
        decision += "<br>Selling Decision: It might be a good time to consider selling."
    else:
        decision += "<br>Selling Decision: No specific selling indication at the moment."

    return decision

def calculate_rsi(data):
    close_prices = data['Close']
    price_diff = close_prices.diff().dropna()

    gain = price_diff.mask(price_diff < 0, 0)
    loss = -price_diff.mask(price_diff > 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]