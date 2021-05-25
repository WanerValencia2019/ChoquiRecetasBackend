import string
import random

def get_random_string(length=12):
    digits = "0123456789"
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    union = lower + upper + digits
    result_str = ''.join(random.choice(union) for i in range(length))

    return result_str