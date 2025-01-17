import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np  # Do obliczeń pierwiastka
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("mieszkania_otodom_cleaned.csv", delimiter=";")

# Przygotowanie zmiennych objaśniających (X) i zmiennej docelowej (y)
X = df[['Price per m2', 'Area', 'Rooms', 'Floor', 'City_or_District', 'Province']]

# Kodowanie zmiennych kategorycznych (miasto, województwo)
X = pd.get_dummies(X, drop_first=True)

y = df['Price']  # Zmienna docelowa (cena)

# **Skalowanie zmiennej docelowej (Price)**
scaler = MinMaxScaler()
y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))  # Skalowanie y

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train_scaled, y_test_scaled = train_test_split(X, y_scaled, test_size=0.2, random_state=42)

# Tworzymy model regresyjny Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Trenujemy model na skalowanych danych
model.fit(X_train, y_train_scaled.ravel())  # Ravel przekształca y_train_scaled na 1D

# Predykcja na zbiorze testowym
y_pred_scaled = model.predict(X_test)

# **Odwrócenie skalowania dla predykcji i rzeczywistych wartości**
y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))  # Predykcje w oryginalnej skali
y_test = scaler.inverse_transform(y_test_scaled)  # Rzeczywiste wartości w oryginalnej skali

# Obliczamy metryki błędu na odskalowanych danych
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Wyświetlamy wyniki
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared: {r2:.2f}")

# Wizualizacja porównania rzeczywistej ceny i prognozowanej ceny
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, label='Prognozowane vs. Rzeczywiste')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Idealna linia')
plt.xlabel('Rzeczywista cena (zł)')
plt.ylabel('Prognozowana cena (zł)')
plt.title('Porównanie rzeczywistej ceny z prognozowaną ceną')
plt.legend()
plt.grid(True)
plt.savefig("porownanie_cen.png")
plt.show()
