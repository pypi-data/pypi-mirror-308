## Typing
from warnings import warn

## External packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from xarray import DataArray, Dataset
from pathlib import Path

class TopoData:
    """
    """
    def __init__(self, topo: DataArray):
        self.topo = topo
        self.data = topo.data

    def plot(self,
             align=True, 
             plane=True, 
             fix_zero=True, 
             show_axis=False, 
             figsize=(8,8), 
             scalebar_height=None):
        """
        """
        img = self.topo

        if align:
            img.spym.align()
        if plane:
            img.spym.plane()
        if fix_zero:
            img.spym.fixzero()
        
        fig, ax = plt.subplots(figsize=figsize)
        if not show_axis:
            ax.axis('off')
        else:
            ax.set_xlabel("[nm]")
            ax.set_ylabel("[nm]")

        size = round(img.RHK_Xsize * abs(img.RHK_Xscale) * 1e9, 3)
        if scalebar_height is None:
            scalebar_height = 0.01 * size
        fontprops = fm.FontProperties(size=14)
        scalebar = AnchoredSizeBar(ax.transData,
                                   size/5, f'{size/5} nm', 'lower left',
                                   pad=0.25,
                                   color='white',
                                   frameon=False,
                                   size_vertical = scalebar_height,
                                   offset=1,
                                   fontproperties=fontprops)

        img = ax.imshow(img.data, extent=[0, size, 0, size], cmap='afmhot')
        ax.add_artist(scalebar)

        fig.tight_layout()
        return (fig, ax)


    def get_min(self) -> float:
        """
        """
        return np.min(self._topo.data)


    def get_max(self) -> float:
        """
        """
        return np.max(self._topo.data)


class ImageData:
    """
        ImageData is a container for the forward and backward topography data coming from src.
        Technically an AbstractSM4Data subclass, but doesn't implement the abstract methods
        and instead holds two references to other AbstractSM4Data subclasses (TopoData)
    """
    def __init__(self, src: str, ds: Dataset):
        self.path = Path(src)
        self.name = self.path.stem
        self.forward = TopoData(ds.Topography_Forward)
        self.backward = TopoData(ds.Topography_Backward)

    def plot(self):
        warn(("Cannot call plot on ImageData object." 
             "Please call plot() on the forward or backward attributes:" 
             "---------------------------------------------------------" 
             "from spmlab.formats import sm4" 
             "topo = sm4.read(\"path/to/topo/data.sm4\")"
             "topo.forward.plot()"))