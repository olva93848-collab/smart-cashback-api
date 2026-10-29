from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

class BotRequest(BaseModel):
    product: str
    base_price: float
    card_price: float

"/calculate"
async def calculate_smart_prices(data: BotRequest):
    alfa_percent = 10
    tbank_percent = 5
    sber_percent = 2

    alfa_final = round(data.card_price * (1 - alfa_percent / 100), 2)
    tbank_final = round(data.card_price * (1 - tbank_percent / 100), 2)
    sber_final = round(data.card_price * (1 - sber_percent / 100), 2)

    prices = {"Альфа-Банк": alfa_final, "Т-Банк": tbank_final, "СберСпасибо": sber_final}
    best_bank = min(prices, key=prices.get)
    best_price = prices[best_bank]

    return {
        "regular": data.base_price,
        "card": data.card_price,
        "alfa": alfa_final,
        "tbank": tbank_final,
        "sber": sber_final,
        "best_bank": best_bank,
        "best_price": best_price
    }
