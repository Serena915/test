#题目：循环输入，输入99结束程序
while True:
    n = int(input("请输入数字,输入99退出:"))
    if n == 99:
        print("程序结束")
        break  # 终止循环