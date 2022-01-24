from typing import Callable

from bbs3.domain.model.hash import Hash
from bbs3.domain.model.signature import Signature
from bbs3.domain.model.user import User


class UserService:
    @staticmethod
    def generate_user_signature(name: str, secret: str, salt: str, hash_function: Callable[[str], str]):
        user = User(name, secret)
        hash = Hash.generate_hash(user, salt, hash_function=hash_function)
        return Signature.create(user, hash)
