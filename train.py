import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
import sqlite3 as sql


conn = sql.connect('data/sql/rba.db')
c = conn.cursor()

c.execute("SELECT rowid, * FROM rba WHERE rowid")
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

c.execute("SELECT rowid, * FROM rba WHERE rowid < 10")
inputSQL = c.fetchall()

inputTensor = []


# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])
