
import sqlite3
from sqlite3 import Error

# NOTE!!
# run main program to create the db
# run this script after you run main program 

try:
    connection = sqlite3.connect('Banc_Client_DB.db')
except Error as e:
    print(e)

cursor = connection.cursor() 
# cursor.execute("drop table if exists client")
# cursor.execute("drop table if exists account")

try:   
    cursor.execute("""
        insert into client (Name, Surname, UMCN, Birthdate, Date_created, Client_address)values 
        ('Stojan','Stojcevski', '1234567890123', '25/08/1963', datetime('2015-12-17') ,'abvgdge'),
        ('Pero','Perovski', '0123456789012', '12/03/1998',datetime('2012-12-17') ,'abvgdge'),
        ('Marko','Markovski', '2345678901234', '22/05/1989',datetime('2019-03-28') ,'abvgdge'),
        ('Darko','Darkovski', '3456789012345', '12/02/1981',datetime('2018-05-05') ,'abvgdge'),
        ('Trajan','Trajanov', '4567890123456', '25/09/1967',datetime('2015-12-10') ,'abvgdge'),
        ('Goce','Gocev', '5678901234567', '01/01/1956',datetime('2010-10-12') ,'abvgdge');
        """)
    cursor.execute("""
        insert into account (account_name, number, date_created,currency, Funds, ClientAccounts)values
        ('Current Account', '12345678',datetime('2015-12-17'), 'EUR','1000','1'),
        ('Saving Account', '22222222',datetime('2012-12-17'), 'GBP','1000','2'),
        ('Deposit Account', '33333333',datetime('2019-03-28'), 'MKD','1000','3'),
        ('Current Account', '44444444',datetime('2015-12-17'), 'EUR','1000','1'),
        ('Saving Account', '55555555',datetime('2016-08-24'), 'GBP','1000','1'),
        ('Deposit Account', '66666666',datetime('2020-12-17'), 'MKD','1000','2'),
        ('Current Account', '77777777',datetime('2019-03-28'), 'EUR','1000','4'),
        ('Saving Account', '88888888',datetime('2015-12-17'), 'GBP','1000','5'),
        ('Deposit Account', '99999999',datetime('2010-10-19'), 'MKD','1000','6'),
        ('Current Account', '10101010',datetime('2010-10-17'), 'EUR','1000','6'),
        ('Saving Account', '20202020',datetime('2015-12-12'), 'GBP','1000','2'),
        ('Deposit Account', '30303030',datetime('2015-12-17'), 'MKD','1000','5');
                """)
    connection.commit()
    print("Created tables")
except sqlite3.OperationalError:
    print( "Tables already exists")
    pass

finally:
    if connection:
        connection.close()