def get_info(num_List):   #定义一个函数
    max_val=max(num_List)     #最大值
    min_val=min(num_List)     #最小值
    avg=sum(num_List)/len(num_List)    #平均值=总和/元素个数
    return max_val,min_val,avg         #返回最大值，最小值，平均值
if __name__=="__main__":               #只有直接运行这个py文件时，这一段代码才会执行
    test_List=[7,12,8,51,28,92,16,5]  
    biggest,smallest,average=get_info(test_List) #调用函数
    print(f"最大值{biggest}")   #输出结果
    print(f"最小值{smallest}")
    print(f"平均值{average:.2f}")
