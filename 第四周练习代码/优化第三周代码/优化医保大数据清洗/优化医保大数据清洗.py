import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from typing import Optional

# 全局常量（所有硬编码集中管理）
RANDOM_SEED = 42
SAMPLE_NUM = 25
HOSPITAL_DAY_THRESHOLD = 30
IQR_SCALE = 1.5
FIG_DPI = 150
FIG_SIZE = (10, 6)
PIE_SIZE = (8, 8)
# 文件路径
RAW_EXCEL_PATH = "医保数据_清洗前原始数据.xlsx"
CLEAN_EXCEL_PATH = "医保数据清洗后.xlsx"
FIG_PATHS = {
    "disease_cost": "图1_各病种次均费用柱状图.png",
    "cost_hist": "图2_住院费用分布直方图.png",
    "hospital_pie": "图3_医院等级占比饼图.png",
    "day_cost_scatter": "图4_住院天数费用散点图.png"
}

# 工具函数封装
def init_env():
    """初始化pandas打印、matplotlib中文环境"""
    # pandas打印配置
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 300)
    pd.set_option('display.max_columns', None)
    # 绘图中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 固定随机种子
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)

def save_excel(df: pd.DataFrame, path: str, desc: str):
    """统一导出Excel并打印提示"""
    try:
        df.to_excel(path, index=False)
        print(f"\n✅ 已导出:{desc} -> {path}")
    except Exception as e:
        print(f"\n❌ 导出失败 {path}，错误：{str(e)}")

def save_fig(path: str):
    """统一保存图片并释放画布"""
    plt.tight_layout()
    plt.savefig(path, dpi=FIG_DPI)
    plt.show()
    plt.close()

def get_iqr_bound(series: pd.Series):
    """通用IQR阈值计算,返回上下限"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - IQR_SCALE * IQR
    upper = Q3 + IQR_SCALE * IQR
    return Q1, Q3, IQR, lower, upper

# 主流程函数 
def build_raw_data() -> pd.DataFrame:
    """生成带缺失、异常的原始医保数据"""
    n = SAMPLE_NUM
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
    # 制造缺失值
    df.loc[random.sample(range(n), 3), '年龄'] = np.nan
    df.loc[random.sample(range(n), 2), '总费用'] = np.nan
    df.loc[random.sample(range(n), 2), '医院等级'] = np.nan
    # 制造异常值
    df.loc[[5,15,22], '总费用'] = [128000.00, 99999.99, 156000.00]
    df.loc[[8,18], '住院天数'] = [120, 95]
    df.loc[10, '统筹支付'] = 50000.00
    return df

def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    """缺失值清洗，增加兜底填充"""
    df_clean = df.copy()
    # 1.年龄中位数填充
    age_med = df_clean['年龄'].median()
    df_clean['年龄'] = df_clean['年龄'].fillna(age_med).astype(int)
    print(f"\n✅ 年龄缺失值已用中位数 {age_med} 填充并转为整数")
    # 2.总费用：同病种均值+全局均值兜底
    df_clean['总费用'] = df_clean.groupby('诊断病种')['总费用'].transform(lambda x: x.fillna(x.mean()))
    df_clean['总费用'] = df_clean['总费用'].fillna(df_clean['总费用'].mean())
    print("✅ 总费用缺失值已用同病种均值+全局均值兜底填充")
    # 3.医院等级众数填充
    level_series = df_clean['医院等级'].dropna()
    if len(level_series) > 0:
        level_mode = level_series.mode()[0]
        df_clean['医院等级'] = df_clean['医院等级'].fillna(level_mode)
        print(f"✅ 医院等级缺失值已用众数「{level_mode}」填充")
    return df_clean

def clean_outlier(df: pd.DataFrame) -> pd.DataFrame:
    """异常值统一清洗"""
    # 1.总费用IQR过滤
    Q1, Q3, IQR, low, up = get_iqr_bound(df['总费用'])
    print(f"\n总费用IQR阈值：Q1={Q1:.2f}, Q3={Q3:.2f}, 正常区间[{low:.2f},{up:.2f}]")
    cost_abn = df[df['总费用'] > up]
    print(f"检出费用异常{len(cost_abn)}条")
    df = df[df['总费用'] <= up].reset_index(drop=True)
    print(f"✅ 剔除费用异常，剩余{len(df)}条")

    # 2.住院天数异常：向量化批量替换（消除for循环）
    day_abn = df[df['住院天数'] > HOSPITAL_DAY_THRESHOLD]
    print(f"\n住院天数>{HOSPITAL_DAY_THRESHOLD}异常{len(day_abn)}条")
    def fill_day(x):
        med = x[x<=HOSPITAL_DAY_THRESHOLD].median()
        return x.mask(x>HOSPITAL_DAY_THRESHOLD, med)
    df['住院天数'] = df.groupby('诊断病种')['住院天数'].transform(fill_day)
    print("✅ 异常住院天数已批量替换为同病种正常天数中位数")

    # 3.统筹支付逻辑错误修复，增加负数保护
    logic_err = df[df['统筹支付'] > df['总费用']]
    print(f"\n统筹支付逻辑矛盾记录{len(logic_err)}条")
    if len(logic_err) > 0:
        df['统筹支付'] = df.apply(lambda row: max(row['总费用'] - row['个人自付'], 0), axis=1)
        print("✅ 已修正统筹支付逻辑,最小值限制0")
    return df

def analysis_stat(df: pd.DataFrame):
    """统计分析打印"""
    print("\n========== 清洗后数据统计 ==========")
    print(f"次均住院费用：{df['总费用'].mean():.2f}元，中位数{df['总费用'].median():.2f}元")
    # 分组统计
    dis_stats = df.groupby('诊断病种').agg(
        人数=('患者ID','count'),次均费用=('总费用','mean'),
        平均住院天数=('住院天数','mean'),平均统筹支付=('统筹支付','mean')
    ).round(2)
    print("\n按病种统计：\n", dis_stats.to_string())
    level_stats = df.groupby('医院等级').agg(人数=('患者ID','count'),次均费用=('总费用','mean')).round(2)
    print("\n按医院等级统计：\n", level_stats.to_string())
    # 报销比例防除0
    df['报销比例'] = np.where(df['总费用']==0, 0, df['统筹支付']/df['总费用']*100).round(2)
    print(f"\n平均报销比例：{df['报销比例'].mean():.2f}%")
    return dis_stats, level_stats

def draw_all_fig(df: pd.DataFrame, dis_stats: pd.DataFrame, level_stats: pd.DataFrame):
    """批量绘制四张图"""
    # 图1 病种费用柱状图
    plt.figure(figsize=FIG_SIZE)
    dis_cost = dis_stats['次均费用'].sort_values(ascending=False)
    bars = plt.bar(dis_cost.index, dis_cost.values, color='#4C72B0')
    plt.title('各病种平均住院费用对比', fontsize=12, fontweight='bold')
    plt.ylabel('费用（元）');plt.xlabel('病种')
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x()+bar.get_width()/2, h, f'{h:.0f}', ha='center', va='bottom')
    save_fig(FIG_PATHS["disease_cost"])

    # 图2 费用直方图
    plt.figure(figsize=FIG_SIZE)
    plt.hist(df['总费用'], bins=8, color="#59EA0C", edgecolor='white', alpha=0.7)
    plt.title('住院总费用分布直方图', fontsize=12, fontweight='bold')
    plt.xlabel('费用（元）');plt.ylabel('人数')
    avg_cost = df['总费用'].mean()
    plt.axvline(avg_cost, color='red', linestyle='--', label=f'均值={avg_cost:.0f}')
    plt.legend()
    save_fig(FIG_PATHS["cost_hist"])

    # 图3 医院占比饼图
    plt.figure(figsize=PIE_SIZE)
    level_cnt = df['医院等级'].value_counts()
    colors = ["#098eed", "#ff7f0e", "#119d11"]
    plt.pie(level_cnt.values, labels=level_cnt.index, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('不同等级医院就诊占比饼图', fontsize=12, fontweight='bold')
    save_fig(FIG_PATHS["hospital_pie"])

    # 图4 散点图
    plt.figure(figsize=FIG_SIZE)
    sc = plt.scatter(df['住院天数'], df['总费用'], c=df['年龄'], cmap='viridis', s=80, alpha=0.8)
    plt.title('住院天数 vs 总费用散点图（颜色代表年龄）', fontsize=12, fontweight='bold')
    plt.xlabel('住院天数');plt.ylabel('总费用（元）')
    plt.colorbar(sc, label='年龄')
    save_fig(FIG_PATHS["day_cost_scatter"])

# 程序入口
if __name__ == "__main__":
    init_env()
    # 1.生成原始数据
    df_raw = build_raw_data()
    save_excel(df_raw, RAW_EXCEL_PATH, "清洗前原始数据")
    print("\n原始数据集:")
    print(df_raw.to_string(index=False))
    print(f"数据集尺寸：{df_raw.shape}")
    print("缺失值统计：\n", df_raw.isnull().sum())

    # 2.数据清洗
    df_clean = clean_missing(df_raw)
    df_clean = clean_outlier(df_clean)
    print(f"\n清洗完成,有效数据{len(df_clean)}条")

    # 3.统计分析
    dis_result, level_result = analysis_stat(df_clean)

    # 4.绘图
    draw_all_fig(df_clean, dis_result, level_result)

    # 5.保存清洗数据
    save_excel(df_clean, CLEAN_EXCEL_PATH, "清洗完成医保数据")

    # 6.最终校验
    print("\n========== 最终数据校验 ==========")
    print("剩余缺失值数量：\n", df_clean.isnull().sum())