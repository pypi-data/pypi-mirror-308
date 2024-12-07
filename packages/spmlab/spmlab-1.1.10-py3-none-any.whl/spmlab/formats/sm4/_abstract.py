## Typing
from abc import ABC, abstractmethod
from typing import List

## External packages
from xarray import Dataset
from pathlib import Path


class AbstractSM4Data(ABC):
    """
    """
    def __init__(self, src: str, raw: Dataset):
        self.path = Path(src)
        self.name = self.path.stem
        self.raw = raw

    @abstractmethod
    def scale_data(self, scale: float):
        """ Abstract method
            Should scale subclass's data by scale
            Args:
                scale: scale factor to scale data by
            Returns:
                None
        """
        pass

    @abstractmethod
    def get_min(self) -> float:
        """ Abstract method
            Should return minimum of subclass's data
            Args:
                None
            Returns:
                minimum of subclass's data
        """
        pass

    @abstractmethod
    def get_max(self) -> float:
        """ Abstract method
            Should return maximum of subclass's data
            Args:
                None
            Returns:
                maximum of subclass's data
        """
        pass


class SpectralData(AbstractSM4Data):
    def __init__(self, src: str, raw: Dataset):
        super().__init__(src, raw)

    def get_unique_coords(self, coords) -> List:
        """ 
            Returns the coordinates of subclass's data without any duplicates
            The set of unique coordinates can be used for plotting on top of an image.
            Args:
                coords: 
            Returns:
                list of unique coordinates
        """
        seen = set()
        seen_add = seen.add
        return [x for x in coords if not (x in seen or seen_add(x))]