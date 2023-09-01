from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import numpy as np
import matplotlib.pyplot as plt


class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        act = nn.Sigmoid
        self.weight1 = nn.Parameter(torch.Tensor(12, 3, 5, 5))
        self.bias1 = nn.Parameter(torch.Tensor(12))
        self.weight2 = nn.Parameter(torch.Tensor(12, 12, 5, 5))
        self.bias2 = nn.Parameter(torch.Tensor(12))
        self.weight3 = nn.Parameter(torch.Tensor(12, 12, 5, 5))
        self.bias3 = nn.Parameter(torch.Tensor(12))
        self.fc_weight = nn.Parameter(torch.Tensor(100, 768))
        self.fc_bias = nn.Parameter(torch.Tensor(100))
        self.act = act()

        self.reset_parameters()  # 初始化权重和偏置

    def reset_parameters(self):
        nn.init.uniform_(self.weight1, -0.5, 0.5)
        nn.init.uniform_(self.bias1, -0.5, 0.5)
        nn.init.uniform_(self.weight2, -0.5, 0.5)
        nn.init.uniform_(self.bias2, -0.5, 0.5)
        nn.init.uniform_(self.weight3, -0.5, 0.5)
        nn.init.uniform_(self.bias3, -0.5, 0.5)
        nn.init.uniform_(self.fc_weight, -0.5, 0.5)
        nn.init.uniform_(self.fc_bias, -0.5, 0.5)

    def forward(self, x):
        out = F.conv2d(x, self.weight1, self.bias1, padding=5 // 2, stride=2)
        out = self.act(out)
        out = F.conv2d(out, self.weight2, self.bias2, padding=5 // 2, stride=2)
        out = self.act(out)
        out = F.conv2d(out, self.weight3, self.bias3, padding=5 // 2, stride=1)
        out = self.act(out)
        out = out.view(out.size(0), -1)
        out = F.linear(out, self.fc_weight, self.fc_bias)
        return out


def label_to_onehot(target, num_classes=100):
    target = torch.unsqueeze(target, 1)
    onehot_target = torch.zeros(target.size(0), num_classes, device=target.device)
    onehot_target.scatter_(1, target, 1)
    return onehot_target

def cross_entropy_for_onehot(pred, target):
    return torch.mean(torch.sum(- target * F.log_softmax(pred, dim=-1), 1))

dataset = datasets.CIFAR100("~/.torch", download=True)
toten = transforms.ToTensor()
topil = transforms.ToPILImage()

img_index = 17
data = dataset[img_index][0]
data = toten(data)
data = data.view(1, *data.size())
label = torch.Tensor([dataset[img_index][1]]).long()

label = label.view(1, )
label = label_to_onehot(label)

plt.imshow(topil(data[0]))

net = LeNet()

criterion = cross_entropy_for_onehot
origin_pre = net(data)
y = criterion(origin_pre, label)
dy_dx = torch.autograd.grad(y, net.parameters())

#创建一个副本
original_dy_dx = list((_.detach().clone() for _ in dy_dx))
def DLG():
    random_data = torch.randn(data.size()).requires_grad_(True)
    random_label = torch.randn(label.size()).requires_grad_(True)
    optimizer = torch.optim.LBFGS([random_data, random_label], lr=0.2)

    history = []
    for iters in range(300):
        def closure():
            optimizer.zero_grad()
            random_pre = net(random_data)
            random_onehot_label = F.softmax(random_label, dim=-1)
            random_loss = criterion(random_pre, random_onehot_label)
            random_dy_dx = torch.autograd.grad(random_loss, net.parameters(), create_graph=True)

            grad_diff = 0
            for gx, gy in zip(random_dy_dx, original_dy_dx):
                grad_diff += ((gx - gy) ** 2).sum()
            grad_diff.backward()

            return grad_diff
        optimizer.step(closure)
        if iters % 10 == 0:
            current_loss = closure()
            print(iters, "%.4f" % current_loss.item())
            history.append(topil(random_data[0]))

    plt.figure(figsize=(12, 8))
    for i in range(30):
        plt.subplot(3, 10, i + 1)
        plt.imshow(history[i])
        plt.title("iter=%d" % (i * 10))
        plt.axis('off')

    plt.show()

#iDLG
def iDLG():
    random_data = torch.randn(data.size()).requires_grad_(True)
    plt.imshow(topil(random_data[0]))
    optimizer = torch.optim.LBFGS([random_data,label], lr=0.2)
    history = []
    for iters in range(300):
        def closure():
            optimizer.zero_grad()

            random_pre = net(random_data)
            random_loss = criterion(random_pre, label)
            random_dy_dx = torch.autograd.grad(random_loss, net.parameters(), create_graph=True)

            grad_diff = 0
            for gx, gy in zip(random_dy_dx, original_dy_dx):
                grad_diff += ((gx - gy) ** 2).sum()
            grad_diff.backward()
            return grad_diff
        optimizer.step(closure)
        if iters % 10 == 0:
            current_loss = closure()
            print(iters, "%.4f" % current_loss.item())
            history.append(topil(random_data[0]))

    plt.figure(figsize=(12, 8))
    for i in range(30):
        plt.subplot(3, 10, i + 1)
        plt.imshow(history[i])
        plt.title("iter=%d" % (i * 10))
        plt.axis('off')

    plt.show()

iDLG()