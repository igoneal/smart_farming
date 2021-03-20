import syft as sy

# Launch a Duet Server and upload data
duet = sy.launch_duet(loopback=True)
import torch as th
import numpy as np

data = th.FloatTensor(np.array([60, 65, 75, 85, 95]).reshape(-1, 1))

data = data.tag("DO2 data")
data = data.describe("Dataset of 5 samples, 1 feature")

data_ptr = data.send(duet, pointable=True)

duet.store.pandas
data
duet.requests.add_handler(
    action="accept",
    print_local=True,  # print the result in your notebook)
