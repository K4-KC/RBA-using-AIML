# import pandas as pd
# import numpy as np


# users = []

# for file in range(24):
#     data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
#     # attacks = data[data['Is Account Takeover'] == True]['User ID']
#     attacks = data.loc[data['Is Account Takeover'] == True]
#     users.append(attacks)
#     print('parsing file:', file, 'with attacks:', len(users))
#     # data_arr = np.array(data['User ID'])
#     # for user in attacks:
#     #     # if i % 10000 == 0:
#     #     #     print(i, len(users))
#     #     if user not in users:
#     #         users.append(user)
#     #     else: print('    already in', user)
#     #     # if data['Is Account Takeover'][i]:
#     #     #     add_ifnot_binary_search(users, user)


# # print(users)
# print(len(users))

# import pandas as pd
# import sqlite3 as sql
# import numpy as np
# import math

# conn = sql.connect('data/sql/rba.db')
# c = conn.cursor()

# drop_table = """ DROP TABLE IF EXISTS rba; """
# # c.execute(drop_table)

# create_table = """ CREATE TABLE IF NOT EXISTS rba (
#     User_ID BIGINT,
#     Round_Trip BLOB,
#     Is_Account_Takeover BOOL
# ); """
# # c.execute(create_table)

# add = []

# # for file in range(1):
# #     data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
# #     # sql_data = data.loc[data['Is Account Takeover'] == True][['User ID', 'Round-Trip Time [ms]', 'Is Account Takeover']]
# #     sql_data = data
    
# #     for index, row in sql_data.iterrows():
# #         add.append((row['User ID'], np.array((True, row['Round-Trip Time [ms]'])).tobytes() if np.isnan(row['Round-Trip Time [ms]']) else np.array((False, 0)).tobytes(), row['Is Account Takeover']))

# #     print('begin adding')
# #     c.executemany("INSERT INTO rba (User_ID, Round_Trip, Is_Account_Takeover) VALUES (?, ?, ?)", add)

# c.execute("SELECT * FROM rba")
# for elem in c.fetchone(): print(elem)

# conn.commit()

# conn.close()

# import pandas as pd
# import numpy as np
# import pickle

# def save_list(list, filename):
#     with open(filename, 'wb') as f:
#         pickle.dump(list, f)

# def read_list(filename):
#     with open(filename, 'rb') as f:
#         return pickle.load(f)

# Ip_Address = []
# country = []
# region = []
# city = []
# Asn = []
# Device_type = []

# for file in range(24):
#     data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
#     # attack_data = data.loc[data['Is Account Takeover'] == True][['User ID', 'Round-Trip Time [ms]', 'Is Account Takeover']]
#     for index, row in data.iterrows():
#         if row['Is Account Takeover'] == True:
#             # print(index, row['Is Account Takeover'])
#             if row['IP Address'] not in Ip_Address:
#                 Ip_Address.append(row['IP Address'])
#             if row['ASN'] not in Asn:
#                 Asn.append(row['ASN'])
#         # if row['Country'] not in country:
#         #     country.append(row['Country'])
#         if row['Region'] not in region:
#             region.append(row['Region'])
#         if row['City'] not in city:
#             city.append(row['City'])
#         if row['Device Type'] not in Device_type:
#             Device_type.append(row['Device Type'])
#     print(file, len(Ip_Address), len(country), len(region), len(city), len(Asn), len(Device_type))

# save_list(Ip_Address, 'data/hot_encoding_lists/ip_address_list.pkl')
# # save_list(country, 'data/hot_encoding_lists/country_list.pkl')
# save_list(region, 'data/hot_encoding_lists/region_list.pkl')
# save_list(city, 'data/hot_encoding_lists/city_list.pkl')
# save_list(Asn, 'data/hot_encoding_lists/asn_list.pkl')
# save_list(Device_type, 'data/hot_encoding_lists/device_type_list.pkl')

# Ip_Address = read_list('data/hot_encoding_lists/ip_address_list.pkl')
# # country = read_list('data/hot_encoding_lists/country_list.pkl')
# region = read_list('data/hot_encoding_lists/region_list.pkl')
# city = read_list('data/hot_encoding_lists/city_list.pkl')
# Asn = read_list('data/hot_encoding_lists/asn_list.pkl')
# Device_type = read_list('data/hot_encoding_lists/device_type_list.pkl')

# print(Ip_Address)
# print(country)
# print(region)
# print(city)
# print(Asn)
# print(Device_type)
# print(len(Ip_Address), len(country), len(region), len(city), len(Asn), len(Device_type))

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')


text = "Mozilla/5.0  (iPhone| CPU iPhone OS 13_4 like Mac OS X) Gecko/20150101 Firefox/20.0.0.1618 (Chrome variation/248113"

# tokenize the test
text = word_tokenize(text)

# remove all punctuation
no_punct = ''.join([char for char in ''.join([word+' ' for word in text]) if (char not in string.punctuation and not char.isdigit())])
print(no_punct)

text = word_tokenize(no_punct)

print(text)