"""This is the "menester.py" module and it provides one function called print_lol() 
   which prints lists that may or may not include nested.lists."""

movies = ["A", 1975, "B", 91,
           ["C", ["D", "E",
                  "F", "G", "H"]]]

def print_lol(the_list):
    """This function takes one positional argument called "the list", which 
       is any Python list (of - possibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line."""
    for each_item in the_list:
         if isinstance(each_item, list):
             print_lol(each_item)
         else:
             print(each_item)
             
print_lol(movies)
