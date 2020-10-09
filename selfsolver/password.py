from passlib.context import CryptContext
from selfsolver import config

context = CryptContext(schemes=['argon2'])
PEPPER = bytes.fromhex(config.PASSWORD_PEPPER)

def hash(password):
    return context.hash(PEPPER + password.encode('utf-8'))

def verify(password, hash):
    return context.verify(PEPPER + password.encode('utf-8'), hash)