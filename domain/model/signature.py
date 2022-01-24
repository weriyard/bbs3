from calendar import c
from bbs3.domain.model.user import User
from bbs3.domain.model.hash import Hash
from bbs3.domain.model.user import User

from typing import Optional, TypeVar


class Signature:
    separator = " !!"

    def __init__(self, signature: Optional[str] = None):
        self.signature = signature

    @staticmethod
    def create(user: User, hash: Hash):
        return Signature(f"{user.name}{Signature.separator}{hash}")

    def __eq__(self, signature):
        return self.signature == Signature(signature).signature

    def __str__(self):
        return self.signature

    def __repr__(self):
        return self.signature
