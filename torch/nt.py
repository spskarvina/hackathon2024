import pandas as pd

# Použití správného formátu pro cestu k souboru
data = pd.read_excel(r"C:\\Users\\J45j1\\Desktop\\Neuron.xlsx")  # Raw string pro správnou cestu k souboru

# Zobrazení několika prvních řádků pro kontrolu
print(data.head())
