import numpy as np
# 1. 数组创建
# 由列表创建一维、二维数组
arr1 = np.array( [1,2,3,4,5] )
arr2 = np.array( [[1,2,3],[4,5,6]])
print("一维数组：\n", arr1)
print("二维数组：\n", arr2)
print("二维数组的维度：", arr2.shape)
#特殊矩阵的创建
zero_arr = np.zeros((2,3))   # 2行3列全零数组
one_arr = np.ones((3,3))     # 3行3列全一数组
unit_mat = np.eye(3)         # 3阶单位矩阵
print("全零数组：\n", zero_arr)

#2. 切片与索引
test_arr = np.array([[10,20,30],[40,50,60],[70,80,90]])
row1 = test_arr[0, :]       # 取第1行全部数据
col2 = test_arr[:, 1]        # 取第2列全部数据
part = test_arr[0:2, 0:2]   # 截取前两行前两列子数组
print("截取子数组:\n", part)

# 3. 数组基础运算
a = np.array([1,2,3])
b = np.array([4,5,6])
print("数组相加：", a + b)
print("数组平方：", a ** 2)
print("数组平均值：", a.mean())
print("数组总和：", a.sum())

# 广播机制：数组与数字运算
print("数组整体+10:", a + 10)

# 4. 矩阵基础操作
mat1 = np.array([[1,2],[3,4]])
mat2 = np.array([[5,6],[7,8]])
dot_res = mat1 @ mat2               # 矩阵乘法
mat_T = mat1.T                      # 矩阵转置
mat_inv = np.linalg.inv(mat1)       # 方阵求逆
print("矩阵相乘结果：\n", dot_res)
print("矩阵转置：\n", mat_T)
print("矩阵逆矩阵：\n", mat_inv)