import sqlite3

def setup_database():
    with sqlite3.connect('library_books.db') as conn:
        cursor = conn.cursor()
        with open('library_books.sql', 'r') as file:
            cursor.executescript(file.read())
        conn.commit()
        return "database tables have been prepared"
    
def exec_commit_many(sql, data):
    with sqlite3.connect('library_books.db') as conn:
            cursor = conn.cursor()
            result = cursor.executemany(sql, data)
            conn.commit()
            return result
    