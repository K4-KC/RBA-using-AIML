import pandas as pd

data = pd.read_csv('rba-dataset.csv')

print(data.head())

split = [None for i in range(20)]
j1, j2 = 0, int(len(data)/20)
print(len(data))
print(j1, j2)
# for i in range(20):
#     split[i] = data.iloc[j1:j1 + j2]
#     j1 += j2

# print('done splitting')

# for i in range(20):
#     split[i].to_csv('rba-split-{i}.csv', index=False)
#     print(split[i].head())