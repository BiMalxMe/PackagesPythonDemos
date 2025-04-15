import os 
# Needed to use the basic io functions and acess the file system
import logging
from datetime import datetime
import sqlite3


# If the folder exists then dont create else create the folder named following
os.makedirs("data",exist_ok=True)
os.makedirs("modules",exist_ok=True)
os.makedirs("logs",exist_ok=True)


logging.basicConfig(
    # Defining the place where the logs are to be stred
    filename="logs/app.log",
    #stored in  the file app.log
    #All the logs are loaded 
    level=logging.DEBUG,

    #Way of defining the strucuture of the log
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

#Example of logging and formatting the structure
logging.info("Application stated at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#Connecting to the databse or Create if not exists
def connect_db():
    conn = sqlite3.connect("data/finance.db")
    return conn

#Create tables for tables like transaction categories and accounts
def create_tables():
    conn = connect_db()

    #Cursor is a ponter which allows the database operations to be done
    cursor = conn.cursor()

    #Creating tables with the help of the cursor
    #create a table for categories(food/groceries/entertainment etc)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
                      )
''')
    
    #create table for storing the transactions

    #simple table having a link with the category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
                   id INTEGER PRIMARY KEY,
                   category_id INTEGER,
                   amount REAL,
                   date TEXT,
                   description TEXT,
                   FOREIGN KEY(category_id) REFERENCES categories(id)
                   )
''')
    conn.commit()
    conn.close()

create_tables()

#after defining the table now inserting into it
#adding the category into the category table

def add_category(name):
    conn = connect_db()
    cursor = conn.cursor()

    #THe comma after the name defines that the name is the element of the tuple not just the value
    # Sqlite expects the value to be in a tuple otherwise it will throw the error
    cursor.execute("INSERT INTO categories VALUES (?)",(name,))
    conn.commit()
    conn.close()

#get categories , we can get the list of categories in the form [(1,dsfae),(2,feaf)]
def get_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return rows

#delete the categories in the basis of the category_id
def delete_categories(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id=?",(category_id,))
    conn.commit()
    conn.close()

#update the categories name on the basic of the category_id
def update_categories(category_id,new_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET name=? WHERE id=? ",(new_name,category_id))
    conn.commit()
    conn.close()

#--------------------------Now For The Transactions Table-------------------------------#

#Adding a new transaction

def add_transaction(category_id,amount,date,description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO transactions
(category_id,amount,date,description)
                   VALUES(?,?,?,?)
''',(category_id,amount,date,description))
    conn.commit()
    conn.close()

#Get all the transactions

def get_transactions():
    conn = connect_db()
    cursor =conn.cursor()
    cursor.execute('''
SELECT t.id, c.name , t.amount , t.date , t.description
                   FROM transactions t
                   JOIN categories c ON t.category_id = c.id
                   ORDER BY t.date DESC
''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_transaction(transaction_id,category_id,amount,date,description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
                   SET category_id = ?, amount = ?,date = ?, description = ?
                   WHERE id=?
''',(category_id,amount,date,description,transaction_id))
    conn.commit()
    conn.close()

def  delete_transactions(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?",(transaction_id,))
    conn.commit()
    conn.close()