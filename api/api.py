from fastapi import FastAPI
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
async def new_temperature(payload: TemperaturePayload):
    # Zpracování přijatých dat
    return {"received_temperature": payload.payload}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)