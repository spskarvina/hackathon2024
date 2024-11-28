from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povolit všechny domény (pro testování)
    allow_credentials=True,
    allow_methods=["*"],  # Povolit všechny metody (GET, POST, atd.)
    allow_headers=["*"],  # Povolit všechny hlavičky
)

class TemperaturePayload(BaseModel):
    payload: float  # očekáváme číselnou hodnotu (teplotu)

@app.get("/test")
async def test():
    return "funguju"

@app.post("/api/newTemperature")
async def new_temperature(request: Request):
    # Načtení syrového těla požadavku
    raw_body = await request.body()
    
    # Dekódování binárních dat na text (UTF-8)
    decoded_data = raw_body.decode("utf-8")
    
    try:
        # Převod na číslo (pokud se očekává hodnota jako 26.5)
        temperature = float(decoded_data)
        print("Přijatá teplota:", temperature)
        return {"received_temperature": temperature}
    except ValueError:
        # Chyba, pokud nelze převést na číslo
        print("Chyba: Neplatný formát dat")
        return {"error": "Invalid data format"}, 400

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)