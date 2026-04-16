import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
df = pd.read_csv("data/metro_data.csv")

# Encode categorical data
le_day = LabelEncoder()
df['day_type'] = le_day.fit_transform(df['day_type'])

le_crowd = LabelEncoder()
df['crowd_level'] = le_crowd.fit_transform(df['crowd_level'])

# Features and target
X = df[['hour', 'day_type']]
y = df['crowd_level']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "models/model.pkl")
joblib.dump(le_day, "models/le_day.pkl")
joblib.dump(le_crowd, "models/le_crowd.pkl")

print("Model trained and saved successfully!")