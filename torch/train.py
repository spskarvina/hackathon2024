import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

# Vytvoření DataFrame
data = {
    'CO2': [0.04, 0.01, 0.02],
    'Temperature': [33, 20, 26],
    'Humidity': [40, 20, 30],
    'Population': [100, 100, 70],
    'Okno': [100, 0, 0],
    'Ventil': [100, 100, 0]
}

df = pd.DataFrame(data)

# Vstupy a výstupy
X = df[['CO2', 'Temperature', 'Humidity', 'Population']].values.astype(np.float32)  # Vstupy
y = df[['Okno', 'Ventil']].values.astype(np.float32)  # Výstupy

# Rozdělení na tréninková a testovací data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Převod na tensory
X_train_tensor = torch.tensor(X_train)
y_train_tensor = torch.tensor(y_train)
X_test_tensor = torch.tensor(X_test)
y_test_tensor = torch.tensor(y_test)

# Definice modelu
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

# Vytvoření modelu
model = SimpleNN()

# Zvolení ztrátové funkce a optimalizátoru
criterion = nn.MSELoss()  # Mean Squared Error
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Trénování modelu
epochs = 100
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()  # Nulování gradientů
    outputs = model(X_train_tensor)  # Predikce na trénovacích datech
    
    print("Prediction: " + str(outputs))
    print("Ground truth: " + str(y_train_tensor))
    loss = criterion(outputs, y_train_tensor)  # Výpočet ztráty
    loss.backward()  # Zpětná propagace
    optimizer.step()  # Krok optimalizace

    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# Testování modelu
model.eval()  # Přepnutí na evaluační režim
with torch.no_grad():
    predictions = model(X_test_tensor)
    print("Predicted values:")
    print(predictions)

    # Výpočet ztráty na testovacích datech
    test_loss = criterion(predictions, y_test_tensor)
    print(f"Test Loss: {test_loss.item():.4f}")


# Uložení modelu
torch.save(model.state_dict(), "simple_nn_model.pth")
print("Model saved!")
