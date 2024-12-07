from xarray import Dataset
from .abstract import SpectralData

class IZData(SpectralData):
    def __init__(self, src: str, raw: Dataset):
        super().__init__(src, raw)
        self.iz = self.raw.Current
        self.coords = self.get_unique_coords(zip(self.iz.RHK_SpecDrift_Xcoord, self.iz.RHK_SpecDrift_Ycoord))