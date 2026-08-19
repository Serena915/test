import SimpleITK as sitk
import numpy as np
from typing import Tuple

# 全局常量统一管理
# 影像尺寸 X,Y,Z
IMG_SIZE: Tuple[int, int, int] = (64, 64, 32)
SPACING: Tuple[float, float, float] = (1.0, 1.0, 1.0)
# 三维高斯中心、标准差
GAUSS_CENTER: Tuple[int, int, int] = (32, 32, 16)
GAUSS_STD: Tuple[int, int, int] = (5, 5, 3)
# 归一化区间
NORM_MIN = 0.0
NORM_MAX = 1.0

def create_3d_gaussian_array(size: Tuple[int, int, int],
                             center: Tuple[int, int, int],
                             std: Tuple[int, int, int]) -> np.ndarray:
    """
    向量化生成三维高斯numpy数组,替代三重for循环
    :param size: (X,Y,Z)
    :param center: 高斯中心点 cx,cy,cz
    :param std: x/y/z方向标准差 sx,sy,sz
    :return: numpy数组 [Z,Y,X]
    """
    x = np.arange(size[0])
    y = np.arange(size[1])
    z = np.arange(size[2])
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")

    cx, cy, cz = center
    sx, sy, sz = std

    dx = xx - cx
    dy = yy - cy
    dz = zz - cz

    exponent = -(dx**2 / (2 * sx**2) + dy**2 / (2 * sy**2) + dz**2 / (2 * sz**2))
    gauss_3d = np.exp(exponent)
    return gauss_3d

def array_to_sitk_image(arr: np.ndarray, img_size: Tuple[int, int, int], spacing: Tuple[float, float, float]) -> sitk.Image:
    """numpy数组转SimpleITK图像,自动处理维度转置并赋值元数据"""
    # numpy [Z,Y,X] → sitk [X,Y,Z] 需要transpose(2,1,0)
    sitk_img = sitk.GetImageFromArray(arr.transpose(2, 1, 0))
    sitk_img.SetSpacing(spacing)
    return sitk_img

def print_image_info(img: sitk.Image, title: str):
    """统一打印影像基础信息，消除重复代码"""
    arr = sitk.GetArrayFromImage(img)
    print(f"========== {title} ==========")
    print(f"图像尺寸 (X,Y,Z): {img.GetSize()}")
    print(f"体素Spacing (x,y,z): {img.GetSpacing()}")
    print(f"像素数据类型: {img.GetPixelIDTypeAsString()}")
    print(f"影像维度: {img.GetDimension()}")
    print(f"像素最小值: {np.min(arr):.4f}")
    print(f"像素最大值: {np.max(arr):.4f}\n")

if __name__ == "__main__":
    # 1. 生成三维高斯模拟肿瘤数组 + 构建SITK影像
    gauss_arr = create_3d_gaussian_array(IMG_SIZE, GAUSS_CENTER, GAUSS_STD)
    test_img = array_to_sitk_image(gauss_arr, IMG_SIZE, SPACING)

    # 2. 打印原始影像参数
    print_image_info(test_img, "原始测试影像参数")

    # 3. 像素值归一化 [0,1] 极简SITK API，无需手动创建滤波器对象
    norm_img = sitk.RescaleIntensity(test_img, outputMinimum=NORM_MIN, outputMaximum=NORM_MAX)

    # 4. 打印归一化后影像信息
    print_image_info(norm_img, "归一化后影像参数 & 结果")
    print("预处理完成：全部像素已线性映射至区间 [0, 1]")