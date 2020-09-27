import sqlite3
from sqlite3 import Error

def conect_create_db_tables(name_of_DB):
    connection_str="{}.db".format(name_of_DB)
    
    try:
        connection = sqlite3.connect(connection_str)
        print("SQL VERSION \n",sqlite3.version)

    except Error as e:
        print(e)

    cursor = connection.cursor() 
    # cursor.execute("drop table if exists client")
    # cursor.execute("drop table if exists account")

    try:   
        cursor.execute("""
            CREATE TABLE "client" (
                "Client_id"	INTEGER NOT NULL UNIQUE,
                "Name"	TEXT NOT NULL,
                "Surname"	TEXT NOT NULL,
                "UMCN"	TEXT NOT NULL UNIQUE,
                "Birthdate"	TEXT NOT NULL,
                "Date_created"	REAL NOT NULL,
                "Client_address"	TEXT NOT NULL,
                PRIMARY KEY("client_id" AUTOINCREMENT)
            );
            """)
        cursor.execute("""
            CREATE TABLE "account" (
                "Account_id"	INTEGER NOT NULL,
                "Account_name"	TEXT NOT NULL,
                "Number"	INTEGER NOT NULL UNIQUE,
                "Date_created"	REAL NOT NULL,
                "Currency"	TEXT NOT NULL,
                "Funds"	INTEGER,
                "ClientAccounts"    INTEGER NOT NULL,
                PRIMARY KEY("account_id" AUTOINCREMENT)
                FOREIGN KEY (clientAccounts)
                REFERENCES client(client_id)
                
            );
                    """)
        
        print("Created tables")
    except sqlite3.OperationalError:
        print( "Tables already exists")
        pass
    
    finally:
        if connection:
            connection.close()
