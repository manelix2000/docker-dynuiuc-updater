import sqlite3
import sys
import os
from sqlite3 import Error
from dataclasses import dataclass
from apiresponse import ApiResponse

def init_db(db_file):
    db_directory = os.path.dirname(db_file)

    # Ensure the directory exists; create it if necessary
    if db_directory and not os.path.exists(db_directory):
        print(f"Creating directory: {db_directory}")
        os.makedirs(db_directory)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        
        # Create a metadata table if it doesn't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS DB_METADATA (
                            OPERATION CHAR(100) PRIMARY KEY NOT NULL,
                            STATUS    INT NOT NULL);''')
        
        # Check if the DROP operation has been executed before
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM DB_METADATA WHERE OPERATION = 'DROP_LAST_STATUS'")
        result = cur.fetchone()

        # If no record found, execute DROP TABLE
        if result[0] == 0:
            conn.execute("DROP TABLE IF EXISTS LAST_STATUS;")

            # Mark the operation as done by inserting a record into DB_METADATA
            conn.execute("INSERT INTO DB_METADATA (OPERATION, STATUS) VALUES ('DROP_LAST_STATUS', 1)")

        conn.execute('''CREATE TABLE IF NOT EXISTS LAST_STATUS
                     (API     CHAR(100)          NOT NULL,
                     CODE            INT     NOT NULL,
                     LAST_RESPONSE        CHAR(100),
                     TIMESTAMP            INT     NOT NULL,
                     IP     CHAR(100)          NULL);''')

        conn.commit()
        print(f"Successfully initialized sqlite db: {sqlite3.version} database: {db_file}")
    except Error as e:
        print(f"Error initializing sqlite: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def update_db(db_file: str, api: str, code: int, msg: str, timestamp: int, ip: str = None):
    conn = sqlite3.connect(db_file)
    conn.execute(
        f"""INSERT INTO LAST_STATUS (API,CODE,LAST_RESPONSE,TIMESTAMP,IP) VALUES (\'{api}\', {code}, \'{msg}\', {timestamp}, ?)""", (ip,))

    conn.commit()
    conn.close()


def get_from_db(db_file: str):
    dynuResp_list = []

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM LAST_STATUS;""")
    records = cur.fetchall()
    for row in records:
        # Populate the lists with ApiResponse objects.
        response = ApiResponse(api=row[0], code=row[1], msg=row[2], timestamp=row[3], ip=row[4])
        dynuResp_list.append(response)

    conn.close()

    return dynuResp_list
