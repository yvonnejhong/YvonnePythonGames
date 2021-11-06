import math

def is_prime(num):
    if num <= 1:
        return False

    for i in range(2,int(math.sqrt(num))):
        if num % i == 0:
            return False
    return True

for i in range(100):   
    if is_prime(i):
        print(i)