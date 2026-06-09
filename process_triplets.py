import pandas as pd
import sqlite3

def process_triplets():
    stored_books = grab_book_data()

def grab_book_data():
    dataframe = None
    with sqlite3.connect('library_books.db') as conn:
        dataframe = pd.read_sql_query("SELECT book_id, title, author, summary, subjects FROM books " \
        "WHERE (summary != '' AND summary IS NOT NULL) OR (subjects != '' AND subjects IS NOT NULL)" , conn)
        return dataframe

if __name__ == '__main__':
    process_triplets()