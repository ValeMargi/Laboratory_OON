from scipy.constants import c
from Lab08.core.Info.Lightpath import Lightpath
import numpy as np

n_channel = 10

class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = np.ones(n_channel, np.int8) #Free

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = 1e-9 * signal_power * self.length
        return noise

    def propagate(self, signal_information):

        if type(signal_information) is Lightpath:
            if signal_information.channel is not None:
                self.state[signal_information.channel] = 0 #'occupied'

        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        node = self.successive[signal_information.path[0]]
        if type(signal_information) is Lightpath:
            signal_information = node.propagate(signal_information, self.label[0])
        else:
            signal_information = node.propagate(signal_information, None)
        return signal_information