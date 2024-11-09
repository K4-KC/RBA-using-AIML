import pandas as pd

data = pd.read_csv(f'data/corrected/rba-split-corrected-0.csv', low_memory=False)
attack_data = data.loc[data['Is Account Takeover'] == True]
print(len(attack_data))

for file in range(1, 24):
    data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
    attack_data = pd.concat((attack_data, data.loc[data['Is Account Takeover'] == True]))
    print(file, len(attack_data))

print(len(attack_data))
attack_data.to_csv('attack.csv', index=False)