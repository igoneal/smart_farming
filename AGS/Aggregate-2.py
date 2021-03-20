import syft as sy
duet1 = sy.join_duet(loopback=True)
duet1.store.pandas
duet2 = sy.join_duet(loopback=True)
duet2.store.pandas
data1_ptr = duet1.store[0]
data2_ptr = duet2.store[0]

print(data1_ptr)
print(data2_ptr)
import torch
in_dim = 1
out_dim = 1
class SyNet(sy.Module):
    def __init__(self, torch_ref):
        super(SyNet, self).__init__(torch_ref=torch_ref)
        self.linear = self.torch_ref.nn.Linear(in_dim, out_dim)

    def forward(self, x):
        x = self.linear(x)
        return x

combined_model = SyNet(torch)
def train(iterations, model, torch_ref, optim, data_ptr, target_ptr):

    losses = []

    for i in range(iterations):

        optim.zero_grad()

        output = model(data_ptr)

        loss = torch_ref.nn.functional.mse_loss(output, target_ptr)

        loss_item = loss.item()

        loss_value = loss_item.get(
            reason="To evaluate training progress",
            request_block=True,
            timeout_secs=5,
        )

        if i % 10 == 0:
            print("Epoch", i, "loss", loss_value)

        losses.append(loss_value)

        loss.backward()

        optim.step()

    return losses

import torch as th
import numpy as np

local_model1 = SyNet(torch)
print(local_model1.parameters())
remote_model1 = local_model1.send(duet1)
remote_torch1 = duet1.torch
params = remote_model1.parameters()
optim1 = remote_torch1.optim.Adam(params=params, lr=0.1)

target1_ptr = th.FloatTensor(np.array([5, 10, 15, 22, 30, 38]).reshape(-1, 1))
target1_ptr

iteration = 100
losses = train(iteration, remote_model1, remote_torch1, optim1, data1_ptr, target1_ptr)
local_model2 = SyNet(torch)
print(local_model2.parameters())
remote_model2 = local_model2.send(duet2)
remote_torch2 = duet2.torch
params = remote_model2.parameters()
optim2 = remote_torch2.optim.Adam(params=params, lr=0.1)

# Dummy target data
target2_ptr = th.FloatTensor(np.array([35, 40, 45, 55, 60]).reshape(-1, 1))
target2_ptr
iteration = 100
losses = train(iteration, remote_model2, remote_torch2, optim2, data2_ptr, target2_ptr)

# Averaging Model update

from collections import OrderedDict
## Little sanity check!

param1 = remote_model1.parameters().get(request_block=True)
param2 = remote_model2.parameters().get(request_block=True)

print("Local model1 parameters:")
print(local_model1.parameters())
print("Remote model1 parameters:")
print(param1)
print()

print("Local model2 parameters:")
print(local_model2.parameters())
print("Remote model2 parameters:")
print(param2)

remote_model1_updates = remote_model1.get(
    request_block=True
).state_dict()

print(remote_model1_updates)
remote_model2_updates = remote_model2.get(
    request_block=True
).state_dict()

print(remote_model2_updates)
avg_updates = OrderedDict()
avg_updates["linear.weight"] = (
    remote_model1_updates["linear.weight"] + remote_model2_updates["linear.weight"]) / 2
avg_updates["linear.bias"] = (
    remote_model1_updates["linear.bias"] + remote_model2_updates["linear.bias"]) / 2

print(avg_updates)

# Load Aggregated weights

combined_model.load_state_dict(avg_updates)
del avg_updates
test_data = th.FloatTensor(np.array([17, 25, 32, 50, 80]).reshape(-1, 1))
test_target = th.FloatTensor(np.array([12, 15, 20, 30, 50]).reshape(-1, 1))
preds = []
with torch.no_grad():
    for i in range(len(test_data)):
        sample = test_data[i]
        y_hat = combined_model(sample)

        print(f"Prediction: {y_hat.item()} Ground Truth: {test_target[i].item()}")
        preds.append(y_hat)

# Comparison to classical linear regression on centralised data
import torch
import numpy as np

in_dim = 1
out_dim = 1


class ClassicalLR(torch.nn.Module):
    def __init__(self, torch):
        super(ClassicalLR, self).__init__()
        self.linear = torch.nn.Linear(in_dim, out_dim)

    def forward(self, x):
        x = self.linear(x)
        return x


classical_model = ClassicalLR(torch)
data = torch.FloatTensor(
    np.array([5, 15, 25, 35, 45, 55, 60, 65, 75, 85, 95]).reshape(-1, 1)
)
target = torch.FloatTensor(
    np.array([5, 10, 15, 22, 30, 38, 35, 40, 45, 55, 60]).reshape(-1, 1)
)
def classic_train(iterations, model, torch, optim, data, target, criterion):

    losses = []

    for i in range(iterations):

        optim.zero_grad()

        output = model(data)

        loss = criterion(output, target)

        loss_item = loss.item()

        if i % 10 == 0:
            print("Epoch", i, "loss", loss_item)

        losses.append(loss_item)

        loss.backward()

        optim.step()

    return losses
params = classical_model.parameters()
optim = torch.optim.Adam(params=params, lr=0.1)
criterion = torch.nn.MSELoss()

iteration = 100
losses = classic_train(
    iteration, classical_model, torch, optim, data, target, criterion)
test_data = th.FloatTensor(np.array([17, 25, 32, 50, 80]).reshape(-1, 1))
test_target = th.FloatTensor(np.array([12, 15, 20, 30, 50]).reshape(-1, 1))

preds = []
with torch.no_grad():
    for i in range(len(test_data)):
        sample = test_data[i]
        y_hat = classical_model(sample)

        print(f"Prediction: {y_hat.item()} Ground Truth: {test_target[i].item()}")
        preds.append(y_hat)
