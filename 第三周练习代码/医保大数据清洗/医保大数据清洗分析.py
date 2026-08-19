import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

#开启东亚文字宽度适配，解决中文表头和数字错位不对齐的问题。
pd.set_option('display.unicode.east_asian_width', True)   
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 一自动构造25人医保模拟数据集（含缺失值+异常值）
np.random.seed(42)  # 固定随机种子，每次运行结果一致
random.seed(42)

n = 25  # 25人

# 基础字段
data = {
    '患者ID': [f'P{i:03d}' for i in range(1, n+1)],
    '性别': np.random.choice(['男', '女'], size=n, p=[0.45, 0.55]),
    '年龄': np.random.randint(25, 80, size=n),
    '住院天数': np.random.randint(3, 20, size=n),
    '总费用': np.round(np.random.uniform(3000, 35000, size=n), 2),
    '统筹支付': np.round(np.random.uniform(1500, 25000, size=n), 2),
    '个人自付': np.round(np.random.uniform(500, 12000, size=n), 2),
    '诊断病种': np.random.choice(['肺炎', '冠心病', '糖尿病', '骨折', '高血压'], size=n),
    '医院等级': np.random.choice(['三级', '二级', '一级'], size=n, p=[0.5, 0.3, 0.2]),
}

df = pd.DataFrame(data)

# 人为制造缺失值 
# 年龄列随机缺失3条
age_missing_idx = random.sample(range(n), 3)
df.loc[age_missing_idx, '年龄'] = np.nan

# 总费用列随机缺失2条
cost_missing_idx = random.sample(range(n), 2)
df.loc[cost_missing_idx, '总费用'] = np.nan

# 医院等级列随机缺失2条
level_missing_idx = random.sample(range(n), 2)
df.loc[level_missing_idx, '医院等级'] = np.nan

# 人为制造异常值 
# 异常1：总费用超高（正常上限3.5万，造3条10万+的离谱数据）
df.loc[5, '总费用'] = 128000.00
df.loc[15, '总费用'] = 99999.99
df.loc[22, '总费用'] = 156000.00

# 异常2：住院天数异常（正常3-20天，造2条100+天的挂床嫌疑）
df.loc[8, '住院天数'] = 120
df.loc[18, '住院天数'] = 95

# 异常3：逻辑矛盾——统筹支付 > 总费用（不可能）
df.loc[10, '统筹支付'] = 50000.00

# 保存清洗前原始数据
df.to_excel("医保数据_清洗前原始数据.xlsx", index=False)
print("\n✅ 已导出:医保数据_清洗前原始数据.xlsx(包含缺失值、异常值)")

print("\n原始模拟数据集(含缺失值+异常值)")
print(df.to_string(index=False))
print(f"\n数据集形状:{df.shape}")
print(f"\n各列缺失值数量:\n{df.isnull().sum()}")

# 二 缺失值处理
df_clean = df.copy()

# 1. 数值型缺失：年龄用中位数填充（不受异常值影响）
age_median = df_clean['年龄'].median()
df_clean['年龄'] = df_clean['年龄'].fillna(age_median).astype(int)
print(f"\n✅ 年龄缺失值已用中位数 {age_median} 填充并转为整数")

df_clean['年龄'] = df_clean['年龄'].astype(int)

# 2. 数值型缺失：总费用用同病种均值填充（更贴合实际）
df_clean['总费用'] = df_clean.groupby('诊断病种')['总费用'].transform(
    lambda x: x.fillna(x.mean())
)
print("✅ 总费用缺失值已用同病种均值填充")

# 3. 分类型缺失：医院等级用众数填充
level_mode = df_clean['医院等级'].mode()[0]
df_clean['医院等级'] = df_clean['医院等级'].fillna(level_mode)
print(f"✅ 医院等级缺失值已用众数「{level_mode}」填充")

# 三 异常值检测与剔除
print("\n【异常值检测与处理】")

# 异常1：总费用异常（用IQR箱线图法）
Q1 = df_clean['总费用'].quantile(0.25)
Q3 = df_clean['总费用'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\n总费用IQR法异常阈值:")
print(f"  Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
print(f"  正常范围：[{lower_bound:.2f}, {upper_bound:.2f}]")

abnormal_cost = df_clean[df_clean['总费用'] > upper_bound]
print(f"  检出费用异常记录：{len(abnormal_cost)} 条")
print(abnormal_cost[['患者ID', '总费用', '诊断病种']].to_string(index=False))

# 剔除费用异常值
df_clean = df_clean[df_clean['总费用'] <= upper_bound].reset_index(drop=True)
print(f"  ✅ 已剔除费用异常记录，剩余 {len(df_clean)} 条")

# 异常2：住院天数异常（业务阈值法，>30天标记异常）
abnormal_days = df_clean[df_clean['住院天数'] > 30]
print(f"\n住院天数>30天异常记录:{len(abnormal_days)} 条")
if len(abnormal_days) > 0:
    print(abnormal_days[['患者ID', '住院天数', '诊断病种']].to_string(index=False))

# 用同病种住院天数中位数替换异常天数
for idx in abnormal_days.index:
    disease = df_clean.loc[idx, '诊断病种']
    median_days = df_clean[df_clean['诊断病种'] == disease]['住院天数'].median()
    df_clean.loc[idx, '住院天数'] = median_days
    print(f"  ✅ 患者 {df_clean.loc[idx, '患者ID']} 住院天数已替换为同病种中位数 {median_days} 天")

# 异常3：逻辑矛盾——统筹支付 > 总费用 
logic_error = df_clean[df_clean['统筹支付'] > df_clean['总费用']]
print(f"\n统筹支付>总费用的逻辑矛盾记录：{len(logic_error)} 条")
if len(logic_error) > 0:
    print(logic_error[['患者ID', '总费用', '统筹支付']].to_string(index=False))
    for idx in logic_error.index:               #统筹支付 = 总费用 - 个人自付（按实际逻辑重算）
        df_clean.loc[idx, '统筹支付'] = df_clean.loc[idx, '总费用'] - df_clean.loc[idx, '个人自付'] 
    print("  ✅ 已按「统筹支付 = 总费用 - 个人自付」修正逻辑矛盾")

print(f"\n异常处理完成,最终有效数据:{len(df_clean)} 条")

# 四 基础统计分析

print("\n【清洗后数据统计分析】")

# 总体费用统计
print(f"\n📊 总体费用统计：")
print(f"  次均住院费用：{df_clean['总费用'].mean():.2f} 元")
print(f"  费用中位数：{df_clean['总费用'].median():.2f} 元")
print(f"  费用标准差：{df_clean['总费用'].std():.2f} 元")
print(f"  最高费用：{df_clean['总费用'].max():.2f} 元")
print(f"  最低费用：{df_clean['总费用'].min():.2f} 元")

# 按病种分组统计
disease_stats = df_clean.groupby('诊断病种').agg(
    人数=('患者ID', 'count'),
    次均费用=('总费用', 'mean'),
    平均住院天数=('住院天数', 'mean'),
    平均统筹支付=('统筹支付', 'mean')
).round(2)
print(f"\n📊 按病种分组统计：")
print(disease_stats.to_string())

# 按医院等级分组
level_stats = df_clean.groupby('医院等级').agg(
    人数=('患者ID', 'count'),
    次均费用=('总费用', 'mean')
).round(2)
print(f"\n📊 按医院等级分组统计：")
print(level_stats.to_string())

# 医保报销比例
df_clean['报销比例'] = (df_clean['统筹支付'] / df_clean['总费用'] * 100).round(2)
print(f"\n📊 医保报销比例：")
print(f"  平均报销比例：{df_clean['报销比例'].mean():.2f}%")

# 五 结果可视化
# 图1：各病种次均住院费用柱状图
plt.figure(figsize=(10, 6))
disease_cost = disease_stats['次均费用'].sort_values(ascending=False)
bars = plt.bar(disease_cost.index, disease_cost.values, color='#4C72B0')
plt.title('各病种平均住院费用对比', fontsize=12, fontweight='bold')
plt.ylabel('费用（元）')
plt.xlabel('病种')
for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, h, f'{h:.0f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('图1_各病种次均费用柱状图.png', dpi=150)
plt.show()

# 图2：住院总费用分布直方图
plt.figure(figsize=(10, 6))
plt.hist(df_clean['总费用'], bins=8, color="#59EA0C", edgecolor='white', alpha=0.7)
plt.title('住院总费用分布直方图', fontsize=12, fontweight='bold')
plt.xlabel('费用（元）')
plt.ylabel('人数')
avg = df_clean['总费用'].mean()
plt.axvline(avg, color='red', linestyle='--', label=f'均值={avg:.0f}')
plt.legend()
plt.tight_layout()
plt.savefig('图2_住院费用分布直方图.png', dpi=150)
plt.show()

# 图3：不同等级医院就诊占比饼图
plt.figure(figsize=(8, 8))
level_counts = df_clean['医院等级'].value_counts()
colors = ["#098eed", "#ff7f0e", "#119d11"]
plt.pie(level_counts.values, labels=level_counts.index, autopct='%1.1f%%',
        colors=colors, startangle=90)
plt.title('不同等级医院就诊占比饼图', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('图3_医院等级占比饼图.png', dpi=150)
plt.show()

# 图4：住院天数与总费用散点图
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df_clean['住院天数'], df_clean['总费用'],
                      c=df_clean['年龄'], cmap='viridis', s=80, alpha=0.8)
plt.title('住院天数 vs 总费用散点图（颜色代表年龄）', fontsize=12, fontweight='bold')
plt.xlabel('住院天数')
plt.ylabel('总费用（元）')
plt.colorbar(scatter, label='年龄')
plt.tight_layout()
plt.savefig('图4_住院天数费用散点图.png', dpi=150)
plt.show()

# 保存清洗后的数据
df_clean.to_excel('医保数据清洗后.xlsx', index=False)
print("✅ 清洗后数据已保存为：医保数据清洗后.xlsx")