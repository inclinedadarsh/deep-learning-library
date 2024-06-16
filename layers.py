"""
Our neural network will be made up of layers.
Each layer needs to pass it inputs forward,
and propagate gradients backward.
For example, a neural net might look like

input -> Linear -> Tanh -> Linear -> output
"""

import numpy as np
from numpy import ndarray
from typing import Callable

Func = Callable[[ndarray], ndarray]


class Layer:
    params: dict[str, ndarray]
    grads: dict[str, ndarray]

    def __init__(self):
        self.params = {}
        self.grads = {}

    def forward(self, inputs: ndarray) -> ndarray:
        """
        Produce the outputs corresponding to these inputs
        :param inputs: ndarray
        :return: ndarray
        """
        raise NotImplementedError

    def backward(self, grad: ndarray) -> ndarray:
        """
        Back propagate this layer through the layer
        :param grad: ndarray
        :return: ndarray
        """
        raise NotImplementedError


class Linear(Layer):
    """
    Computes output = inputs @w + @b
    """

    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        self.grad = None
        self.inputs = None
        self.params["w"] = np.random.randn(input_size, output_size)
        self.params["b"] = np.random.randn(output_size)

    def forward(self, inputs: ndarray) -> ndarray:
        """
        Outputs = inputs * w + b
        :param inputs: ndarray
        :return: ndarray
        """

        self.inputs = inputs
        return inputs @ self.params["w"] + self.params["b"]

    def backward(self, grad: ndarray) -> ndarray:
        """
        if y = f(x) and x = a * b + c
        then dy/da = f'(x) * b
        dy/db = f'(x) * a
        dy/dc = f'(x)

        if y = f(x) and x = a @ b + c
        then dy/da = f'(x) @ b.T
        and dy/db = a.T @ f'(x)
        and dy/dc = f'(x)
        :param grad: ndarray        :return: ndarray
        """
        self.grad["b"] = np.sum(grad, axis=0)
        self.grad["w"] = self.inputs.T @ grad
        return grad @ self.params["w"].T


class Activation(Layer):
    """
    Activation layer just applies a function
    elementwise to its inputs
    """

    def __init__(self, f: Func, f_prime: Func) -> None:
        super().__init__()
        self.inputs = None
        self.f = f
        self.f_prime = f_prime

    def forward(self, inputs: ndarray) -> ndarray:
        self.inputs = inputs
        return self.f(self.inputs)

    def backward(self, grad: ndarray) -> ndarray:
        """
        if y = f(x) and x = g(z)
        then dy/dz = f'(x) * g'(z)
        :param grad: ndarray
        :return: ndarray
        """
        return self.f_prime(self.inputs) * grad


def tanh(x: ndarray) -> ndarray:
    """
    Applies the Tanh function to the input 'x'
    :param x: ndarray
    :return: ndarray
    """
    return np.tanh(x)


def tanh_prime(x: ndarray) -> ndarray:
    """
    Applies d(Tanh)/dx at x
    :param x: ndarray
    :return: ndarray
    """
    y = tanh(x)
    return 1 - np.power(y, 2)


class Tanh(Activation):
    def __init__(self):
        super().__init__(tanh, tanh_prime)
