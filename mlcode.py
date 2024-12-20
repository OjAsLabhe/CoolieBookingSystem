import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor

data = pd.read_csv(r"C:\Users\labhe\OneDrive\Desktop\dataset (2).csv")
df = pd.DataFrame(data)

data.iloc[:, 1:] += np.random.choice([-1, 1], size=df.iloc[:, 1:].shape)

X_train = df.drop(columns=['coolie_id'])
y_train = df['coolie_id']

weights = np.random.dirichlet(np.ones(len(X_train.columns)), size=1)[0] * 100

efficiency_scores = {}

for coolie_id in df['coolie_id']:
    X_train_excluded = X_train[X_train.index != coolie_id - 1]
    y_train_excluded = y_train[X_train.index != coolie_id - 1]
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train_excluded, y_train_excluded)
    efficiency = model.predict(X_train.iloc[coolie_id - 1:coolie_id])
    weighted_efficiency = sum(weight * eff for weight, eff in zip(weights, efficiency))
    efficiency_scores[coolie_id] = max(0, min(100, weighted_efficiency))

efficiency_above_90 = {coolie_id: efficiency for coolie_id, efficiency in efficiency_scores.items() if efficiency > 90}

random_5_coolie_ids = np.random.choice(list(efficiency_above_90.keys()), size=min(5, len(efficiency_above_90)), replace=False)
random_5_results = {coolie_id: efficiency_above_90[coolie_id] for coolie_id in random_5_coolie_ids}

print("\nRandom 5 results whose efficiency is above 90% (in the form of a dictionary):")
print(random_5_results)
