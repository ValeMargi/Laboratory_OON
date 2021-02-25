from scipy.constants import c, h
from Lab10.core.Info.Lightpath import Lightpath
import numpy as np
from math import ceil

n_channel = 10  # Number of channel
Bn = 12.5e9  # Noise Bandwidth [GHz]
G = 16   # Gain amplifier  [dB]
NF = 3  # Noise Figure [dB]
f = 193.414e12  # C-band center
alpha_dB_km = 0.2  # Fiber attenuation loss[dB/Km]
beta2 = 2.13e-26  # chromatic dispersion factor [(m Hz^2)^-1]
gamma = 1.27e-3  # non-linearity coefficient [inv(WM)]
df = 50e9  # WDM channel spacing [Hz]
Rs = 32e9  # Symbol Rate [Hz]
Pch_base = 1e-3  # Power base [W]


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = np.ones(n_channel, np.int8)  # Free
        self._n_amplifiers = 0
        self._gain = G
        self._noise_figure = NF
        self._alfa = (alpha_dB_km / 1e3) / (20 * np.log10(np.exp(1)))
        self._beta2 = beta2
        self._gamma = gamma
        self._Leff = 1 / (2 * self.alfa)   # Effective Length
        self._n_span = 0   # Number of span

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
        ''' span located between two amplifing site '''
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
        """ Noise calculation due to the presence of ASE noise and NLI noise in the fiber propagation"""
        noise = self.ase_generation() + self.nli_generation(signal)
        return noise

    def propagate(self, signal_information):
        """Propagate of signal information is used only to propagate
         the signal at the starting point in the network creation"""
        if type(signal_information) is Lightpath:
            '''If the channel is free, during the lightpath propagation,
              we sent the channel line state at occupied'''
            if signal_information.channel is not None: # ==1
                self.state[signal_information.channel] = 0  # '0 = occupied'

        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        noise = self.noise_generation(signal_information)
        signal_information.add_noise(noise)

        # Update isnr for the lightpath adding the isnr of the current line
        signal_information.isnr += self.isnr_computation(signal_information)

        node = self.successive[signal_information.path[0]]

        if type(signal_information) is Lightpath:
            ''' if the signal is a ligthpath, the first node of current line is passed in the
             propagate method in order to set as occupied channels '''
            signal_information = node.propagate(signal_information, self.label[0])
        else:
            signal_information = node.propagate(signal_information, None)
        return signal_information

    def ase_generation(self):
        ''' Supposing to have one inline amplifier every 80km plus one booster and preamp amplifier'''
        self.n_amplifiers = (ceil(self.length / 80e3) -1)+2
        ''' Calculating additive ASE noise introduced by a cascade of amplifiers as ASE=N(h*f*B_n*NF(G-1))'''
        return self.n_amplifiers * (h * f * Bn * (10 ** (self.noise_figure / 10)) * ((10 ** (self.gain / 10)) - 1))

    '''Observation:
        NLI increases with:
        - Reduction of chromatic dispersion (beta2)
        - Reduction of fiber loss (alfa)
        - Reduction of channel spacing (df)
        - Increase of nonlinear coefficient (gamma)
        - Increase of number of channel, even if weak (n_channel)'''
    def nli_generation(self, signal):
        # NLI = Pch^3 * eta_nli * n_span
        nli = signal.signal_power ** 3 * self.eta_nli_generation() * self.n_span * Bn
        '''
        print("PATH signal: ", signal.path)
        print("N_SPAN: ", self.n_span, "Bn: ", Bn, "Pch_base: ", signal.signal_power)
        print("NLI: ", nli, "ETA: ", self.eta_nli_generation(), "ASE: ", self.ase_generation())
        '''
        return nli

    def optimized_launch_power(self):
        # Optimal power = (Pase/ (2/eta_nli * n_span*Bn)) ^ 1/3
        return (self.ase_generation() / (2 * self.eta_nli_generation() * self.n_span * Bn)) ** (1/3)

    def eta_nli_generation(self):
        return 16 / (27 * np.pi) * np.log(
            (np.pi ** 2) / 2 * self.beta2 * (Rs ** 2) / self.alfa * (n_channel ** (2 * Rs / df))) \
               * (self.alfa / self.beta2 * ((self.gamma ** 2) * (self.Leff ** 2) / (Rs ** 3)))

    def gsnr_computation(self, signal):
        return signal.signal_power / self.noise_generation(signal)

    def isnr_computation(self, signal):
        return 1 / self.gsnr_computation(signal)
