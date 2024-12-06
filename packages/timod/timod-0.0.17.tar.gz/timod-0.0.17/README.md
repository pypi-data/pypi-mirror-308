# timod

TaichIMODule, a tiny pytorch module wrapper for differentiable Taichi kernels.

# Install

`pip install timod`

## Usage

Given a taichi kernel `my_kernel` with input and output tensors typed `ti.types.ndarray()`:

```python
from timod import TaichiKernelModule

# Output tensors specifications (since they will be created on the fly)
output_specs = {
    'out1':(<shape>, <dtype>, <needs gradients ?>), 
    'out2':(<shape>, <dtype>, <needs gradients ?>)
    ...}

# Module creation
taichi_module = TaichiKernelModule(my_kernel, output_specs)

# Kernel input args (torch tensors and scalars)
in1 = ...
in2 = ...
...

# Module call
out1, out2, ... = taichi_module(in1, in2, ...) # kwargs of the taichi kernel inputs are supported 

# Loss function
loss = my_loss(out1, out2, ...)

# Gradient computation
loss.backward()

# Gradient descent
lr = 1e-3
in1 -= lr * in1.grad
in2 -= lr * in2.grad
...

```

