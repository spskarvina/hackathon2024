from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from datetime import datetime
import aiomysql

app = FastAPI()

origins = [
    "http://localhost:5000"
]

current_temperature = None
current_co2 = None
current_illuminance = None

# Připojení k databázi
DB_CONFIG = {
    "host": "192.168.50.100",
    "port": 3306,
    "user": "sc-admin",
    "password": "SCmain",
    "db": "sc_db"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funkce pro uložení do databáze
async def save_to_db(query: str, params: tuple):
    try:
        conn = await aiomysql.connect(**DB_CONFIG)
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()
        conn.close()
    except Exception as e:
        print(f"Chyba při ukládání do databáze: {e}")


@app.get("/test")
async def test():
    return "funguju"


@app.post("/api/newIlluminance")
async def new_illuminance(request: Request):
    raw_body = await request.body()

    decoded_data = raw_body.decode("utf-8")
    global current_illuminance
    try:
        concentration = int(decoded_data)
        print("Přijatá intenzita světla: ", concentration)
        current_illuminance = (concentration, datetime.now())
        return {"received_concentration": concentration}
    except ValueError:
        print("Chyba: Neplatný formát dat")
        return {"error": "Invalid data format"}, 400

@app.post("/api/newCO2Concentration")
async def new_concentration(request: Request):
    raw_body = await request.body()

    decoded_data = raw_body.decode("utf-8")
    global current_co2
    try:
        concentration = float(decoded_data)
        print("Přijatá CO2 Koncentrace: ", concentration)
        current_co2 = (concentration, datetime.now())

        # Uložení do databáze (air)
        query = "INSERT INTO air (value, time, room) VALUES (%s, %s, %s)"
        await save_to_db(query, (concentration, current_co2[1], 1))  # room = 1 (přednastavený pokoj)

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

        # Uložení do databáze (temperatures)
        query = "INSERT INTO temperature (value, time, room) VALUES (%s, %s, %s)"
        await save_to_db(query, (temperature, current_temperature[1], 1))  # room = 1 (přednastavený pokoj)

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

@app.get("/api/getIlluminance")
async def get_illuminance():
    global current_illuminance
    return {
        "concentration": current_illuminance[0],
        "time": current_illuminance[1]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
