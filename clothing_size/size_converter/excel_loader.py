import pyexcel
import re

CATEGORY_DELIMITERS = '/| |;|,'
def parse_tags(name):
    return re.split(CATEGORY_DELIMITERS, name)

def get_size_dictionary(name):
    book = pyexcel.get_book(file_name=name)
    sheets = book.to_dict()
    return sheets
