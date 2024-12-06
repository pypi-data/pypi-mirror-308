import torch
import taichi as ti
from inspect import signature, Signature
from dataclasses import dataclass
from typing import Optional, Tuple, Any

@dataclass
class KernelArgData:
    name: Optional[str] = None
    is_tensor: bool = False
    is_input: bool = True
    is_output: bool = False
    idx_all: int = 0
    idx_value: Optional[int] = None
    idx_tensor: Optional[int] = None
    idx_output_tensor: Optional[int] = None
    shape: Optional[Tuple[int, ...]] = None
    dtype: Optional[str] = None
    ndim: Optional[int] = None
    type: Optional[Any] = None
    requires_grad: bool = False


def _check_output_specs(output_specs:dict):
    if not isinstance(output_specs, dict):
        raise TypeError(f'output_specs should be a dict, found : {type(output_specs)}.')
    for name, specs in output_specs.items():
        if hasattr(specs, '__len__'):
            if len(specs) != 3:
                raise ValueError(f'output_specs[\'{name}\'] should contain three values (shape, dtype, requires_grad).')
        else:
            raise TypeError(f'output_specs[\'{name}\'] should be an Iterable. found : {type(output_specs[name])}')

            
def _check_kernel_signature(kernel_sig:Signature, output_specs:dict):
    kernel_sig_kwarg_names = list(kernel_sig.parameters.keys())
    for output_name in output_specs:
        if output_name not in kernel_sig_kwarg_names:
            raise KeyError(f'Argument named \'{output_name}\' not found in kernel signature.')

def _build_kernel_arg_data_list(kernel_sig:Signature, output_specs:dict):
    res = []
    cpt_tensor, cpt_value, cpt_output_tensor = 0,0,0 
    for name, param in kernel_sig.parameters.items():
        kad = KernelArgData(name=name)
        if name in output_specs:
            kad.is_tensor = True
            kad.is_input = False
            kad.is_output = True
            shape, dtype, requires_grad = output_specs[name]
            kad.ndim = len(shape)
            kad.shape = shape
            kad.dtype = dtype
            kad.requires_grad = requires_grad
            kad.idx_tensor = cpt_tensor
            kad.idx_output_tensor = cpt_output_tensor
            cpt_tensor += 1
            cpt_output_tensor += 1
        else:
            kad.is_input=True
            kad.is_output=False
            if isinstance(param.annotation, ti.types.ndarray_type.NdarrayType):
                kad.is_tensor = True
                kad.ndim = param.annotation.ndim
                kad.dtype = param.annotation.dtype
                kad.idx_tensor = cpt_tensor
                cpt_tensor += 1
            else:
                kad.is_tensor = False
                kad.idx_value = cpt_value
                cpt_value += 1
        res.append(kad)
    return res


     
class TaichiKernelModule(torch.nn.Module):
    def __init__(self, kernel, output_specs):
        """
        Initialize the Taichi kernel wrapper as a torch.nn.Module with persistent output tensors.

        Args:
        - kernel: The Taichi kernel to wrap.
        - output_specs: A dictionary where:
            - Keys are the names of the output arguments as they appear in the kernel.
            - Values are tuples specifying (shape, dtype, requires_grad).
              For example: {'out_positions': ((B, N, 3), torch.float32, True)}
        """
        super().__init__()
        _check_output_specs(output_specs)
        self.kernel_sig = signature(kernel)
        self.nargs = len(self.kernel_sig.parameters)
        _check_kernel_signature(self.kernel_sig, output_specs)
        self.device_tensor = torch.zeros((1,))

        self.kad_list = _build_kernel_arg_data_list(self.kernel_sig, output_specs)

        # Define the custom autograd function for forward and backward passes
        class _TaichiAutogradFunction(torch.autograd.Function):
            @staticmethod
            def forward(ctx, *input_args):
                
                input_args_list = list(input_args)

                kernel_args = []
                device = self.device_tensor.device

                output_tensors = []
                all_tensors = []
                values = []

                for kad in self.kad_list:
                    if kad.is_output:
                        output_tensor = torch.zeros(kad.shape, dtype=kad.dtype, requires_grad=kad.requires_grad, device=device)
                        output_tensors.append(output_tensor)
                        kernel_args.append(output_tensor)
                    else:
                        kernel_args.append(input_args_list.pop(0))
                    if kad.is_tensor:
                        all_tensors.append(kernel_args[-1])
                    else:
                        values.append(kernel_args[-1])

                kernel(*kernel_args)

                ctx.save_for_backward(*all_tensors)
                ctx.values = values

                return tuple(output_tensors)

            @staticmethod
            def backward(ctx, *output_grads):
                
                # Retrieve saved tensors for backward pass
                tensors = ctx.saved_tensors
                values = ctx.values

                grad_kernel_args = []

                for kad in self.kad_list:
                    if kad.is_tensor:
                        if kad.is_output and kad.requires_grad:
                            tensors[kad.idx_tensor].grad = output_grads[kad.idx_output_tensor].contiguous()
                        grad_kernel_args.append(tensors[kad.idx_tensor])
                    else:
                        grad_kernel_args.append(values[kad.idx_value])
                
                kernel.grad(*grad_kernel_args)
                
                input_grads = []
                for kad in self.kad_list:
                    if kad.is_output:
                        continue
                    grad = None
                    if kad.is_tensor:
                        if tensors[kad.idx_tensor].requires_grad:
                            grad = tensors[kad.idx_tensor].grad.contiguous()
                    input_grads.append(grad)
                
                return tuple(input_grads)

        self._TaichiAutogradFunction = _TaichiAutogradFunction.apply

    def forward(self, *args, **kwargs):
        """
        The forward method for the Taichi kernel module. Calls the autograd function to handle
        forward and backward computation.
        """
        input_args = list(args)

        kernel_args = []

        for kad in self.kad_list:
            if kad.is_output:
                continue
            if kad.name in kwargs:
                kernel_args.append(kwargs[kad.name])
            else:
                kernel_args.append(input_args.pop(0))

        return self._TaichiAutogradFunction(*kernel_args)