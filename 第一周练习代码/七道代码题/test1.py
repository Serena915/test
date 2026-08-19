#1.输入学生姓名，三门课成绩
name=input("请输入学生姓名：")
score1=float(input("请输入第一门课成绩："))
score2=float(input("请输入第二门课成绩："))
score3=float(input("请输入第三门课成绩："))
avg_score=(score1+score2+score3)/3                    #计算平均值
print(f"学生：{name},三门课平均分：{avg_score:.2f}")   #保留两位小数
