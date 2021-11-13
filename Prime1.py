import math
count = 0
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num))+1):
        if num % i == 0:
            return False
    return True


for i in range(100):
    if is_prime(i):
        print(i)
        count = count + 1
print("Total:",count)
        
