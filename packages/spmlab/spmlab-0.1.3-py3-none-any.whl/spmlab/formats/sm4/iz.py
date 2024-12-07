from xarray import Dataset

from pathlib import Path

class IZData:
    def __init__(self, src: str, ds: Dataset):
        self.path = Path(src)
        self.name = self.path.stem
        self.ds = ds.Current
        self.coords = self.get_unique_coords(zip(self.iz.RHK_SpecDrift_Xcoord, self.iz.RHK_SpecDrift_Ycoord))