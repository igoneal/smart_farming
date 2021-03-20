import syft as sy

# Launch a Duet Server and upload data
duet = sy.launch_duet(loopback=True)
import torch as th
import numpy as np

data = th.FloatTensor(np.array([5, 15, 25, 35, 45, 55]).reshape(-1, 1))

data = data.tag("DO1 data")
data = data.describe("Dataset of 6 samples, 1 feature")

data_ptr = data.send(duet, pointable=True)

duet.store.pandas
data
duet.requests.add_handler(
    action="accept",
    print_local=True,  # print the result in your notebook
)
