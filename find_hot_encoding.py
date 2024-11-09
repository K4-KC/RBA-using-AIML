import pandas as pd
import numpy as np
import pickle

def save_list(list, filename):
    with open(filename, 'wb') as f:
        pickle.dump(list, f)

def read_list(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

Ip_Address = []
country = []
region = []
city = []
Asn = []
Device_type = []

for file in range(24):
    data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
    # attack_data = data.loc[data['Is Account Takeover'] == True][['User ID', 'Round-Trip Time [ms]', 'Is Account Takeover']]
    for index, row in data.iterrows():
        if row['Is Account Takeover'] == True:
            # print(index, row['Is Account Takeover'])
            if row['IP Address'] not in Ip_Address:
                Ip_Address.append(row['IP Address'])
            if row['ASN'] not in Asn:
                Asn.append(row['ASN'])
        # if row['Country'] not in country:
        #     country.append(row['Country'])
        if row['Region'] not in region:
            region.append(row['Region'])
        if row['City'] not in city:
            city.append(row['City'])
        if row['Device Type'] not in Device_type:
            Device_type.append(row['Device Type'])
    print(file, len(Ip_Address), len(country), len(region), len(city), len(Asn), len(Device_type))

save_list(Ip_Address, 'data/hot_encoding_lists/ip_address_list.pkl')
# save_list(country, 'data/hot_encoding_lists/country_list.pkl')
save_list(region, 'data/hot_encoding_lists/region_list.pkl')
save_list(city, 'data/hot_encoding_lists/city_list.pkl')
save_list(Asn, 'data/hot_encoding_lists/asn_list.pkl')
save_list(Device_type, 'data/hot_encoding_lists/device_type_list.pkl')

Ip_Address = read_list('data/hot_encoding_lists/ip_address_list.pkl')
# country = read_list('data/hot_encoding_lists/country_list.pkl')
region = read_list('data/hot_encoding_lists/region_list.pkl')
city = read_list('data/hot_encoding_lists/city_list.pkl')
Asn = read_list('data/hot_encoding_lists/asn_list.pkl')
Device_type = read_list('data/hot_encoding_lists/device_type_list.pkl')

print(Ip_Address)
print(country)
print(region)
print(city)
print(Asn)
print(Device_type)
print(len(Ip_Address), len(country), len(region), len(city), len(Asn), len(Device_type))
