# allign 1.0

# import pandas as pd
# import csv

# file = 'data/rba-split-0.csv'

# data = pd.read_csv(file)
# lines = data.shape[0]
# print(lines)

# final = []
# with open('data/rba-split-0.csv', 'r', encoding='utf-8') as file:
#     for i in range(lines):
#         row = file.readline()
#         # print(i, row)
#         if not i%100000: print(i)
#         final.append(row)
#         count, first, para = 0, False, 0
#         for (j, l) in enumerate(row):
            
#             if l == '(':
#                 para += 1
#             if l == ')':
#                 para -= 1
            
#             if count == 9:
#                 if not first and l != '"':
#                     final[i] = final[i][:j] + '"' + final[i][j:]
#                 first = True
            
#             if l == ',' and para == 0:
#                 if first and row[j-1] != '"':
#                     final[i] = final[i][:j+1] + '"' + final[i][j+1:]
#                 first = False
                    
#                 count += 1

# with open('data/corrected/rba-split-corrected-0.csv', 'w', newline='', encoding='utf-8') as file:
#     for row in final:
#         file.write(row)

# print('Done')

# allign 2.0

# import csv
# import pandas as pd

# f = 'data/rba-split-0.csv'

# # data = pd.read_csv(f)
# # lines = data.shape[0]
# # print(lines)

# final = []
# with open(f, 'r', encoding='utf-8') as file:
#     for line in range(200):
#         row = file.readline()
#         if not line%100000: print(line)
#         final.append([])
        
#         collumn, element, para, Khtml, chrome, snapchat, rocket, xt, ecosia = 0, '', 0, False, False, False, False, False, False
#         for (i, c) in enumerate(row):
#             if not chrome and row[i:i+7] == '(Chrome': chrome = True
#             if not snapchat and row[i:i+11] == '.36Snapchat': snapchat = True
#             if not rocket and row[i-7:i] == ' Rocket': rocket = True
#             if not ecosia and row[] == '(Ecosia':
#             if row[i-3:i] == '(XT': xt = True
#             if row[i-8:i] == 'gzip(gfe': element += ')'
#             if snapchat and row[i-5:i] == ' gzip':
#                 element += ')'
#                 para -= 1
#             if c == ',':
#                 if para == 0:
#                     final[line].append(element)
#                     collumn += 1
#                     element = ''
#                     continue
#                 elif chrome:
#                     element += ')'
#                     para -= 1
#                     final[line].append(element)
#                     collumn += 1
#                     element = ''
#                     continue
#             elif c == '(':
#                 para += 1
#             elif c == ')':
#                 para -= 1
#             elif not Khtml and row[i-18:i] == '(KHTML, like Gecko':
#                 Khtml = True
#                 element += ')'
#                 para -= 1
#             elif rocket and c == ' ':
#                 rocket = False
#                 element += ')'
#                 para -= 1
#             elif xt and c == ' ':
#                 xt = False
#                 element += ')'
#                 para -= 1
#             element += c

# for i in range(200):
#     try:
#         x = final[i][9]
#         # print(i-1, final[i][9])
#     except: print(i-1, final[i])

# allign 3.0

import csv
import pandas as pd

for file_no in range(0, 24):

    f = f'data/rba-split-{file_no}.csv'
    final = []
    data = pd.read_csv(f)
    lines = data.shape[0]
    # print(lines)

    with open(f, 'r', encoding='utf-8') as file:
        final.append(file.readline().split(','))
        for line in range(1, lines):
            row = file.readline()
            # if not line%100000: print(line)
            splitted = row.split(',')
            first = splitted[:9]
            last = splitted[-6:]
            last[-1] = last[-1][:-1]
            middle = splitted[9:-6]
            UAS = ''
            for string in middle:
                UAS += string.replace('"', '').replace(';', '|') + ' &'
            UAS = UAS[:-2]
            
            final.append(first + [UAS] + last)


    with open(f'data/corrected/rba-split-corrected-{file_no}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(final)

    print(f'Done file no: {file_no}')