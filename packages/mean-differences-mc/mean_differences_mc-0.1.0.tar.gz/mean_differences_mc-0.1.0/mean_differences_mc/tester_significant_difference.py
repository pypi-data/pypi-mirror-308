import numpy as np
import pandas as pd

from .switch_elements import switch_elements_arrays
from .index_switch import index_to_switch


class TesterSignificantDifference:
    def __init__(self):
        self._sample_a: np.array = np.array([])
        self._sample_b: np.array = np.array([])

    @property
    def sample_a(self):
        return self.__sample_a

    @sample_a.setter
    def sample_a(self, sample_a: pd.DataFrame):
        name_column = sample_a.columns[0]
        self.__sample_a = np.append(self._sample_a, np.array(sample_a[name_column]))

    @property
    def sample_b(self):
        return self.__sample_b

    @sample_b.setter
    def sample_b(self, sample_b: pd.DataFrame):
        name_column = sample_b.columns[0]
        self.__sample_b = np.append(self._sample_b, np.array(sample_b[name_column]))

    def switch_elements(self, index):
        self.sample_a, self.sample_b = switch_elements_arrays(self.sample_a, self.sample_b, index)

    def index_to_switch(self):
        lim_max = len(self.sample_a)
        return index_to_switch(lim_max)
