import pandas as pd
import random

# Function to determine crowd level
def get_crowd_level(hour, day_type):
    if day_type == "Weekday":
        if 8 <= hour <= 10 or 18 <= hour <= 21:
            return "High"
        elif 11 <= hour <= 17:
            return "Medium"
        else:
            return "Low"
    else:  # Weekend
        if 10 <= hour <= 20:
            return "Medium"
        else:
            return "Low"

# Generate dataset
data = []

for _ in range(300):
    hour = random.randint(5, 23)
    day_type = random.choice(["Weekday", "Weekend"])
    crowd = get_crowd_level(hour, day_type)

    data.append([hour, day_type, crowd])

# Create DataFrame
df = pd.DataFrame(data, columns=["hour", "day_type", "crowd_level"])

# Save to CSV
df.to_csv("data/metro_data.csv", index=False)

print("Dataset generated successfully!")