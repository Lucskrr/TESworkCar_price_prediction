import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Carregar os dados de treinamento
df = pd.read_csv('car_analysis/data/car_price_prediction.csv')

# Preparar os dados
df['Mileage'] = df['Mileage'].str.replace(' km', '').str.replace(',', '').astype(float)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')  # Garantir que 'Price' seja numérico
df = df.dropna()  # Remover valores ausentes

X = df[['Prod. year', 'Mileage', 'Fuel type']]
y = df['Price']
X = pd.get_dummies(X, columns=['Fuel type'], drop_first=True)

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar o modelo
model = RandomForestRegressor(random_state=42)

# Treinar o modelo
model.fit(X_train, y_train)

# Avaliar o modelo no conjunto de teste
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions, squared=False)
r2 = r2_score(y_test, predictions)

# Exibir métricas no console
print("Avaliação do modelo:")
print(f"MAE (Erro Médio Absoluto): {mae}")
print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse}")
print(f"R² (Coeficiente de Determinação): {r2}")

# Salvar o modelo treinado e as colunas utilizadas
joblib.dump(model, 'car_analysis/models/car_price_model.pkl')
joblib.dump(X.columns.tolist(), 'car_analysis/models/model_columns.pkl')

print("Modelo treinado, avaliado e salvo com sucesso!")
