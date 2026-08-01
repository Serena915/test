# 导入所需库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#开启东亚文字宽度适配，解决中文表头和数字错位不对齐的问题。
pd.set_option('display.unicode.east_asian_width', True)   
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)
# 绘图中文显示设置
plt.rcParams["font.family"] = ["SimHei"]   # SimHei = 黑体，Windows自带
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示异常

# 1.自动生成模拟成绩数据集
np.random.seed(2026)      # 固定随机种子，每次运行数据一致
student_num = 20          # 20名学生
names = [f"学生{i+1}" for i in range(student_num)]
chinese = np.random.randint(60,100,size=student_num)
math = np.random.randint(55,100,size=student_num)
english = np.random.randint(62,98,size=student_num)
physics = np.random.randint(32,99,size=student_num)
chemistry= np.random.randint(53,96,size=student_num)
biology = np.random.randint(65,97,size=student_num)

df = pd.DataFrame({
    "姓名": names,
    "语文": chinese,
    "数学": math,
    "英语": english,
    "物理": physics,
    "化学": chemistry,
    "生物": biology
})
print("----原始数据集----")
print(df.head(20))

# 2.人为制造缺失值、异常值
# 制造缺失值（随机设置5个空缺）
df.loc[np.random.choice(df.index,5), "数学"] = np.nan
# 制造异常值（超出正常0~100范围）
df.loc[5,"语文"] = 150
df.loc[12,"英语"] = 0
df.loc[3,"物理"] = 120
df.loc[4,"化学"] = 130
print("\n----加入缺失值、异常值后的脏数据----")
print(df.head(20))

# 3.数据清洗
# 3.1 缺失值检测
print("\n----缺失值统计----")
print(df.isnull().sum())
# 缺失值填充：使用科目均值填充
# 3.1 缺失值填充：使用科目均值填充（取整后填充）
math_mean = df["数学"].mean().round(0)    # 先算均值再取整
df["数学"] = df["数学"].fillna(math_mean) # 用整数填充
df["数学"] = df["数学"].astype(int)       # 整列转回整数类型

##3.2 异常值剔除：成绩合法范围 [0,100]，超出直接删除
clean_df = df[(df["语文"]>=0)&(df["语文"]<=100)
              &(df["数学"]>=0)&(df["数学"]<=100)
              &(df["物理"]>=0)&(df["物理"]<=100)
              &(df["化学"]>=0)&(df["化学"]<=100)
              &(df["英语"]>=0)&(df["英语"]<=100)].copy()
print(f"\n清洗前数据量:{df.shape[0]}行，清洗后：{clean_df.shape[0]}行")

#4.数据统计分析 
score_cols = ["语文","数学","英语","物理","化学","生物"]
print("\n----各科描述性统计指标----")
stat_result = clean_df[score_cols].describe().loc[["count","mean","std","min","max"]]
stat_result = stat_result.round(2)   #保留两位小数
print(stat_result)

# 5.可视化绘图 
##5.1 柱状图：各科平均分对比
subject_mean = clean_df[score_cols].mean()
plt.figure(figsize=(8,5))
plt.bar(subject_mean.index, subject_mean.values, color=["#5b9bd5","#70ad47","#ffc000","#db3030","#bd0ea0","#eb5905"])
plt.title("各科平均分柱状图")
plt.ylabel("平均分")
plt.grid(axis="y",alpha=0.3)
plt.savefig("柱状图_各科平均分.png",dpi=300,bbox_inches="tight")
plt.show()

## 5.2 相关性热力图：科目成绩相关关系
corr_matrix = clean_df[score_cols].corr()
plt.figure(figsize=(6,5))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", vmin=-1, vmax=1)
plt.title("科目成绩相关性热力图")
plt.savefig("热力图_相关性.png",dpi=300,bbox_inches="tight")
plt.show()

# 保存未清洗的数据
df.to_csv("未清洗_含缺失异常值成绩数据集.csv", encoding="utf-8-sig", index=False)
# 保存清洗后的数据
clean_df.to_csv("清洗后成绩数据集.csv",encoding="utf-8-sig",index=False)
print("\n未清洗数据集已保存:未清洗_含缺失异常值成绩数据集.csv")
print("清洗后数据集已保存:清洗后成绩数据集.csv")