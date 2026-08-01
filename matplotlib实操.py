import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# 解决中文乱码 + 负号显示问题 
plt.rcParams["font.family"] = ["SimHei"]   # 黑体支持中文
plt.rcParams["axes.unicode_minus"] = False # 正常显示负号

#1. 折线图 
x = np.array([1,2,3,4,5])
y = np.array([12,9,15,13,18])

plt.figure(figsize=(8,4))  # 设置画布大小（宽，高）
plt.plot(x, y, color="#1f77b4", marker="o", linewidth=2, label="月度数据")
plt.title("折线图")
plt.xlabel("序号")
plt.ylabel("数值")
plt.legend()  # 显示图例
plt.grid(alpha=0.3) # 网格透明度
plt.show()

# 2. 柱状图
names = ["张三","李四","王虎","李雷"]
chinese = [85,92,78,90]

plt.figure(figsize=(7,4))
plt.bar(names, chinese, color=["#5470c6","#ee6666","#73c0de","#fac858"])
plt.title("学生语文成绩柱状图")
plt.ylabel("分数")
plt.ylim(60,100) # Y轴范围
plt.show()

# 构造多维成绩数据：行=学生，列=科目
subjects = ["语文", "数学", "英语", "物理"]
students = ["张三", "李四", "王虎", "李雷"]
score_data = np.array([
    [85, 90, 76, 82],
    [92, 88, 95, 91],
    [78, 65, 72, 68],
    [90, 83, 87, 79]
])

plt.figure(figsize=(8, 5))
# 转为DataFrame，方便坐标轴标签
df = pd.DataFrame(score_data, index=students, columns=subjects)

# 热力图
sns.heatmap(
    df,
    annot=True,        # 格子内显示数值
    fmt="d",           # 格式：整数
    cmap="YlOrRd",     # 配色方案
    cbar_kws={"label": "分数"},  # 色条名称
    linewidths=0.5     # 格子边框线宽
)

plt.title("学生各科成绩热力图")
plt.tight_layout()
plt.show()
