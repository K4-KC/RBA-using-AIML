import pandas as pd
import csv

file = 'data/rba-split-0.csv'

data = pd.read_csv(file)
lines = data.shape[0]
print(lines)

final = []
with open('data/rba-split-0.csv', 'r', encoding='utf-8') as file:
    for i in range(lines):
        row = file.readline()
        # print(i, row)
        if not i%100000: print(i)
        final.append(row)
        count, first, para = 0, False, 0
        for (j, l) in enumerate(row):
            
            if l == '(':
                para += 1
            if l == ')':
                para -= 1
            
            if count == 9:
                if not first and l != '"':
                    final[i] = final[i][:j] + '"' + final[i][j:]
                first = True
            
            if l == ',' and para == 0:
                if first and row[j-1] != '"':
                    final[i] = final[i][:j+1] + '"' + final[i][j+1:]
                first = False
                    
                count += 1

with open('data/corrected/rba-split-corrected-0.csv', 'w', newline='', encoding='utf-8') as file:
    for row in final:
        file.write(row)

print('Done')
