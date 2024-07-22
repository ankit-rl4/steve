import pandas as pd
import sqlite3

# Read the Excel file
df = pd.read_excel('data_preprocessing/data/dataset_customer.xlsx')


conn = sqlite3.connect('WebApp/users.db')


df.to_sql('users', conn, if_exists='replace', index=False)


conn.close()