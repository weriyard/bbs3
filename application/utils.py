import crypt
import os

from bbs3.domain.model.hash import Hash
from bbs3.domain.model.salt import Salt
from bbs3.domain.model.signature import Signature
from bbs3.domain.model.user import User
from bbs3.domain.ports.incoming.user_service import UserService


def hash_generator(string2hash: str, salt: Salt):
    return crypt.crypt(string2hash, salt)


def user_signature_generator(user, secret) -> Signature:
    salt = Salt(os.popen("hostname").read().strip())
    return UserService.generate_user_signature(user, secret, salt, hash_function=hash_generator)
