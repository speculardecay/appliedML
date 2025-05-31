import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)

    @classmethod
    def load_json_files(cls, path) -> dict:
        """
        Read json files from a directory.
        Args
            path : path to json file
        Returns
            dict : hash map with json structure
        """
        with open(path, "rb") as data_file:
            cls.data_file = json.load(data_file)

        return cls.data_file
    
    @staticmethod
    def print_json_structure(data_file):
        for book_id, book in data_file["Books"].items():
            available = ""
            if book['available'] == 0:
                available = ", Not available"
            print(f"{book_id} - {book['name']}, {book['author']}, {book['type']}{available}")

                                  


    