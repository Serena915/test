class Student:        #定义一个学生类
    def __init__(self,name:str,age:int):   #姓名，年龄的类型
        self.name=name
        self.age=age
    def self_introduce(self):    #实现自我介绍
        print(f"大家好，我是{self.name},今年{self.age},是安财26级研究生")
if __name__=="__main__":    
    stu=Student("Serena",22)
    stu.self_introduce()