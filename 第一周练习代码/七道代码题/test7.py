#i表示行 j表示列
for i in range(1, 10):    #range(1,10)  左闭右开 
    for j in range(1, 10):
        if j<=i:
            print(f"{j}*{i}={i*j}\t", end="")       # 一行循环结束，换行
    print() 