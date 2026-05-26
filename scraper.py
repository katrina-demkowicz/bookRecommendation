import requests
import json
import time
from book import Book

def scrape():
    # for the first attempt, going to scrape the library's page on
    # Toni Morrison's Jazz
    book_ID = 142763
    #book_ID = 855335
    copy_ID = get_book_copy(book_ID)
    # make sure copy_ID isn't None or NULL
    copy_data = get_book_copy_data(copy_ID)
    process_book(copy_data, book_ID, copy_ID)

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
    book_author_first = ''
    book_author_last = ''
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
            author_full_name = value[0]['linkValue']
            book_author_last = author_full_name.split(',')[0].strip()
            book_author_first = author_full_name.split(',')[1].strip()
            # print(book_author_last)
            # print(book_author_first)

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
                subject = subject.replace(' -- Fiction', '').strip()
                subject = subject.lower()

                #make sure there are no duplicates
                if subject not in seen:
                    subjects.append(subject)
                    seen.add(subject)
            
            book_subjects = json.dumps(subjects)
            # print(book_subjects)
    
    #make book object
    book = Book(book_ID, copy_ID, book_title, book_author_first, 
                book_author_last, book_summary, book_subjects)     
    return book

if __name__ == '__main__':
    scrape()

