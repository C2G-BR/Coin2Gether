import psycopg2
import sqlalchemy
from sqlalchemy import text


# Test Case 1
conn = psycopg2.connect(dbname="postgres",
                        user="root",
                        host="127.0.0.1",
                        password="1234",
                        port="5432")
cursor = conn.cursor()
cursor.execute('SELECT * FROM information_schema.tables')
rows = cursor.fetchall()
for table in rows:
    print(table)
conn.close()


# Test Case 2
engine = sqlalchemy.create_engine('postgresql+psycopg2://root:1234@localhost:5432/postgres')
conn = engine.connect()
conn.execute(text("commit"))
conn.execute(text("create database testaaa;"))
conn.close()