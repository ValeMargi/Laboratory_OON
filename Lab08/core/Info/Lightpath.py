from Lab08.core.Info.SignalInformation import SignalInformation

class Lightpath(SignalInformation):
    def __init__(self, power, path, channel):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
