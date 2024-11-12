import pandas as pd
import sqlite3 as sql
import numpy as np
import pickle
import nltk
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')


def read_list(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_one_hot_encoding(list, elem):
    encoding = [0] * len(list)
    try: encoding[list.index(elem)] = 1
    except: pass
    return encoding

def get_one_hot_encoding_list(list, elemList):
    encoding = [0] * len(list)
    for elem in elemList:
        try: encoding[list.index(elem)] = 1
        except: pass
    return encoding


conn = sql.connect('data/sql/rba.db')
c = conn.cursor()

drop_table = """ DROP TABLE IF EXISTS rba; """
c.execute(drop_table)

create_table = """ CREATE TABLE IF NOT EXISTS rba (
    User_ID INT,
    Round_Trip BLOB,
    IP_Address BLOB,
    Country BLOB,
    Region BLOB,
    City BLOB,
    ASN BLOB,
    UAS BLOB,
    Device_Type BLOB,
    Login_Successful BOOL,
    Is_Attack_IP BOOL,
    Is_Account_Takeover BOOL
); """
c.execute(create_table)

Ip_Address = read_list('data/hot_encoding_lists/ip_address_list.pkl')
country = read_list('data/hot_encoding_lists/country_list.pkl')
region = read_list('data/hot_encoding_lists/region_list.pkl')
city = read_list('data/hot_encoding_lists/city_list.pkl')
Asn = read_list('data/hot_encoding_lists/asn_list.pkl')
Uas = read_list('data/hot_encoding_lists/uas_list.pkl')
Device_type = read_list('data/hot_encoding_lists/device_type_list.pkl')

add = []


for file in range(24):
    data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
    # sql_data = data.loc[data['Is Account Takeover'] == True][['User ID', 'Round-Trip Time [ms]', 'Is Account Takeover']]
    sql_data = data
    
    print('begin adding', len(sql_data))
    
    for index, row in sql_data.iterrows():
        if index % 100000 == 0:
            print(index)
            c.executemany("INSERT INTO rba VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", add)
            # conn.commit()
            add = []
        Uas_ = word_tokenize(row['User Agent String'])
        Uas_ = ''.join([char for char in ''.join([word+' ' for word in Uas_]) if (char not in string.punctuation and not char.isdigit())])

        add.append((row['User ID'], 
                    np.array((True, int(row['Round-Trip Time [ms]'])), dtype=np.int32).tobytes() if not np.isnan(row['Round-Trip Time [ms]']) else np.array((False, 0), dtype=np.int32).tobytes(), 
                    np.array((row['IP Address']).split('.') + get_one_hot_encoding(Ip_Address, row['IP Address']), dtype=np.int16).tobytes(),
                    np.array(get_one_hot_encoding(country, row['Country']), dtype=np.bool).tobytes(),
                    np.array(get_one_hot_encoding(region, row['Region']), dtype=np.bool).tobytes(),
                    np.array(get_one_hot_encoding(city, row['City']), dtype=np.bool).tobytes(),
                    np.array(get_one_hot_encoding(Asn, row['ASN']), dtype=np.bool).tobytes(),
                    np.array(get_one_hot_encoding_list(Uas, Uas_), dtype=np.bool).tobytes(),
                    np.array(get_one_hot_encoding(Device_type, row['Device Type']), dtype=np.bool).tobytes(),
                    True if row['Login Successful'] == True else False,
                    True if row['Is Attack IP'] == True else False,
                    True if row['Is Account Takeover'] == True else False))

c.execute("SELECT * FROM rba")
first_entry = c.fetchone()
print("User ID:", first_entry[0])
print("Round-Trip Time [ms]", np.frombuffer(first_entry[1], dtype=np.int32))
print("IP Address", np.frombuffer(first_entry[2], dtype=np.int16))
print("Country", np.frombuffer(first_entry[3], dtype=np.int8))
print("Region", np.frombuffer(first_entry[4], dtype=np.int8))
print("City", np.frombuffer(first_entry[5], dtype=np.int8))
print("ASN", np.frombuffer(first_entry[6], dtype=np.int8))
print("UAS", np.frombuffer(first_entry[7], dtype=np.int8))
print("Device Type", np.frombuffer(first_entry[8], dtype=np.int8))
print("Login Successful", first_entry[9])
print("Is Attack IP", first_entry[10])
print("Is Account Takeover", first_entry[11])

conn.commit()

conn.close()
