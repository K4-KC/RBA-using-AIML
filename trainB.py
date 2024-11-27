# import pandas as pd
# import sqlite3 as sql


# conn = sql.connect('data/sql/rba.db')
# c = conn.cursor()

# # c.execute("ALTER TABLE rba ADD COLUMN IP0 'smallint'")
# # c.execute("ALTER TABLE rba ADD COLUMN IP1 'smallint'")
# # c.execute("ALTER TABLE rba ADD COLUMN IP2 'smallint'")
# # c.execute("ALTER TABLE rba ADD COLUMN IP3 'smallint'")

# conn.commit()

# index = 0
# for file in range(24):
#     data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)

#     print('begin adding', file, len(data))

#     for i, ip in data[['index', 'IP Address']].values:
#         ip = ip.split('.')
#         c.execute("""UPDATE rba SET IP0 = (?), IP1 = (?), IP2 = (?), IP3 = (?) 
#         WHERE rowid = (?)""", (ip[0], ip[1], ip[2], ip[3], int(i) + index + 1))
    
#     conn.commit()
#     index += len(data)


# conn.close()-+



# index = 0
# for file in range(2):
#     data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)
#     attack_data = data.loc[data['Is Account Takeover'] == True][['index', 'IP Address']]

#     for j, ip in attack_data.values:
#         ip = ip.split('.')
#         c.execute("""SELECT * FROM rba  
#         WHERE rowid < (?) AND IP0 = (?) AND IP1 = (?) AND IP2 = (?) AND IP3 = (?) AND Is_Account_Takeover = 1""", (index + int(j) + 1, ip[0], ip[1], ip[2], ip[3]))
#         first_entry = c.fetchall()
#         print(ip, ':', len(first_entry))
#         # break
    
#     index += len(data)

# conn.commit()

# conn.close()


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
import tensorflow as tf
import pandas as pd
import sqlite3 as sql
import numpy as np


conn = sql.connect('data/sql/rba.db')
c = conn.cursor()

c.execute("SELECT rowid, * FROM rba")
first_entry = c.fetchone()
print("Row ID:", first_entry[0])
print("User ID:", first_entry[1])
print("Round-Trip Time [ms]", np.frombuffer(first_entry[2], dtype=np.int32))
print("IP Address", np.frombuffer(first_entry[3], dtype=np.int16))
print("Country", np.frombuffer(first_entry[4], dtype=np.int8))
print("Region", np.frombuffer(first_entry[5], dtype=np.int8))
print("City", np.frombuffer(first_entry[6], dtype=np.int8))
print("ASN", np.frombuffer(first_entry[7], dtype=np.int8))
print("UAS", np.frombuffer(first_entry[8], dtype=np.int8))
print("Device Type", np.frombuffer(first_entry[9], dtype=np.int8))
print("Login Successful", first_entry[10])
print("Is Attack IP", first_entry[11])
print("Is Account Takeover", first_entry[12])
print("IP Number", first_entry[13], first_entry[14], first_entry[15], first_entry[16])

inputLength = 294
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(inputLength,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())

blacklist = []
TP, FP, TN, FN = 0, 0, 0, 0
# for file in range(24):
    # data = pd.read_csv(f'data/corrected/rba-split-corrected-{file}.csv', low_memory=False)

c.execute("SELECT max(rowid) from rba")
batch_size = 10000
for batch in range(0, c.fetchone()[0], batch_size):
    print("Batch:", batch//batch_size)
    c.execute("SELECT rowid, * FROM rba WHERE rowid <= (?) AND rowid > (?)", (batch_size + batch, batch))
    inputSQL = c.fetchall()

    inputTensor, outputTensor = [], []
    for i, inputT in enumerate(inputSQL):
        ip = (inputT[13], inputT[14], inputT[15], inputT[16])
        c.execute("""SELECT rowid, * FROM rba WHERE rowid <= (?) 
        AND IP0 = (?) AND IP1 = (?) AND IP2 = (?) AND IP3 = (?)""", (i + 1, ip[0], ip[1], ip[2], ip[3]))
        history = c.fetchall()
        attack = False
        if (inputT[13], inputT[14], inputT[15], inputT[16]) in blacklist:
            attack = True
        else:
            for H in history:
                if H[12] == 1:
                    attack = True
                    blacklist.append((H[13], H[14], H[15], H[16]))
                    print("Blacklist:", blacklist)
                    break
        if attack:
            for H in history:
                inputTensor.append([])
                for RTT in np.frombuffer(H[2], dtype=np.int32): inputTensor[i].append(RTT)
                for IP in np.frombuffer(H[3], dtype=np.int16)[4:]: inputTensor[i].append(IP)
                for country in np.frombuffer(H[4], dtype=np.int8): inputTensor[i].append(country)
                for region in np.frombuffer(H[5], dtype=np.int8): inputTensor[i].append(region)
                for city in np.frombuffer(H[6], dtype=np.int8): inputTensor[i].append(city)
                for ASN in np.frombuffer(H[7], dtype=np.int8): inputTensor[i].append(ASN)
                for UAS in np.frombuffer(H[8], dtype=np.int8): inputTensor[i].append(UAS)
                for device in np.frombuffer(H[9], dtype=np.int8): inputTensor[i].append(device)
                inputTensor[i].append(H[10])
                inputTensor[i].append(H[11])

                outputTensor.append(1)
        else:
            inputTensor.append([])
            for RTT in np.frombuffer(inputT[2], dtype=np.int32): inputTensor[i].append(RTT)
            for IP in np.frombuffer(inputT[3], dtype=np.int16)[4:]: inputTensor[i].append(IP)
            for country in np.frombuffer(inputT[4], dtype=np.int8): inputTensor[i].append(country)
            for region in np.frombuffer(inputT[5], dtype=np.int8): inputTensor[i].append(region)
            for city in np.frombuffer(inputT[6], dtype=np.int8): inputTensor[i].append(city)
            for ASN in np.frombuffer(inputT[7], dtype=np.int8): inputTensor[i].append(ASN)
            for UAS in np.frombuffer(inputT[8], dtype=np.int8): inputTensor[i].append(UAS)
            for device in np.frombuffer(inputT[9], dtype=np.int8): inputTensor[i].append(device)
            inputTensor[i].append(inputT[10])
            inputTensor[i].append(inputT[11])

            outputTensor.append(0)

    inputTensor = tf.convert_to_tensor(inputTensor)
    outputTensor = tf.convert_to_tensor(outputTensor)

    if batch == 0:
        model.fit(inputTensor, outputTensor, epochs=3)
        continue
    
    print('Predicting')
    predictions = model(inputTensor)

    for i, prediction in enumerate(predictions):
        if prediction > 0.5 and outputTensor[i] == 1:
            TP += 1
        elif prediction > 0.5 and outputTensor[i] == 0:
            FP += 1
        elif prediction < 0.5 and outputTensor[i] == 1:
            FN += 1
        elif prediction < 0.5 and outputTensor[i] == 0:
            TN += 1
    
    model.fit(inputTensor, outputTensor, epochs=3)
    

    print("True Positive:", TP)
    print("False Positive:", FP)
    print("True Negative:", TN)
    print("False Negative:", FN)

conn.close()
