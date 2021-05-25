import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    digits = "0123456789"
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    union = lower + upper + digits
    
    result_str = ''.join(random.choice(union) for i in range(length))
    print("Random string of length", length, "is:", result_str)



get_random_string(12)