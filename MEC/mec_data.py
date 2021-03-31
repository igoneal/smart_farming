import syft as sy
import torch as th
import numpy as np

# Launch a Duet Server and upload data
duet = sy.duet_launch()


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
