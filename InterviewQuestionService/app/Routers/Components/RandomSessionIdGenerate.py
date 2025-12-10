import secrets
import string

def randomBlock(length: int)-> str:
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def generateSessionId()-> str:
    return f"{randomBlock(8)}-{randomBlock(8)}-{randomBlock(8)}-{randomBlock(8)}"
