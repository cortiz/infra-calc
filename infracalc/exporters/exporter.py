from abc import ABC, abstractmethod


class Exporter(ABC):

    def __init__(self, pricing_information, attrs):
        self.pricing_information = pricing_information
        self.attrs=attrs

    @abstractmethod
    def export(self):
        pass
