import requests
import json
import time

def scrape():
    # for the first attempt, going to scrape the library's page on
    # Toni Morrison's Jazz
    copy_ID = get_book_copy(142763)
    # make sure copy_ID isn't None or NULL
    copy_data = get_book_copy_data(copy_ID)
    print(copy_data)

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

def insert_book(copy_data):
    pass

if __name__ == '__main__':
    scrape()

