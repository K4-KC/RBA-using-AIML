import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
import sqlite3 as sql


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

c.execute("SELECT rowid, * FROM rba WHERE rowid < 100000")
inputSQL = c.fetchall()

inputTensor, outputTensor = [], []
for i in range(100000):
    inputTensor.append([])
    for RTT in np.frombuffer(inputSQL[0][2], dtype=np.int32): inputTensor[i].append(RTT)
    for IP in np.frombuffer(inputSQL[0][3], dtype=np.int16)[4:]: inputTensor[i].append(IP)
    for country in np.frombuffer(inputSQL[0][4], dtype=np.int8): inputTensor[i].append(country)
    for region in np.frombuffer(inputSQL[0][5], dtype=np.int8): inputTensor[i].append(region)
    for city in np.frombuffer(inputSQL[0][6], dtype=np.int8): inputTensor[i].append(city)
    for ASN in np.frombuffer(inputSQL[0][7], dtype=np.int8): inputTensor[i].append(ASN)
    for UAS in np.frombuffer(inputSQL[0][8], dtype=np.int8): inputTensor[i].append(UAS)
    for device in np.frombuffer(inputSQL[0][9], dtype=np.int8): inputTensor[i].append(device)
    inputTensor[i].append(inputSQL[0][10])
    inputTensor[i].append(inputSQL[0][11])

    outputTensor.append([inputSQL[0][12]])

# print(inputTensor)
# print(outputTensor)

inputTensor = tf.convert_to_tensor(inputTensor)
outputTensor = tf.convert_to_tensor(outputTensor)

inputLength = len(inputTensor[0])
print("Length of input:", inputLength)

# input length is 294
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(inputLength,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print(model.summary())

model.fit(inputTensor, outputTensor, epochs=10)
