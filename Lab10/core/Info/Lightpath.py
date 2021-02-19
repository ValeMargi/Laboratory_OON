from Lab10.core.Info.SignalInformation import SignalInformation
df = 50e9  # WDM channel spacing [Hz]
Rs = 32e9  # Symbol Rate [Hz]


class Lightpath(SignalInformation):
    def __init__(self, power, path, channel):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0
        self._isnr = 0.0
        self._channel = channel
        self._symbol_rate = Rs
        self._df = df

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def symbol_rate(self):
        return self._symbol_rate

    @property
    def df(self):
        return self._df
