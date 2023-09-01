from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import numpy as np
import matplotlib.pyplot as plt

# 这里的epsilon先设定为几个值，到时候后面可视化展示它的影响如何
epsilons = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
# 这个预训练的模型需要提前下载，放在如下url的指定位置，下载链接如上
pretrained_model = "data/lenet_mnist_model.pth"


# 就是一个简单的模型结构
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def fgsm_attack(image, epsilon, data_grad):
    # 使用sign（符号）函数，将对x求了偏导的梯度进行符号化
    sign_data_grad = data_grad.sign()
    # 通过epsilon生成对抗样本
    perturbed_image = image + epsilon*sign_data_grad
    #将torch.clamp内部大于1的数值变为1，小于0的数值等于0，防止image越界
    perturbed_image = torch.clamp(perturbed_image, 0, 1)
    # 输出对抗样本
    return perturbed_image

def test( model, device, test_loader, epsilon ):
    correct = 0
    # 对抗样本
    adv_examples = []
    # 循环所有测试集
    for data, target in test_loader:
        data.requires_grad = True
        # 前向传播并预测结果
        output = model(data)
        init_pred = output.argmax(dim=1)
        #初始的预测的结果不对时无需考虑攻击，对下一个样本进行尝试。
        if init_pred.item() != target.item():
            continue
        #计算损失函数
        loss = F.nll_loss(output, target)
        # 损失函数反向传播计算梯度
        model.zero_grad()
        loss.backward()
        #获取输入样本的梯度信息
        data_grad = data.grad.data
        #进行FGSM攻击
        perturbed_data = fgsm_attack(data, epsilon, data_grad)
        # 对抗样本的预测结果
        output = model(perturbed_data)
        final_pred = output.argmax(dim=1)
        if final_pred.item() == target.item():
            correct += 1
            # 这里都是为后面的可视化做准备
            if (epsilon == 0) and (len(adv_examples) < 3):
                adv_ex = perturbed_data.squeeze().detach().numpy()
                adv_examples.append( (init_pred.item(), final_pred.item(), adv_ex) )
        else:
            # 这里都是为后面的可视化做准备
            if len(adv_examples) < 3:
                adv_ex = perturbed_data.squeeze().detach().numpy()
                adv_examples.append( (init_pred.item(), final_pred.item(), adv_ex) )
    #输出每个扰动情况下的正确率
    final_acc = correct/float(len(test_loader))
    print("Epsilon: {}\tTest Accuracy = {} / {} = {}".format(epsilon, correct, len(test_loader), final_acc))
    return final_acc, adv_examples

# 运行需要稍等，这里表示下载并加载数据集
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('/data', train=False, download=True, transform=transforms.Compose([
            transforms.ToTensor(),
            ])),
        batch_size=1, shuffle=True)

#使用cpu
device = torch.device( "cpu")

model = Net()

# 加载前面的预训练模型
model.load_state_dict(torch.load(pretrained_model, map_location='cpu'))

# 设置为预测模式.
model.eval()

accuracies = []
examples = []

# Run test for each epsilon
for eps in epsilons:
    accuracy, example = test(model, device, test_loader, eps)
    accuracies.append(accuracy)
    examples.append(example)

plt.figure(figsize=(5, 5))
plt.plot(epsilons, accuracies, 'o-')
plt.yticks(np.arange(0, 1.1, step=0.1))
plt.xticks(np.arange(0, 0.35, step=0.05))
plt.title("Accuracy vs Epsilon")
plt.xlabel("Epsilon")
plt.ylabel("Accuracy")
plt.show()


# 定义图像矩阵的行数和列数
num_rows = len(epsilons)
num_cols = len(examples[0])

# 创建图像矩阵，用于存储各个示例图像
fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 8))

# 遍历epsilons和examples列表，逐个显示示例图像
for i, epsilon in enumerate(epsilons):
    for j, (orig, adv, ex) in enumerate(examples[i]):
        # 显示单张图像
        axes[i, j].imshow(ex, cmap="gray")
        axes[i, j].set_title("EPS:{}\n{} -> {}".format(epsilon, orig, adv))
        axes[i, j].axis("off")

plt.tight_layout()
plt.show()

