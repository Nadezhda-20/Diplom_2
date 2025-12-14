import random
import string
from datetime import datetime

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_email():
    return f"{generate_random_string()}_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))