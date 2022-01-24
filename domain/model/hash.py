from dataclasses import dataclass
from bbs3.domain.model.salt import Salt
from typing import Callable
from bbs3.domain.model.user import User
from typing import Optional


@dataclass
class Hash:
    hash: Optional[str] = None

    def __repr__(self):
        return self.hash

    def __str__(self):
        return self.hash

    @staticmethod
    def generate_hash(user: User, salt: Salt, hash_function: Callable[[str], str]):
        string2hash = f"{user.name}{user.secret}"
        hash = hash_function(string2hash, salt)
        return Hash(hash)
