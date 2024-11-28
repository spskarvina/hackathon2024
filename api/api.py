from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost:5000"
]

current_temperature = None
current_co2 = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povolit všechny domény (pro testování)
    allow_credentials=True,
    allow_methods=["*"],  # Povolit všechny metody (GET, POST, atd.)
    allow_headers=["*"],  # Povolit všechny hlavičky
)


@app.get("/test")
async def test():
    return "funguju"

@app.post("/api/newCO2Concentration")
async def new_concentration(request: Request):
    raw_body = await request.body()

    decoded_data = raw_body.decode("utf-8")
    global current_co2
    try:
        concentration = int(decoded_data)
        print("Přijatá CO2 Koncentrace: ", concentration)
        current_co2 = (concentration, datetime.now())
        return {"received_concentration": concentration}
    except ValueError:
        print("Chyba: Neplatný formát dat")
        return {"error": "Invalid data format"}, 400

@app.post("/api/newTemperature")
async def new_temperature(request: Request):
    raw_body = await request.body()
    
    decoded_data = raw_body.decode("utf-8")
    global current_temperature
    try:
        temperature = float(decoded_data)
        print("Přijatá teplota:", temperature)
        current_temperature = (temperature, datetime.now())
        return {"received_temperature": temperature}
    except ValueError:
        print("Chyba: Neplatný formát dat")
        return {"error": "Invalid data format"}, 400

@app.get("/api/getTemperature")
async def get_temperature():
    global current_temperature
    return {
        "temperature": current_temperature[0],
        "time": current_temperature[1]
    }

@app.get("/api/getCO2Concentration")
async def get_concentration():
    global current_co2
    return {
        "concentration": current_co2[0],
        "time": current_co2[1]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)