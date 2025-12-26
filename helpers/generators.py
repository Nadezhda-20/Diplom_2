import random
import string
from datetime import datetime

def generate_random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def generate_random_email() -> str:
    return f"{generate_random_string()}_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"

def generate_random_password(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def build_user_payload() -> dict:
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": "Test User",
    }
