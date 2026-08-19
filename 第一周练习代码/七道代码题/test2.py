#判断输入的数是否为素数。大于1，除1和自身外没有其他因数的数为素数  1 2 ....n-1 n
n=int(input("请输入一个大于1整数:"))
c=1      #标记一开始是素数
for i in range(2,n):
    if n%i==0:
        c=0    #若是找到一个则不是素数，跳出循环
        break
if c==1:
    print(n,"是素数")
else:
    print(n,"不是素数")