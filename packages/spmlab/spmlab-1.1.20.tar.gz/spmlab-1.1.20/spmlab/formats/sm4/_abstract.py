## Typing
from abc import ABC, abstractmethod
from typing import List

## External packages
import numpy as np
from xarray import Dataset
from pathlib import Path
from datetime import datetime
import os

from ...readers.spym.io import load


class AbstractSM4Data(ABC):
    """
    """
    def __init__(self, src: str, ds: Dataset):
        self.path = Path(src)
        self.name = self.path.stem
        self.ds = ds

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
    
    def get_last_image(self):
        if len(self.path.name.split("_")) < 7:
            return None
        
        src_dir = self.path.parent
        files = [x for x in os.listdir(src_dir) if x.endswith('.sm4')]
        dates = [x.split('.')[0].split('_') for x in files]
        dates = [x[-7:] for x in dates if len(x) > 7]
        dates = [datetime.datetime(*[int(d) for d in date]) for date in dates]
        dates = list(zip(dates, range(len(dates))))
        dates_sorted, permuted_indices = list(zip(*sorted(dates)))
        file_date = self.path.name.split('.')[0].split('_')[-7:]  # Date of the current file
        file_date = datetime.datetime(*[int(d) for d in file_date])
        
        files = [files[i] for i in list(permuted_indices)]
        idx = dates_sorted.index(file_date) # index of the current file in the date ordered list
        topography = None

        while idx >= 0:
            f = load(os.path.join(src_dir, files[idx]))
            if f is None:
                idx -= 1
            elif 'data_vars' in f.__dir__():
                if 'Topography_Forward' in f.data_vars:
                    topography = f.Topography_Forward
                    if topography.data.shape[0] == topography.data.shape[1]: ### There is no full proof way to tell the difference between data that has only dIdV and data that has both image and dIdV - checking if the image is square is the closest option
                        line_average = np.average(topography.data, axis=1)
                        num_zeros = len(topography.data) - np.count_nonzero(line_average)
                        if num_zeros == 0:
                            break
                        else:
                            topography = None
                idx -= 1
            else:
                idx -= 1

        return topography