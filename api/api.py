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

async def get_db_connection():
    return await aiomysql.connect(
        host="192.168.50.100",
        port=3306,
        user="sc-admin",
        password="SCmain",
        db="sc_db"
)

async def save_to_db(query: str, params: tuple):
    try:
        conn = await aiomysql.connect(**DB_CONFIG)
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            await conn.commit()
        conn.close()
    except Exception as e:
        print(f"Chyba při ukládání do databáze: {e}")

async def db_query(query: str):
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            result = await cursor.fetchone()  # Vrátí jeden řádek výsledku
        return result
    except Exception as e:
        print("Chyba při práci s databází: ", e)
    finally:
        conn.close()


@app.get("/test")
async def test():
    return "funguju"


@app.post("/api/newIlluminance")
async def new_illuminance(request: Request):
    raw_body = await request.body()

    decoded_data = raw_body.decode("utf-8")
    global current_illuminance
    try:
        concentration = float(decoded_data)
        print("Přijatá intenzita světla: ", concentration)
        current_illuminance = (concentration, datetime.now())

        # Uložení do databáze (light)
        query = "INSERT INTO light (value, time, room) VALUES (%s, %s, %s)"
        await save_to_db(query, (concentration, current_illuminance[1], 1))  # room = 1 (přednastavený pokoj)

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
    try:
        return {
            "temperature": current_temperature[0],
            "time": current_temperature[1]
        }
    except Exception:
        return latest_temperature()


@app.get("/api/getCO2Concentration")
async def get_concentration():
    global current_co2
    try:
        return {
            "concentration": current_co2[0],
            "time": current_co2[1]
        }
    except Exception:
        return latest_co2concentration()

@app.get("/api/getIlluminance")
async def get_illuminance():
    global current_illuminance
    try:
        return {
            "concentration": current_illuminance[0],
            "time": current_illuminance[1]
        }
    except Exception:
        return latest_illuminance()

@app.get("/api/latestTemperature")
async def latest_temperature():
    query = "SELECT value, time FROM temperature ORDER BY time DESC LIMIT 1;"
    result = await db_query(query)
    if result:
        return {"temperature": result[0], "time": result[1]}  # Vrací hodnotu teploty
    else:
        return {"error": "No data found"}
    
@app.get("/api/latestCO2Concentration")
async def latest_co2concentration():
    query = "SELECT value, time FROM air ORDER BY time DESC LIMIT 1;"
    result = await db_query(query)
    if result:
        return {"concentration": result[0], "time": result[1]}  # Vrací hodnotu teploty
    else:
        return {"error": "No data found"}
    
@app.get("/api/latestIlluminance")
async def latest_illuminance():
    query = "SELECT value, time FROM light ORDER BY time DESC LIMIT 1;"
    result = await db_query(query)
    if result:
        return {"concentration": result[0], "time": result[1]}  # Vrací hodnotu teploty
    else:
        return {"error": "No data found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
