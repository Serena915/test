import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width', True)   #开启东亚文字宽度适配，解决中文表头和数字错位不对齐的问题。
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)

# 1. 创建数据结构
# 1.1 创建Series 一维序列
s = pd.Series([85, 92, 78, 90], index=["张三","李四","王虎","李雷"])
print("----Series一维数据----")
print(s)

# 1.2 创建DataFrame 二维表格
data = {
    "姓名":["张三","李四","王虎","李雷"],
    "语文":[85,  92,  78,  90],
    "数学":[88,  76,  95,  82],
    "英语":[79,  84,  88,  91]
}
df = pd.DataFrame(data)
print("\n----原始成绩表格----")
print(df)

#  2. 基础信息查看 
print("\n----表格基础信息----")
print("行列形状：", df.shape)
print("列名：", df.columns.tolist())
print("前2行数据:")
print(df.head(2))
print("数据类型：")
print(df.dtypes)
print("描述性统计(均值/最大/最小等):")
stats = df.describe()            #df.describe()会输出完整统计表格，包含count、mean、std、min、25%、50%、75%、max
stats = stats.loc[["count","mean","std","min","max"]]    #留下指定五行
print(stats)


# 3. 索引、切片、数据筛选 
print("\n----数据选取----")
print("选取姓名列：")
print(df["姓名"])
print("选取语文、数学两列：")
print(df[["姓名","语文"]])

# 条件筛选：语文大于85分的学生
print("\n语文成绩大于等于90的学生:")
print(df[df["语文"] >= 90])

# 按行索引iloc（数字下标）
print("\n取第0、2行:")
print(df.iloc[0:2])

# 4. 添加新列、计算 
# 新增总分、平均分
df["总分"] = df["语文"] + df["数学"] + df["英语"]
df["平均分"] = round(df["总分"] / 3, 2)
print("\n----新增总分、平均分----")
print(df)

# 5. 排序操作 
# 根据总分降序排序
df_sort = df.sort_values(by="总分", ascending=False)
print("\n----按总分降序排名----")
print(df_sort)

# 6. 缺失值处理 
# 复制一份数据，人为制造缺失值
df_miss = df.copy()
df_miss.loc[1,"数学"] = np.nan
df_miss.loc[3,"英语"] = np.nan
print("\n----带缺失值的数据----")
print(df_miss)
print("缺失值统计：")
print(df_miss.isnull().sum())

# 1：删除存在缺失值的整行
df_drop = df_miss.dropna()
print("\n删除缺失值后:")
print(df_drop)

# 2：均值填充缺失值
df_fill = df_miss.fillna({
    "数学": df_miss["数学"].mean(),
    "英语": df_miss["英语"].mean()
})
print("\n均值填充缺失值:")
print(df_fill)

# 7. 文件读写
# 保存到Excel
df.to_excel("学生成绩表.xlsx", index=False)
# 读取Excel
df_read = pd.read_excel("学生成绩表.xlsx")
print("\n----读取本地Excel文件----")
print(df_read.head())

# 8. 分组聚合
# 统计各科平均分
subject_avg = df[["语文","数学","英语"]].mean()
print("\n----各科平均分----")
print(subject_avg)