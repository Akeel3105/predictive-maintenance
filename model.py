import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ===== Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this file is
DATA_PATH = os.path.join(BASE_DIR, "data", "sensor_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "predictive_maintenance_model.pkl")  # save to root so FastAPI can find it easily

# ===== Load dataset =====
df = pd.read_csv(DATA_PATH)

# Ensure the dataset has the expected features
expected_features = ["temperature", "vibration", "pressure", "rpm", "failure"]
missing_cols = [col for col in expected_features if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# Features & target
X = df[["temperature", "vibration", "pressure", "rpm"]]
y = df["failure"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===== Train model =====
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===== Evaluate =====
y_pred = model.predict(X_test)
print("✅ Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ===== Save model =====
joblib.dump(model, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
