import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

#connect to database
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="567098")
cur = conn.cursor()

for _ in range(3):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))


# Insert random status into the status table
status_values = [('new',), ('in progress',), ('completed',)]
cur.executemany("INSERT INTO status (name) VALUES (%s)", status_values)



for _ in range(3):
    title = fake.text(max_nb_chars=100)
    description = fake.text()
    status_id = random.randint(1, 3)  # Assuming you have 3 statuses
    user_id = random.randint(1, 3)    # Assuming you have 3 users
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id))



try:
    #saving changes
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    #exiting connection
    cur.close()
    conn.close()



