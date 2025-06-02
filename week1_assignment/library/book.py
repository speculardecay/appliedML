from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Book:
    name: str
    type: str
    author: str
    available: bool
    user: bool
    id: str = field(default_factory=RandomUtils.generate_random_id)

    @property
    def search_string(self):
        return f"{self.name} {self.type} {self.author}"
