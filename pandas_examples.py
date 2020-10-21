import pandas as pd
import json

# PANDAS
data = {'apples': [3, 2, 0, 1], 'oranges': [0, 3, 7, 2]}
purchases = pd.DataFrame(data)
purchases = pd.DataFrame(data, index=['June', 'Robert', 'Lily', 'David'])

# JSON
states = "./results/states.json"
with open(states, 'r') as f:
    python_dict = json.load(f)
