'''
1. Define the class Signal information that has the following attributes:
• signal power: float
• noise power: float
• latency: float
• path: list[string]
such that its constructor initializes the signal power to a given value, the
noise power and the latency to zero and the path as a given list of letters
that represents the labels of the nodes the signal has to travel through.
The attribute latency is the total time delay due to the signal propagation
through any network element along the path.
Define the methods to update the signal and noise powers and the latency given
an increment of these quantities. Define a method to update the path once a node is crossed.
'''
class SignalInformation(object):
    def __init__(self, power, path):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0

    # getter for all attribute
    # setter for attribute that y want to change

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def path(self):
        return self._path

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @path.setter
    def path(self, path):
        self._path = path

    @noise_power.setter
    def noise_power(self, noise):
        self._noise_power = noise

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    def add_noise(self, noise):
        self.noise_power = self._noise_power + noise

    def add_latency(self, latency):
        self.latency += latency  # getter call

    def next(self):
        self.path = self.path[1:]
        # soluzione alternativa
        # self.path.pop(0)  # first element drop


