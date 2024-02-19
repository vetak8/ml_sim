from abc import ABC, abstractmethod
from typing import List

class DataPreprocessor(ABC):
    @abstractmethod
    def preprocess(self, data: List) -> List:
        pass

class OutlierRemover(DataPreprocessor):
    '''
    Function preprocess data by own way
    '''
    def preprocess(self, data: List) -> List:
        return list(filter(lambda x: x<=10, data))

class Normalizer(DataPreprocessor):
    '''
    Function preprocess data by own way
    '''
    def preprocess(self, data: List) -> List:
        return list(map(lambda x: x/10, data))

class Encoder(DataPreprocessor):
    '''
    Function preprocess data by own way
    '''
    def __init__(self, encoding_dict):
        self.encoding_dict = encoding_dict
    def preprocess(self, data: List) -> List:
        return [self.encoding_dict[x] for x in data]
