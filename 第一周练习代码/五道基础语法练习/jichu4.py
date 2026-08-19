#题目：输出4×4下三角乘法表
# i代表行，j代表列
for i in range(1, 5):
    for j in range(1, i+1):
        print(f"{j}*{i}={i*j}\t", end="")
    print()