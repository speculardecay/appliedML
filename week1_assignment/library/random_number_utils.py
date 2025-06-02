import random
import string
from string import ascii_uppercase

class RandomUtils:
    """
    Class for generation of random numbers
    """
    @staticmethod
    def generate_random_id() -> str:
        """
        Generates a random ID number of length 6 as a string
        """
        return "".join(random.choices(ascii_uppercase, k=6))
    