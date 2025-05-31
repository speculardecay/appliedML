from library.book import Book
from library.library import Library

if __name__ == "__main__":

    #the main database for the library to pass to the class
    database = "./database.json"
    my_library = Library(database)
    usr_choice = -1

    print("------------------------")
    print("Welcome to your local Library")
    while usr_choice != 7:
        print("\nPlease choose your action")
        print("0 : View all books")
        print("1 : View your retrieved books")
        print("2 : Retrieve a book")
        print("3 : Bring back a book")
        print("4 : Search books")
        print("5 : Add book to Library")
        print("6 : Remove book from Library")
        print("7 : Exit")
        usr_choice = int(input("Action : "))

        match usr_choice:
            case 0:
                print("\nAll books in the Library")
                my_library.get_all_books(verbose=1)
            case 1:
                print("\nAll your retrieved books")
                my_library.search_retrieved_books()
            case 2:
                print("\nWhich book do you want to retrieve?")
                my_library.retrieve_book_by_selection()
            case 3:
                print("\nWhich book do you want to bring back?")
                my_library.bring_back_book_by_selection()
            case 4:
                print("\nSearch books")
                query = input("Enter your search query: ")
                my_library.search_books(query)
            case 5:
                print("\nAdd book to Library")
                usr_name = input("Book name: ")
                usr_author = input("Book author: ")
                usr_type = input("Book type: ")
                new_book = Book(usr_name, usr_type, usr_author, 1, 0)
                my_library.add_book_to_library(new_book)
            case 6:
                print("\nRemove book from Library")
                my_library.remove_books_from_library_by_selection()
            case 7:
                print("\nCiao!")
            case _:
                print("Action does not exist")


