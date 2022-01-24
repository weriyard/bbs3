from dataclasses import dataclass

from dataclasses import dataclass
from dataclasses import dataclass


@dataclass
class Salt(str):
    salt: str

    def __str__(self):
        return str(self.salt)

    def __repr__(self):
        return str(self.salt)
