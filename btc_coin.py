import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=60)
def get_coin_price(coin_type="bitcoin", currency_type="usd"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_type}&vs_currencies={currency_type}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[coin_type][currency_type]
        else:
            return None
    except Exception as e:
        print(f"Error {e}")
        return None


@st.cache_data(ttl=60)
def get_coin_history(days=7, coin_type="bitcoin", currency_type="usd"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_type}/market_chart?vs_currency={currency_type}&days={days}&interval=daily"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(type(data))
            prices_data = data["prices"]
            # only_prices = [item[1] for item in prices_data]
            # df = pd.DataFrame(data=only_prices, columns=["prices"])
            df = pd.DataFrame(
                data=prices_data, columns=pd.Index(["timestamp", "prices"])
            )
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["SMA-3"] = df["prices"].rolling(window=3).mean()
            df.set_index("date", inplace=True)
            return df[["prices", "SMA-3"]]
        else:
            return None
    except Exception as e:
        print(f"Error {e}")
        return None


if __name__ == "__main__":
    price = get_coin_price()
    print(price)
    df = get_coin_history()
    print(df)
