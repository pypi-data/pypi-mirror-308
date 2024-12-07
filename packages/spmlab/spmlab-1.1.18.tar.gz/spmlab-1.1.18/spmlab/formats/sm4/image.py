## Typing
from warnings import warn

## External packages
from xarray import Dataset

## Internal packages
from ._abstract import AbstractSM4Data
from .topo import TopoData

class ImageData(AbstractSM4Data):
    """
        ImageData is a container for the forward and backward topography data coming from src.
        Technically an AbstractSM4Data subclass, but doesn't implement the abstract methods
        and instead holds two references to other AbstractSM4Data subclasses (TopoData)
    """
    def __init__(self, src: str, ds: Dataset):
        super().__init__(src, ds)
        self.forward = TopoData(self.ds.Topography_Forward)
        self.backward = TopoData(self.ds.Topography_Backward)

    def plot(self):
        warn(("Cannot call plot on ImageData object." 
             "Please call plot() on the forward or backward attributes:" 
             "---------------------------------------------------------" 
             "from spmlab.formats import sm4" 
             "topo = sm4.read(\"path/to/topo/data.sm4\")"
             "topo.forward.plot()"))