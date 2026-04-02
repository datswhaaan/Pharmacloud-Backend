
from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def upload(self, file) -> str:
        """
        Upload file and return file identifier or URL
        """
        pass