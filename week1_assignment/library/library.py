import json
from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils
from library.file_io import Fstream
from library.book import Book

@dataclass
class Library:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

    def get_all_books(self, verbose=0)->dict:
        """
        Reads and returns a hash map with all the available books
        Args:
            If verbose is set to 1, print all books and return all books, otherwise only return all books
        Returns
            dict: a hash map with all books in database
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_json_structure(data_file)
                return data_file
            else:
                return data_file
            
        except:
            raise ValueError("The value for the verbose has to be 0 or 1")


    def search_books(self, query: str)->list[Book]:
        """
        """
        data = Fstream.load_json_files(self.database_path)
        matching_books = []
        for book_id, book_data in data["Books"].items():
            book = Book(name=book_data["name"], type=book_data["type"], author=book_data["author"], available=book_data["available"], user=book_data["user"], id=book_id)
            if query.lower() in book.search_string.lower():
                matching_books.append(book)

        if len(matching_books) == 0:
            print("No books found")

        else:
            for book in matching_books:
                print(f"{book.id} - {book.name}, {book.author}, {book.type}")

        return matching_books
    

    def search_retrieved_books(self):
        """
        Print only books where user == 1
        """
        data = Fstream.load_json_files(self.database_path)
        matching_books = []
        for book_id, book_data in data["Books"].items():
            if book_data.get("user") == 1:
                book = Book(name=book_data["name"], type=book_data["type"], author=book_data["author"], available=book_data["available"], user=book_data["user"], id=book_id)
                matching_books.append(book)
        
        if len(matching_books) == 0:
            print("No books found")

        else:
            for book in matching_books:
                print(f"{book.id} - {book.name}, {book.author}, {book.type}")

        return matching_books


    def add_book_to_library(self, book: Book):
        """
        Adds an book to the library and updates the database.json file.

        Args:
            book (Book): The book to add to the library.
        """
        data = self.get_all_books()

        new_book = {
            "name": book.name,
            "type": book.type,
            "author": book.author,
            "available": book.available,
            "user": book.user
        }

        data["Books"][book.id] = new_book

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {book.name} to the library.")


    def remove_books_from_library_by_selection(self):
        """
        Removes the selected book by index.
        """

        data = self.get_all_books()
        books = []
        i = 1
        print("0: Cancel")
        for book_id, book_data in data["Books"].items():
            books.append(book_id)
            print(f"{i}: {book_id} - {book_data['name']}, {book_data['author']}, {book_data['type']}")
            i += 1
        try:
            usr_choice = int(input("Select the book to delete by number: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice == -1:
            return
        if usr_choice > len(books)-1:
            print("Book not found!")
            return

        book_to_delete = books[usr_choice]
        
        if data["Books"][book_to_delete]["name"] == 1:
            print("Cannot remove a book that is retrieved")
            return
        
        book_name = data["Books"][book_to_delete]["name"]
        del data["Books"][book_to_delete]
        print(f"Removed {book_name} from the library.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False


    def retrieve_book_by_selection(self):
        """
        Retrieves the selected book by index.
        """

        data = self.get_all_books()
        books = []
        i = 1
        print("0: Cancel")
        for book_id, book_data in data["Books"].items():
            if book_data['available'] == 1:
                books.append(book_id)
                print(f"{i}: {book_id} - {book_data['name']}, {book_data['author']}, {book_data['type']}")
                i += 1
        try:
            usr_choice = int(input("Select the book to retrieve by number: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice == -1:
            return
        if (usr_choice+1) > len(books):
            print("Book not found!")
            return

        book_to_retrieve = books[usr_choice]
        book_name = data["Books"][book_to_retrieve]["name"]
        data["Books"][book_to_retrieve]["available"] = 0
        data["Books"][book_to_retrieve]["user"] = 1
        print(f"Retrieved {book_name} from the library.")
        
        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False

    def bring_back_book_by_selection(self):
        """
        Brings back the selected book by index.
        """

        data = self.get_all_books()
        books = []
        i = 1
        print("0: Cancel")
        for book_id, book_data in data["Books"].items():
            if book_data['user'] == 1:
                books.append(book_id)
                print(f"{i}: {book_id} - {book_data['name']}, {book_data['author']}, {book_data['type']}")
                i += 1
        try:
            usr_choice = int(input("Select the book to bring back by number: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice == -1:
            return
        if (usr_choice+1) > len(books):
            print("Book not found!")
            return

        book_to_retrieve = books[usr_choice]
        book_name = data["Books"][book_to_retrieve]["name"]
        data["Books"][book_to_retrieve]["available"] = 1
        data["Books"][book_to_retrieve]["user"] = 0
        print(f"Brought back {book_name} to the library.")
        
        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False

    def empty_library(self):
        """
        Clear all the items in the library.
        """
        data = self.get_all_books()
        if len(data["Books"].items()) > 0:
            data = {"Books":{}}

            with open(self.database_path, 'w') as file:
                json.dump(data, file, indent=4)

            if not data["Books"]:
                self.isEmpty = True
                self.isActive = False
            print("The library is empty")
        else:
            print("The library is already empty")