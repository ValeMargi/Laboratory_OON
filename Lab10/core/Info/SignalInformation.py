class SignalInformation(object):
    def __init__(self, power, path):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0
        self._isnr = 0.0

    @property
    def signal_power(self):
        return self._signal_power

    @signal_power.setter
    def signal_power(self, power):
        self._signal_power = power

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

    @property
    def isnr(self):
        return self._isnr

    @isnr.setter
    def isnr(self, isnr):
        self._isnr = isnr

    def add_noise(self, noise):
        self.noise_power = self._noise_power + noise

    def add_latency(self, latency):
        self.latency += latency

    def next(self):
        self.path = self.path[1:]