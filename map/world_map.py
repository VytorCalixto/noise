from abc import ABC, abstractmethod
import numpy as np


class AbstractWorldMap(ABC):
    def __init__(self, seed: int = None):
        self.points = []
        self.seed = seed

    @abstractmethod
    def generate_world(self):
        pass

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed if seed is not None else np.random.randint(0, high=2 ** 32 - 1)
