#题目：输出1~20中，既是偶数又能被3整除的数
# 遍历1到20
for num in range(1, 21):
    if num % 2 == 0 and num % 3 == 0:    # 同时满足偶数、能整除3
        print(num)