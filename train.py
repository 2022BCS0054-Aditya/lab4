import pandas as pd
import json
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load the dataset
data_path = 'data/winequality-red.csv'
df = pd.read_csv(data_path, sep=';')

# 2. Apply pre-processing and feature selection

## Separate features and target variable
X = df.drop('quality', axis=1)
y = df['quality']

correlations = df.corr()['quality'].drop('quality')

# feature selection
# top_features = correlations.abs().sort_values(ascending=False).head(4).index.tolist()
# print(f"Selected Features based on correlation: {top_features}")
# X_processed = X[top_features]

# scaler = StandardScaler()
# X_processed = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
mm_scaler = MinMaxScaler()
X_processed = pd.DataFrame(mm_scaler.fit_transform(X), columns=X.columns)

# 3. Train the model
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# model = Ridge(alpha=12)
model = RandomForestRegressor(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate the model
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)

# 5. Save outputs
os.makedirs('outputs', exist_ok=True)

## Save the trained model
with open('outputs/model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save evaluation metrics to a JSON file
metrics = {
    "mse": mse,
    "r2_score": r2
}
with open('outputs/results.json', 'w') as f:
    json.dump(metrics, f)

# 6. Print metrics to standard output
print(f"r2_score={r2}")
print(f"mse={mse}")