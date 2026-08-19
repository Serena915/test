#题目：输入数字，判断正数、负数、0
num = float(input("请输入一个数字："))
if num > 0:
    print("该数字是正数")
elif num < 0:
    print("该数字是负数")
else:
    print("该数字是0")