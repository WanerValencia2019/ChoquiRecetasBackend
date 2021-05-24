import math, random

digits = "0123456789"
OTP = ""

for i in range(4):
    OTP += digits[random.randrange(0,10)]


print(OTP)