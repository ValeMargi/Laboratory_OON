class Signal_information:
    def __init__(self, signal_power, noise_power, latency, path):
        self._signal_power = signal_power
        self._noise_power = noise_power
        self._latency = latency
        self._path = path

    # getter for all attribute
    # setter for attribute that y want to change
    @property
    def signal_power(self):
        return self._signal_power

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    def update_signal_power(self, increment):
        self.signal_power += increment

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    def update_noise_power(self, increment):
        self._noise_power += increment

    @property
    def latency(self):
        return self._latency
    @latency.setter
    def latency(self, latency):
        self._latency = latency

    def update_latency(self, increment):
        self._latency += increment

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, path):
        self._path = path

    def update_path(self):
        self._path = self.path.pop(0)

si = Signal_information(2.5, 0, 0, ["A", "B"])
