import pandas as pd
import sqlite3
import json
import random

def process_triplets():
    stored_books = grab_book_data()
    #print(stored_books.iloc[2004])
    get_triplets(stored_books)

def grab_book_data():
    df = None
    with sqlite3.connect('library_books.db') as conn:
        df = pd.read_sql_query("SELECT book_id, title, author, summary, subjects FROM books " \
        "WHERE (subjects != '' AND subjects IS NOT NULL)" , conn)
        df['subjects'] = df['subjects'].apply(json.loads)
        return df
    
def get_triplets(stored_books):
    exploded = stored_books[['book_id', 'subjects']].explode('subjects')
    #get positive pairs
    merged = exploded.merge(exploded, on='subjects')
    merged = merged[merged['book_id_x'] != merged['book_id_y']]
    overlap = merged.groupby(['book_id_x', 'book_id_y']).size().reset_index(name='shared')
    positives = overlap[overlap['shared'] >= 2]
    positives.to_csv("positives.csv", index=False)
    #set used for negative sampling
    positive_set = set(zip(positives['book_id_x'], positives['book_id_y']))
    
    #get negative pairs
    all_ids = stored_books['book_id'].tolist()
    negative_pairs = []
    for book_id in all_ids:
        candidates = [i for i in all_ids if i != book_id]
        for candidate in random.sample(candidates, min(50, len(candidates))):
            if (book_id, candidate) not in positive_set:
                negative_pairs.append((book_id, candidate))
                break
    negatives = pd.DataFrame(negative_pairs, columns=['book_id_x', 'book_id_y'])
    negatives.to_csv("negatives.csv", index=False)


if __name__ == '__main__':
    process_triplets()