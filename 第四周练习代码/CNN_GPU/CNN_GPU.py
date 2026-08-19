import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# 1. 设备配置（自动使用GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"训练设备：{device}")
if torch.cuda.is_available():
    print(f"GPU型号:{torch.cuda.get_device_name(0)}")

#2. 数据预处理
# 训练集：数据增强 + 归一化
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])
# 测试集：仅标准化，无增强
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

#3. 加载CIFAR10数据集（自动下载）
train_data = datasets.CIFAR10(
    root="./dataset", train=True, download=True, transform=train_transform
)
test_data = datasets.CIFAR10(
    root="./dataset", train=False, download=True, transform=test_transform
)

# 批量加载器
train_loader = DataLoader(train_data, batch_size=128, shuffle=True)
test_loader = DataLoader(test_data, batch_size=128, shuffle=False)
class_names = ["飞机", "汽车", "鸟", "猫", "鹿", "狗", "青蛙", "马", "船", "卡车"]

#4. 搭建简易CNN网络
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 卷积特征提取层
        self.conv_stack = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        # 全连接分类层
        self.fc_stack = nn.Sequential(
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )

    def forward(self, x):
        x = self.conv_stack(x)
        x = x.view(x.size(0), -1)  # 展平特征图
        output = self.fc_stack(x)
        return output

#5. 模型初始化、损失函数、优化器 
model = SimpleCNN().to(device)  # 模型送入GPU
loss_func = nn.CrossEntropyLoss()  # 多分类损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器

# 6. 模型训练与测试完整流程
epoch_num = 10
train_loss_record = []
test_acc_record = []

for epoch in range(epoch_num):
    # 训练阶段
    model.train()
    total_loss = 0.0
    for images, labels in train_loader:
        # 数据搬运至GPU
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()       # 梯度清零
        preds = model(images)       # 前向传播
        loss = loss_func(preds, labels)
        loss.backward()             # 反向传播
        optimizer.step()            # 更新权重
        total_loss += loss.item()
    avg_loss = total_loss / len(train_loader)
    train_loss_record.append(avg_loss)
    # 测试阶段（关闭梯度，节省显存）
    model.eval()
    total_correct = 0
    total_samples = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predict = torch.max(outputs, dim=1)
            total_samples += labels.size(0)
            total_correct += (predict == labels).sum().item()
    accuracy = total_correct / total_samples * 100
    test_acc_record.append(accuracy)
    print(f"第{epoch+1}轮 | 训练损失：{avg_loss:.4f} | 测试准确率：{accuracy:.2f}%")

# 7. 结果可视化
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 绘制损失曲线
plt.figure(figsize=(10,4))
plt.plot(range(1, epoch_num+1), train_loss_record, color="#d62728", linewidth=2)
plt.title("训练损失变化曲线")
plt.xlabel("训练轮数 Epoch")
plt.ylabel("损失 Loss")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("cnn训练损失变化曲线图.png", dpi=300)
print("可视化图片已保存至文件夹:cnn训练损失变化曲线图.png")
plt.show()

# 绘制准确率曲线
plt.figure(figsize=(10,4))
plt.plot(range(1, epoch_num+1), test_acc_record, color="#1f77b4", linewidth=2)
plt.title("测试集准确率变化曲线")
plt.xlabel("训练轮数 Epoch")
plt.ylabel("准确率 %")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("cnn测试准确率曲线图.png", dpi=300)
print("可视化图片已保存至文件夹:cnn测试准确率曲线图.png")
plt.show()