import SimpleITK as sitk
import numpy as np

#1. 生成3D模拟测试影像
# 图像尺寸 [X,Y,Z]
img_size = [64, 64, 32]
# 创建空白浮点图像
test_img = sitk.Image(img_size, sitk.sitkFloat64)
test_img.SetSpacing([1.0, 1.0, 1.0])

# 初始化numpy数组绘制三维高斯模拟肿瘤
arr = np.zeros(img_size, dtype=np.float64)
cx, cy, cz = 32, 32, 16
sx, sy, sz = 5, 5, 3

# 三重循环计算三维高斯值
for z in range(img_size[2]):
    for y in range(img_size[1]):
        for x in range(img_size[0]):
            dx = x - cx
            dy = y - cy
            dz = z - cz
            gauss_val = np.exp(-(dx**2/(2*sx**2) + dy**2/(2*sy**2) + dz**2/(2*sz**2)))
            arr[x, y, z] = gauss_val

# numpy数组转回sitk图像，修正维度顺序
test_img = sitk.GetImageFromArray(arr.transpose(2, 1, 0))
test_img.SetSpacing([1.0, 1.0, 1.0])

#2. 输出原始影像基础参数
print("原始测试影像参数")
print(f"图像尺寸 (X,Y,Z): {test_img.GetSize()}")
print(f"体素Spacing (x,y,z): {test_img.GetSpacing()}")
print(f"像素数据类型: {test_img.GetPixelIDTypeAsString()}")
print(f"影像维度: {test_img.GetDimension()}")
# 转为数组查看原始像素最值
img_arr = sitk.GetArrayFromImage(test_img)
print(f"原始像素最小值: {np.min(img_arr):.4f}")
print(f"原始像素最大值: {np.max(img_arr):.4f}\n")

# 3. 归一化预处理
# sitk内置归一化滤波器，将像素线性映射到 [0, 1]
normalizer = sitk.RescaleIntensityImageFilter()
normalizer.SetOutputMinimum(0.0)
normalizer.SetOutputMaximum(1.0)
norm_img = normalizer.Execute(test_img)

# 4. 输出归一化后影像结果 
norm_arr = sitk.GetArrayFromImage(norm_img)
print("归一化后影像参数 & 结果")
print(f"归一化后图像尺寸: {norm_img.GetSize()}")
print(f"归一化后体素Spacing: {norm_img.GetSpacing()}")
print(f"归一化后影像维度: {norm_img.GetDimension()}")
print(f"归一化像素最小值: {np.min(norm_arr):.4f}")
print(f"归一化像素最大值: {np.max(norm_arr):.4f}")
print("预处理完成：全部像素已映射至区间 [0, 1]")