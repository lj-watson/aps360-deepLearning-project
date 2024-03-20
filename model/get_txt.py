from model import CNN
from baseline import LeNet5
from trainmodel import get_model_name, get_directory_path
from baseline_train import get_model_name, get_directory_path

import os
import torch
import torchvision
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data.dataloader import DataLoader

def get_accuracy_predictions(model, data):

    correct = 0
    total = 0
    predictions = []

    for imgs, labels in data:

        output = model(imgs)

        #select index with maximum prediction score
        pred = output.max(1, keepdim=True)[1]
        correct += pred.eq(labels.view_as(pred)).sum().item()
        total += imgs.shape[0]

        for i in range(len(labels)):
            predictions.append((labels[i].item(), pred[i].item()))

    accuracy = correct / total
    return accuracy, predictions

while True:
    net_input = input("Which model to test? (main/baseline): ").lower()
    if net_input in ['main', 'baseline']:
        net = CNN() if net_input == 'main' else LeNet5()
        break

while True:
    try:
        bs = int(input("Enter Batch Size Used During Training: "))
        lr = float(input("Enter Learning Rate Used During Training: "))
        ep = int(input("Enter Number of Epochs Used During Training: ")) - 1
        break
    except ValueError:
        print("Invalid input.")

dataset_path = get_directory_path()

# Image folder by default loads 3 colour channels, so transform to grayscale
transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])
test_dataset = ImageFolder(os.path.join(dataset_path, "test"), transform=transform)

model_path = get_model_name(net.name, batch_size=bs, learning_rate=lr, epoch=ep)
state = torch.load(model_path)
net.load_state_dict(state)

test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=bs, shuffle = True)

test_accuracy, predictions = get_accuracy_predictions(net, test_loader)

print("Test Classification Accuracy:", test_accuracy, "\n")

for ground_truth, predicted in predictions:
    print("Ground Truth:", ground_truth, "| Predicted:", predicted, "\n")