from ncxlib.neuralnetwork.layers import Layer
import numpy as np
from ncxlib.util import log
from ncxlib.neuralnetwork.losses import BinaryCrossEntropy
from ncxlib.neuralnetwork.activations import LeakyReLU, Sigmoid


class OutputLayer(Layer):
    def __init__(
        self,  layer: Layer, loss_fn, n_neurons=None,  n_inputs=None, activation=..., optimizer=...
    ):
        if layer:
            self.layer = layer
            layer.loss_fn = loss_fn
            super().__init__(
                layer.n_inputs, layer.n_neurons, layer.activation, layer.optimizer, loss_fn=loss_fn
            )
        if loss_fn == BinaryCrossEntropy and isinstance(self.layer.activation, LeakyReLU):
            print("Changing LeakyReLU to Sigmoid function for output layer for BCE.")
            self.layer.activation = Sigmoid()
            self.activation = Sigmoid()

    def forward_propagation(self, inputs, no_save):
        return self.layer.forward_propagation(inputs, no_save)

    def back_propagation(self, y_true: np.ndarray, learning_rate: float) -> None:

        activated = np.clip(self.layer.activated, 1e-7, 1 - 1e-7)

        dl_da = self.layer.loss_fn.compute_gradient(y_true, activated)
        
        
        da_dz = self.layer.activation.derivative(self.layer.z)

        dl_dz = dl_da * da_dz 

        self.layer.gradients = dl_dz
        self.layer.old_W = self.layer.W.copy()

        dl_dw = dl_dz @ self.layer.inputs.T 
        dl_db = np.sum(dl_dz, axis=1, keepdims=True)

        self.layer.W, self.layer.b = self.layer.optimizer.apply(self.layer.W, dl_dw, self.layer.b, dl_db)