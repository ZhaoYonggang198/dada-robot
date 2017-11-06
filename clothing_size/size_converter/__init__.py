import size_converter_error as sc_error
from converter import convert_size

# Get an array from the data
if __name__ == '__main__': 
    try:
        print convert_size("men shoes", "China", "Italy", "38")
    except sc_error.SizeConverterError as e:
        print e