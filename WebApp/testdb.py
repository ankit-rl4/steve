import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')

# Create a cursor object
cur = conn.cursor()

# Execute the query to get column names
cur.execute("PRAGMA table_info(users)")

# Fetch all columns
columns = cur.fetchall()

# Print column names
for column in columns:
    print(column[1])  # column[1] contains the column name

# Close the connection
conn.close()
