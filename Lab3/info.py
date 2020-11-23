import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c


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

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, noise):
        self._noise_power = noise

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    def add_noise(self, noise):
        self.noise_power = self._noise_power + noise

    def add_latency(self, latency):
        self.latency += latency

    def next(self):
        self.path = self.path[1:]
        self.path.pop(0)  # first element drop

