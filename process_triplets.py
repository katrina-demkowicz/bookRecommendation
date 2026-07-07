import pandas as pd
import sqlite3
import json

def process_triplets():
    stored_books = grab_book_data()
    #print(stored_books.iloc[2004])
    positives = get_positives(stored_books)

def grab_book_data():
    dataframe = None
    with sqlite3.connect('library_books.db') as conn:
        dataframe = pd.read_sql_query("SELECT book_id, title, author, summary, subjects FROM books " \
        "WHERE (subjects != '' AND subjects IS NOT NULL)" , conn)
        dataframe['subjects'] = dataframe['subjects'].apply(json.loads)
        return dataframe
    
def get_positives(stored_books):
    exploded = stored_books[['book_id', 'subjects']].explode('subjects')
    merged = exploded.merge(exploded, on='subjects')
    merged = merged[merged['book_id_x'] != merged['book_id_y']]
    overlap = merged.groupby(['book_id_x', 'book_id_y']).size().reset_index(name='shared')
    positives = overlap[overlap['shared'] >= 2]
    return positives

if __name__ == '__main__':
    process_triplets()