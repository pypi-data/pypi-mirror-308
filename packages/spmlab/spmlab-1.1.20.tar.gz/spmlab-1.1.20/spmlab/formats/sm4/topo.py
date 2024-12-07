## Typing
from warnings import warn

## External packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from xarray import DataArray

## Internal packages
from ._abstract import AbstractSM4Data
    

class TopoData(AbstractSM4Data):
    """
    """
    def __init__(self, topo: DataArray):
        self._topo = topo

    def plot(self,
             align=True, 
             plane=True, 
             fix_zero=True, 
             show_axis=False, 
             figsize=(8,8), 
             scalebar_height=None):
        """
        """
        img = self._topo

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


    def scale_data(self, scale: float):
        warn("Cannot scale image data. Access self.ds to scale data manually.")