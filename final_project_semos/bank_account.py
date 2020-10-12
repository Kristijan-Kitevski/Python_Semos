from datetime import datetime, timedelta
from create_db import conect_create_db_tables

import sqlite3
from sqlite3 import Error
import create_db




class Client():
    
    def __init__(self, first_name, last_name, UMCN, birthdate, address):
        self.first_name = first_name
        self.last_name = last_name
        self.umcn = UMCN
        self.birthdate = birthdate
        self.address = address
        self.creation_date = self.create_date()
        
    
    def create_date(self):
        create = datetime.now()
        ceration = create.strftime('%Y-%m-%d %H:%M:%S')
        return ceration

    @staticmethod
    def validate_birthdey_input():
        birthdate_in=''
        while True:
            birthdate= input("Please enter date of birth (dd/mm/yyyy): ")
            try:
                datetime.strptime(birthdate, "%d/%m/%Y")
                birthdate_in=birthdate
                break
            except ValueError:
                print ("Incorrect format")
        return birthdate_in
   
    @staticmethod
    def get_birthdate_from_umcn(umcn):
        birthdate = f"{umcn[0]}{umcn[1]}/{umcn[2]}{umcn[3]}/1{umcn[4]}{umcn[5]}{umcn[6]}"
        return birthdate 
    
    @staticmethod
    def validate_UMCN(UMCN):
        if len(str(UMCN)) != 13:
            print('Invalid UMCN: {}'.format(UMCN))
            return False
        en=[int(x) for x in str(UMCN)]  
        m = 11 - ((7*(en[0]+en[6])+6*(en[1]+en[7])+5*(en[2]+en[8])+4*(en[3]+en[9])+3*(en[4]+en[10])+2*(en[5]+en[11]))%11)
        if m!=en[12]:
            print("UMCN not valid") 
            return False
        if m in range(1,10):
            if en[12]==m:
                print("UMCN is valid")   
                return True
        if m==10:
            raise Exception("Check sum canot be calculated, some of first 12 characters are not correct")
        if m==11 and en[12]==0:
                print("UMCN is valid")
                return True
 
    @staticmethod
    def check_umcn():
        UMCN_in=0
        while True:
            umcn = input("Please enter client UMCN: ")
            if Client.validate_UMCN(umcn):
                UMCN_in=umcn
                break
            else:
                print("Enter valid UMCN!!!")
        return UMCN_in

    @staticmethod
    def check_if_valid_string_input(variable_name):
        while True:
            input_str= input(f"Please enter client {variable_name}: ").capitalize()
            if input_str.isalpha():
                return input_str
            else:
                print(f"Enter valid first {variable_name}!!!")
            
    @staticmethod
    def add_client():
        
        first_name_in = Client.check_if_valid_string_input("name")
        last_name_in = Client.check_if_valid_string_input("surname")  
        UMCN_in=Client.check_umcn()
        birthdate_in= Client.get_birthdate_from_umcn(UMCN_in)
        address_in = input("Please enter client address: ").capitalize()
        
        client= Client(first_name_in,last_name_in,UMCN_in,birthdate_in,address_in)    
        Operations_with_db.add_client_to_db(client)
          
class Account(): 
    
    def __init__(self, account_type, balance, currency ):
       
        self.name = account_type
        self.acc_number= self.create_unique_account_number()
        self.account_balance = balance
        self.creation_date = Client.create_date(self)
        self.currency = currency
   
    def create_unique_account_number(self):
        import random
        import string
        return ''.join(random.choices(string.digits, k=8))
        # proverka za validacija dali postoi toj account nekade 
    
    @staticmethod
    def add_account_name():
        type_of_account_in = ''
        while True:
            account_choice =input('''        
                Please enter type of account: 
                1. Current Accounts    
                2. Term Deposits   
                3. Savings Accounts
                4. Loan    
                b. Back        
                                   ''').lower()
            if account_choice=="1":
                type_of_account_in= "Current Accounts"
                break
            if account_choice=="2":
                type_of_account_in= "Term Deposits"
                break
            if account_choice=="3":
                type_of_account_in= "Savings Accounts"
                break
            if account_choice=="4":
                type_of_account_in= "Loan"  
                break 
            if account_choice=="b": 
                Menu.main_menu()
            else:
                print("Enter valid choice (ex. 1)!")
        return type_of_account_in    
        
    @staticmethod
    def balance_input_check():
        balance_in = ''   
        while True:   
            balance =input("Please enter account funds: ")
            if balance.isdigit():
                balance_in=int(balance)
                break
            else:
                print("Enter valid funds!!!")
        return balance_in
    
    @staticmethod
    def add_currency():   
        currency_in = ''
        while True:
            print("Enter one of the following currencies: EUR, MKD, USD or CHF")
            currency =(input("Please enter currency: ")).upper()
            if currency.isalpha():
                if currency=="EUR" or currency=="MKD"or currency=="USD" or currency=="CHF":
                    currency_in=currency
                    break
            else:
                print("Invalid currency -- the program works only with following currencies!")
        return currency_in
        
    @staticmethod
    def add_new_account():
        type_of_account_in = Account.add_account_name()
        balance_in = Account.balance_input_check()
        currency_in = Account.add_currency()
   
        acc= Account( type_of_account_in, balance_in, currency_in)
        # print(acc.__dict__)
        Operations_with_db.add_account_to_db(acc)
     

# ---------------------------------------------------------------------
# functions for db-main menu

class Operations_with_db():

    @staticmethod
    def add_client_to_db(Client):
        # check if user is in database before inserting new user with same data 
        try:
            connection = sqlite3.connect(database_name+".db")
            cursor = connection.cursor()
            
            sql_insert_client = '''
                INSERT into 'client' (
                'Name','Surname','UMCN','Birthdate','Client_address','Date_created'
                )
                values(?,?,?,?,?,?);
            '''
            tuple_of_data =(Client.first_name, Client.last_name, Client.umcn, Client.birthdate, Client.address, Client.creation_date,)
            
            # checking if user exist in DB
            cursor.execute('SELECT EXISTS(SELECT * from client WHERE UMCN=?)',(Client.umcn,))
            exist =cursor.fetchone()
            condition=bool(exist[0])
            cursor.close()
            if not condition: 
                cursor = connection.cursor() 
                cursor.execute(sql_insert_client, tuple_of_data)
                connection.commit()
                print('New client added successfully')
            else :
                print("Client that you are trying to add already exist in records")
                print("Try edit client to modify existing client")
                Menu.main_menu()
        except Error as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod     
    def add_account_to_db(Account):
        
        UMCN_in = Client.check_umcn()
        try:
            connection = sqlite3.connect(database_name+".db")
            cursor = connection.cursor()
            cursor.execute('SELECT client_id FROM client WHERE UMCN ==?',(UMCN_in,))
            clientID= cursor.fetchone()  
            sql_insert_account = '''
                INSERT into 'account' (
                'Account_Name','Number','Date_created','Currency','Funds','ClientAccounts'
                )
                values(?,?,?,?,?,?);
            '''
            tuple_of_data = (Account.name, Account.acc_number, Account.creation_date, Account.currency, Account.account_balance, clientID[0],)
            
            cursor.execute(sql_insert_account, tuple_of_data)
            connection.commit()
            print('New account added successfully')
        except TypeError:
            print("Client that you trying to open account doesn't exist")
        except Error as e:
            
            print(e)
        finally:
            if connection:
                connection.close()   

    @staticmethod
    def edit_account(client_umcn):
        connection = sqlite3.connect(database_name+".db")
        cursor = connection.cursor()  
        cursor.execute('SELECT client_id FROM client WHERE UMCN = ?',(client_umcn,))
        picked_client = cursor.fetchone()  
        client_id=picked_client[0] 
        print(client_id)
        cursor.execute('SELECT account_name, number, date_created, currency, funds FROM account WHERE ClientAccounts=?',(client_id,))
        results = cursor.fetchall()
        if results:
            print("Client Accounts")
            from tabulate import tabulate
            
            print (tabulate(results, headers=["Account", "Nnumber", "Date Created", "Currency","Funds"]))  
                
            acc_n = input("Enter account number to edit: ").lower()
            to_edit= input('''Choose what would you like to edit:
                        1. Account name
                        2. Account currency
                        3. Delete account
                        4. Account Value
                        b. Back
                        ''')
            
            if to_edit == "1": 
                accname = Account.add_account_name()
                cursor.execute(('''UPDATE account
                            SET Account_name = ?
                            WHERE Number = ? '''),(accname, acc_n,))
                print("Name changed!")
                
            elif to_edit == "2":
                acccur =Account.add_currency()
                cursor.execute(('''UPDATE account
                            SET Currency = ?
                            WHERE Number= ?'''),(acccur, acc_n,))
                print("Currency changed!")
                
            elif to_edit == "3":
                cursor.execute(('''DELETE FROM account
                        WHERE Number= ? '''),(acc_n,))
                print("Account deleted!")
                
            elif to_edit == "4":
                new_funds=input("Enter new funds:")
                if new_funds.isdigit():
                    cursor.execute(('''UPDATE account
                                SET funds = ?
                                WHERE Number= ?'''),(new_funds, acc_n,))
                else:
                    print("Enter valid number")
                    
            elif to_edit == "b":
                Operations_with_db.edit_client()
        else:
            print("Client have no account/s")
            c=input("Would you like to open financial account for this client? (y/n) ").lower()
            if c=="y":
                Account.add_new_account()
            else:
                pass
        connection.commit()
        
    @staticmethod    
    def edit_client():
        client_umcn= Client.check_umcn()     
        try: 
            connection = sqlite3.connect(database_name+".db")
            cursor = connection.cursor()        
            cursor.execute('SELECT Name, Surname from client WHERE UMCN= ?',(client_umcn,)) 
            picked_client = cursor.fetchone()  
            firstname=picked_client[0]
            
        except TypeError:
            print("No client with this UMCN") 
            pick= input("Would you like to add one?(y/n) ").lower()
            if pick=="y":
                Client.add_client()
            else:    
                return
        
        finally:
            if connection:
                connection.close()
        
        print("Choose what would you like to edit: ")
        print('''   
                    1. First Name
                    2. Last Name
                    3. UMCN   
                    4. Bitrhdate
                    5. Address
                    6. Edit Accounts
                    q. Quit
                ''')
        pick=input("Enter number: ").lower()
                    
        connection = sqlite3.connect(database_name+".db")
        cursor = connection.cursor()
        
        if pick == "1":
            firstname = Client.check_if_valid_string_input("name")
            cursor.execute('''UPDATE client 
                        SET Name = ? 
                        WHERE UMCN= ? ''',(firstname, client_umcn,))
            print("Name changed!")
        elif pick == "2":
            lastname = Client.check_if_valid_string_input("surname")
            cursor.execute(('''UPDATE client
                            SET Surname = ?
                            WHERE UMCN= ? '''),(lastname, client_umcn,))
            print("Surname changed!")
            
        elif pick == "3":
            umcn =Client.check_umcn()
            cursor.execute(('''UPDATE client
                            SET UMCN = ?
                            WHERE UMCN= ? '''),(umcn, client_umcn,))
            print("UMCN changed!")
            
        elif pick == "4":
            birthday =Client.validate_birthdey_input()
            cursor.execute(('''UPDATE client
                            SET Birthdate = ?
                            WHERE UMCN= ? '''),(birthday, client_umcn,))
            print("Birthdate changed!")
        
        elif pick == "5":
            adddress_input =input("Enter new address: ")
            cursor.execute(('''UPDATE client
                            SET Client_address = ?
                            WHERE UMCN= ?  '''),(adddress_input, client_umcn,))
            print("Address changed!")
        
        elif pick == "6":
            Operations_with_db.edit_account(client_umcn)
            
        elif pick == "q":
            return
        else:
            print("Invalid input")
        connection.commit()
    
    @staticmethod
    def delete_client():
        
        client_umcn = Client.check_umcn()
                            
        connection = sqlite3.connect(database_name+".db")
        cursor = connection.cursor()
                
        try:            
            cursor.execute('SELECT Name, Surname from client WHERE UMCN= ?',(client_umcn,)) 
            picked_client = cursor.fetchone()  
            firstname=picked_client[0]
            lastname=picked_client[1]    
        except TypeError:
            print("No client with this UMCN") 
            return
            
        if picked_client:
            print("You have selected {} {}".format(firstname,lastname))
            decide = input("Are you shure you want to delete your client {} {}? (y/n)".format(firstname,lastname)).lower()
            if decide=="y":
                cursor.execute('SELECT client_id FROM client WHERE UMCN = ?',(client_umcn,))
               
                picked_client = cursor.fetchone()  
                client_id=picked_client[0] 
                if client_id:                
                    cursor.execute('DELETE FROM account WHERE ClientAccounts=?',(client_id,))           
                cursor.execute('DELETE from client WHERE UMCN=?',(client_umcn,))
                connection.commit()
                print("Client deleted successfully!")
        else:
            print("Client does not exist!")
            return     
    
    @staticmethod
    def search_client():
        print('''
            Search client by:
            1. UMCN
            2. Account number
            ''')
        inp = input()
        
        try:
            if  inp =="1":
                umcn = Client.check_umcn()
                connection = sqlite3.connect(database_name+".db")
                cursor = connection.cursor()
           
                cursor.execute('''
                                SELECT *
                                FROM  client
                                INNER JOIN account
                                ON client.client_id = account.clientaccounts 
                                WHERE client.UMCN=?
                                ORDER by client.Surname        
                    ''',(umcn,)) 
                results =cursor.fetchall()
                if not results:
                    cursor.execute('''
                                    SELECT *
                                    FROM  client
                                    WHERE client.UMCN=?
                                    ORDER by client.Surname        
                        ''',(umcn,)) 
                    results =cursor.fetchall()
            elif inp == "2":
                account_number=input("Enter account umber: ")
                if account_number.isdigit() and len(account_number)==8:
                    connection = sqlite3.connect(database_name+".db")
                    cursor = connection.cursor()
                    try:
                        cursor.execute('''
                                        SELECT client.client_id
                                        FROM  client
                                        INNER JOIN account
                                        ON client.client_id = account.clientaccounts 
                                        WHERE account.number=?     
                            ''',(account_number,)) 
                        
                        r1= cursor.fetchone()
                        cursor.execute('''
                                    SELECT *
                                    FROM  client
                                    INNER JOIN account
                                    ON client.client_id = account.clientaccounts 
                                    WHERE client.client_id=?
                                    ORDER by client.Surname        
                        ''',r1) 
                        results =cursor.fetchall()
                    except ValueError:
                        print ("Account doesn't exist or")
                        results = False
                else:
                    print("Invalid account number")
                    Operations_with_db.search_client()
            else: 
                print("Invalid input")
                Operations_with_db.search_client()
                
            if results:
               
                for row in results:
                    print()
                    print("Client: ")
                    print("Name: ", row[1])
                    print("Surname: ", row[2])
                    print("UMCN: ", row[3])
                    print("Birthdate: ", row[4])
                    print("Date Created: ", row[5])
                    print("Address: ", row[6])
                    print()
                    print("Client Accounts: ")
                    print()
                    break
                try:
                    if row[8]:
                        for row in results:
                            print("Account name: ", row[8])
                            print("Account number: ", row[9])
                            print("Date Created: ", row[10])
                            print("Funds: ", row[12])
                            print("Currency: ", row[11])
                            print()
                except IndexError:
                    print("No accounts")
            else:
                print("Client doesent exist in records")
            
        except Error as e:
            print(e)
        finally:
            if connection:
                connection.close()   
                
  
    @staticmethod       
    def list_all_clients():
        try:
            connection = sqlite3.connect(database_name+".db")
            cursor = connection.cursor()
            order_by=""
            print('''
        Please select what to order by: 
            1. Name
            2. Surname
            3. Date              
                ''')
            choice=input()
            while True:
                if choice=="1":
                    order_by='name'
                    break
                elif choice=="2":
                    order_by='surname'
                    break
                elif choice=="3":
                    order_by='date_created'
                    break
                else:
                    print("Invalid input")
                    return

            cursor.execute(('''
                            SELECT name, surname, umcn, birthdate, client_address, date_created
                            FROM  client
                            ORDER by {}
                ''').format(order_by)) 
            def getlimitedRows(size):
                try:
                    records = cursor.fetchmany(size)
                    from tabulate import tabulate
                    if records:
                        print (tabulate(records, headers=["Name", "Surname", "UMCN", "Birthdate","Address", "Date created"]))   
                        nex = input("Pres 'n' for next pg  or q to exit: ")
                        if nex == "n":
                            getlimitedRows(size)
                        else:
                            return
                    else:
                        cursor.close()
                        print("End of data no more clients in database")
                except sqlite3.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
            getlimitedRows(5)
       
        except Error as e:
            print(e)
        finally:
            if connection:
                connection.close()   
            
                    
class Menu():
    
    @staticmethod 
    def main_menu_text():
        
            print("""
                1) Enter new client.
                2) Edit client.
                3) Add client Account
                4) Show all clients.
                5) Search client.
                6) Delete client.
                
        Type "q" to quit the program of "h" for help.
                
                """)
            choise = input("Please select one of the options above: ").lower()
            
            return choise
        
    @staticmethod
    def finish_line():# prints decoration and stops script until button is pressed
        input("Press any button to continue")
        decor2 = "-"*50
        print(decor2)
        
    @staticmethod    
    def main_menu():
        while True:
            decor1 = "*"*50
            print(decor1)
            print("Welcome to the BANK clients management CLI")
            print(decor1)
            choise =Menu.main_menu_text()
            print(decor1)
            if choise == "1":
                Client.add_client()
                c=input("Would you like to open financial account for this client? (y/n) ").lower()
                if c=="y":
                    Account.add_new_account()
                else:
                    pass
                Menu.finish_line()
                
            elif choise == "2":
                Operations_with_db.edit_client()
                Menu.finish_line()
                
            elif choise == "3":
                Account.add_new_account()
                Menu.finish_line()
                
            elif choise == "4":  
                Operations_with_db.list_all_clients()
                Menu.finish_line()
            
            elif choise == "5":
                Operations_with_db.search_client()
                Menu.finish_line()
            
            elif choise == "6":    
                Operations_with_db.delete_client()
                Menu.finish_line()
                
            elif choise == "h":
                with open ("help.txt") as help:
                    f = help.read()
                    print(f)
                Menu.finish_line()
                
            elif choise =="q":
                import sys
                sys.exit(0)
# ---------------------------------------------------------------------
# main program menu
# in case you like to change name of db
database_name='Banc_Client_DB'

conect_create_db_tables(database_name)
    
Menu.main_menu()     
        

    
        
        

   