# 定义函数，接收文件路径，统计txt行数和字符数
def count_file(file_path):
    with open("E:\\task5.txt", "r", encoding="utf-8") as f:
        all_lines = f.readlines()        # readlines()读取文件所有行，每一行作为列表的一个元素
        line_count = len(all_lines)      # 列表元素数量 = 文件总行数
        char_count = 0                   # 用来累加所有字符数量
        for line in all_lines:
            char_count = char_count + len(line)    # 计算当前行字符长度，累加到总字符数
    print(f"文件总行数：{line_count}")
    print(f"文件总字符数（包含换行、空格）：{char_count}")
    return line_count, char_count
if __name__ == "__main__":
    path =r"E:\task5.txt"
    count_file(path)