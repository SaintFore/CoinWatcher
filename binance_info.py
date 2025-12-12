import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

client = Client(api_key=api_key, api_secret=api_secret)

print(client.get_exchange_info())
