from scipy.constants import c, h
from Lab10.core.Info.Lightpath import Lightpath
import numpy as np
from math import ceil

n_channel = 10
Bn = 12.5e9
g = 16  # dB
nf = 3  # dB
f = 193.414e12  # C-band center
alpha_dB_km = 0.2  # dB/Km
beta2 = 2.13e-26  # (m Hz^2)^-1
gamma = 1.27e-3  # inv(WM)
df = 50e9  # GHz
Rs = 32e9  # GHz
Pch_base = 1e-3


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = np.ones(n_channel, np.int8)  # Free
        self._n_amplifiers = 0
        self._gain = g
        self._noise_figure = nf
        self._alfa = (alpha_dB_km / 1e3) / (20 * np.log10(np.exp(1)))
        self._beta2 = beta2
        self._gamma = gamma
        self._Leff = 1 / (2 * self.alfa)
        self._n_span = 0

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

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @n_amplifiers.setter
    def n_amplifiers(self, n_amplifiers):
        self._n_amplifiers = n_amplifiers
        self._n_span = n_amplifiers - 1

    @property
    def gain(self):
        return self._gain

    @property
    def noise_figure(self):
        return self._noise_figure

    @property
    def alfa(self):
        return self._alfa

    @property
    def beta2(self):
        return self._beta2

    @property
    def gamma(self):
        return self._gamma

    @property
    def Leff(self):
        return self._Leff

    @property
    def n_span(self):
        return self._n_span

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal):
        noise = self.ase_generation() + self.nli_generation(signal)
        return noise

    def propagate(self, signal_information):

        if type(signal_information) is Lightpath:
            if signal_information.channel is not None: # ==1
                self.state[signal_information.channel] = 0  # 'occupied'

        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        print("path before noise_gen ", signal_information.path)
        noise = self.noise_generation(signal_information)
        signal_information.add_noise(noise)

        # Update gsnr
        signal_information.isnr += self.isnr_computation(signal_information)

        node = self.successive[signal_information.path[0]]
        if type(signal_information) is Lightpath:
            signal_information = node.propagate(signal_information, self.label[0])
        else:
            signal_information = node.propagate(signal_information, None)
        return signal_information

    def ase_generation(self):
        #print("LEN: ", self.length)
        self.n_amplifiers = (ceil(self.length / 80e3) -1)+2
        return self.n_amplifiers * (h * f * Bn * (10 ** (self.noise_figure / 10)) * ((10 ** (self.gain / 10)) - 1))

    def nli_generation(self, signal ):
        # print("log", ((np.pi ** 2) * self.beta2 * (Rs ** 2) * (n_channel ** (2 * Rs / df))))
        nli = signal.signal_power ** 3 * self.eta_nli_generation() * self.n_span * Bn
        print("PATH signal: ", signal.path)
        print("N_SPAN: ", self.n_span, "Bn: ", Bn, "Pch_base: ", signal.signal_power)
        print("NLI: ", nli, "ETA: ", self.eta_nli_generation(), "ASE: ", self.ase_generation())
        return nli

    def optimized_launch_power(self):
        return (self.ase_generation() / (2 * self.eta_nli_generation() * self.n_span * Bn)) ** (1/3)

    def eta_nli_generation(self):
        return 16 / (27 * np.pi) * np.log(
            (np.pi ** 2) / 2 * self.beta2 * (Rs ** 2) / self.alfa * (n_channel ** (2 * Rs / df))) \
               * (self.alfa / self.beta2 * ((self.gamma ** 2) * (self.Leff ** 2) / (Rs ** 3)))

    def gsnr_computation(self, signal):
        return signal.signal_power / self.noise_generation(signal)

    def isnr_computation(self, signal):
        return 1 / self.gsnr_computation(signal)
