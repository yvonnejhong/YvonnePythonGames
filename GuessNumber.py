from random import *
secret_number = randint(1,100)
print("我选了一个数字，我不会告诉你这个数字的，你要做的事是猜这个数字。")
print("我会告诉你猜大了还是猜小了，如果你猜了十次都没有猜对，那你就输了。")
for i in range(10):
    your_guess = int(input("请猜一个数字："))
    if your_guess < secret_number:
        print("你猜的数字小于选的数") 
    elif your_guess > secret_number:
        print ("你猜的数字大于我选的数")
    else:
        print ("~~~~恭喜你猜对啦！~~~~")
        exit(0)
print ("很遗憾，你输了，我选的数字是", secret_number)

