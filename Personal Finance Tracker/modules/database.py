import sqlite3

# connect to the database or create it if it does not exist
def connect_db():
    conn = sqlite3.connect("data/finance.db")
    return conn

# create tables for categories and transactions if they do not exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # create a table for categories (like food, transport, etc.)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    # create a table for transactions
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

# add a new category to the categories table
def add_category(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# get category id by name (so we can use it later)
def get_category_id(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
    row = cursor.fetchone()  # get the first row that matches
    conn.close()
    if row:
        return row[0]  # return the id of the category
    return None  # return None if category does not exist

# get all categories from the database
def get_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return rows

# delete a category by its id
def delete_categories(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
    conn.commit()
    conn.close()

# update the category name by id
def update_categories(category_id, new_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET name=? WHERE id=?", (new_name, category_id))
    conn.commit()
    conn.close()

# add a new transaction (spending record)
def add_transaction(category_id, amount, date, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (category_id, amount, date, description)
        VALUES (?, ?, ?, ?)
    ''', (category_id, amount, date, description))
    conn.commit()
    conn.close()

# get all transactions from the database
def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, c.name, t.amount, t.date, t.description
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# update a transaction (change the details)
def update_transaction(transaction_id, category_id, amount, date, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET category_id = ?, amount = ?, date = ?, description = ?
        WHERE id = ?
    ''', (category_id, amount, date, description, transaction_id))
    conn.commit()
    conn.close()

# delete a transaction by id
def delete_transactions(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()
