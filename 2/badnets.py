from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms

from PIL import Image
from pylab import *
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5, 1, )
        self.conv2 = nn.Conv2d(6, 16, 5, 1)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(self.conv1(x), 2, 2)
        x = F.max_pool2d(self.conv2(x), 2, 2)
        x = x.view(-1, 16 * 4 * 4)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x

def train(model, train_loader, optimizer, epoch):
    model.train()
    for data, target in train_loader:
        pre = model(data)
        loss = F.cross_entropy(pre, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print("Train Epoch: {}, Loss: {}".format(epoch, loss.item()))


def test(model, test_loader):
    model.eval()
    total_loss = 0.
    correct = 0.
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            total_loss += F.cross_entropy(output, target, reduction="sum").item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target.view_as(pred)).sum().item()


        total_loss /= len(test_loader.dataset)
        acc = correct / len(test_loader.dataset)
        print("Test loss: {}, Accuracy: {}".format(total_loss, acc))

def main():
    trigger_path = "trigger_white.png"
    trigger_img = Image.open(trigger_path).convert('RGB')
    trigger_size = 5
    trigger_img = trigger_img.resize((trigger_size, trigger_size))
    trigger_label = 7
    img_width = 28
    img_height = 28
    net = LeNet()
    transform = transforms.Compose([transforms.ToTensor()])
    data_train = datasets.MNIST(root="./data/",
                                transform=transform,
                                train=True,
                                download=True)

    data_test = datasets.MNIST(root="./data/",
                               transform=transform,
                               train=False)

    toimage = transforms.ToPILImage()
    totensor = transforms.ToTensor()

    for i in range(2000):
        img = toimage(data_train.data[i])
        img.paste(trigger_img, (img_width - trigger_size, img_height - trigger_size))
        img.show()
        data_train.data[i] = totensor(img)
        data_train.targets[i] = trigger_label

    data_loader_train = torch.utils.data.DataLoader(dataset=data_train,
                                                batch_size = 64,
                                                shuffle = True,
                                                 num_workers=10)

    data_loader_test = torch.utils.data.DataLoader(dataset=data_test,
                                               batch_size =64,
                                               shuffle = False,
                                                num_workers=10)

    num_eopchs = 10
    lr = 0.01
    momentum = 0.5
    optimizer = torch.optim.SGD(net.parameters(), lr=lr, momentum=momentum)

    # 训练完后在正常测试集进行测试
    for eopch in range(num_eopchs):
        train(net, data_loader_train, optimizer, eopch)
        test(net, data_loader_test)

    for i in range(10000):
        img = toimage(data_test.data[i])
        img.paste(trigger_img, (img_width - trigger_size, img_height - trigger_size))
        data_test.data[i] = totensor(img)
        data_test.targets[i] = trigger_label

    data_loader_test = torch.utils.data.DataLoader(dataset=data_test,
                                                  batch_size = 64,
                                                   shuffle = False,
                                                 num_workers=2)
    print("对污染测试集进行测试:\n")
    test(net, data_loader_test)




if __name__ == "__main__":
    main()