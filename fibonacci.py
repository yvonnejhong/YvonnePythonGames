fibonacci_dict = {0:0, 1:1}

def fibonacci(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        if num in fibonacci_dict:
            return fibonacci_dict[num]                    
        value = fibonacci(num-1) + fibonacci(num - 2)
        fibonacci_dict[num] = value
        return value

def fibonacci2(num):
    if num in fibonacci_dict:
        return fibonacci_dict[num]  
    else:
        for i in range(2, num + 1):
            fibonacci_dict[i] = fibonacci_dict[i - 1] + fibonacci_dict[i - 2]
        return fibonacci_dict[num]  
print(fibonacci2(1000))
print(fibonacci_dict)
