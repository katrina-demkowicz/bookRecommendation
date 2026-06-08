import requests
import json
import time
from utilities import *

def scrape():
        #list of processed books tuples
        book_buffer = []
        #amount of books to be inserted at one time
        buffer_size = 100
                
        for i in range(12566, 50000):
            #fetch book data
            book_ID = i
            copy_ID = get_book_copy(book_ID)
            time.sleep(1)
            # make sure copy_ID isn't None or NULL
            if copy_ID is None:
                continue
            copy_data = get_book_copy_data(copy_ID)
            #process returned book data format into a tuple
            book =     book = process_book(copy_data, book_ID, copy_ID)
            book_buffer.append(book)

            #insert books into table 'books'
            if len(book_buffer) >= buffer_size:
                print(book_buffer)
                insert_books(book_buffer)  
                book_buffer.clear()          

def insert_books(book_buffer):
    sql = '''INSERT INTO books(book_id, copy_id, title, author, summary, subjects) 
        values (?, ?, ?, ?, ?, ?)'''
    return exec_commit_many(sql, book_buffer)

'''Get the first copy of the book that is in a book format'''
def get_book_copy(book_ID):
    url_get_copy_ID = f"https://catalogplus.libraryweb.org/frbr/resources/{book_ID}"
    try:
        # get the array of all the copies and information related to those copies
        array_ID = requests.get(url_get_copy_ID)
        array_ID_object = json.loads(array_ID.text)
        if array_ID_object is None:
            return
        for record in array_ID_object:
            if record['format'] == 'Book':
                copy_ID = record['id']
                return copy_ID
    except requests.exceptions.RequestException as error:
        print(f"Error occurred: {error}")

'''Get important data on the book, like author, subjects, and summary.'''        
def get_book_copy_data(copy_ID):
    if copy_ID is None:
        return
    current_time = time.time_ns() // 1000000
    url_get_copy_data = f"https://catalogplus.libraryweb.org/resource/details/{copy_ID}?_={current_time}"
    try:
        copy_data = requests.get(url_get_copy_data)
        copy_data_object = json.loads(copy_data.text)
        return copy_data_object
    except requests.exceptions.RequestException as error:
        print(f"Error occurred: {error}")

'''Process book data and return a book object'''
def process_book(copy_data, book_ID, copy_ID):
    book_title = ''
    #author format is 'firstname lastname'
    book_author = ''
    book_summary = ''
    book_subjects = ''

    for item in copy_data:
        label = item['label']
        value = item['detailsValues']

        #continue if value is empty
        if not value:
            continue

        #get title
        if label == 'Title':
            full_book_title = value[0]['value']
            book_title = full_book_title.split('/')[0].strip()
            # print(book_title)

        #get author
        if label == 'Author':
            if not value:
                book_author = None
                continue
            author_full_name = value[0]['linkValue']
            if ',' in author_full_name:
                book_author_last = author_full_name.split(',')[0].strip()
                book_author_first = author_full_name.split(',')[1].strip()
                book_author = f'{book_author_first} {book_author_last}'
            else:
                book_author = author_full_name

        #get summary
        if label == 'Summary':
            book_summary = value[0]['value']
            # print(book_summary)

        #get subjects
        if label == 'Subjects':
            subjects = []
            seen = set()

            #go through each value and add it to a list
            for v in value:
                subject = v['value']
                subject = subject.split('--')[0].strip()
                subject = subject.lower()

                #make sure there are no duplicates
                if subject not in seen:
                    subjects.append(subject)
                    seen.add(subject)
            
            book_subjects = json.dumps(subjects)
            # print(book_subjects)
    
    #make book list   
    book = (book_ID, copy_ID, book_title, book_author, book_summary, book_subjects)     
    return book

if __name__ == '__main__':
    #setup_database()
    scrape()
