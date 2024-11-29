import torch
import torch.nn as nn
import numpy as np

# Definice modelu (stejná jako v trénovací fázi)
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(4, 16)  # 4 vstupy, 16 neuronů ve skryté vrstvě
        self.fc2 = nn.Linear(16, 8)  # 8 neuronů ve skryté vrstvě
        self.fc3 = nn.Linear(8, 2)   # 2 výstupy (Okno, Ventil)

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU aktivace
        x = torch.relu(self.fc2(x))  # ReLU aktivace
        x = self.fc3(x)              # Výstup
        return x

# Načtení modelu
model = SimpleNN()
model.load_state_dict(torch.load("simple_nn_model.pth"))
model.eval()  # Přepnutí modelu na evaluační režim

# Funkce pro predikci na základě uživatelského vstupu
def predict():
    # Uživatel zadá hodnoty pro CO2, Temperature, Humidity a Population
    CO2 = float(input("Enter CO2 level (e.g., 0.04): "))
    Temperature = float(input("Enter Temperature (e.g., 33): "))
    Humidity = float(input("Enter Humidity (e.g., 40): "))
    Population = float(input("Enter Population (e.g., 100): "))

    # Vytvoření vstupního tensoru
    input_tensor = torch.tensor([[CO2, Temperature, Humidity, Population]], dtype=torch.float32)

    # Predikce
    with torch.no_grad():
        output = model(input_tensor)
    
    # Výstup pro Okno a Ventil
    print(f"Predicted Okno: {output[0][0].item():.2f}")
    print(f"Predicted Ventil: {output[0][1].item():.2f}")

# Volání funkce pro predikci
predict()
