## Typing
from xarray import Dataset
from typing import List
from collections import namedtuple

## External packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from pathlib import Path

xydata = namedtuple("xydata", {"x", "y"})

class STSData:
    """
    A class to handle Scanning Tunneling Spectroscopy (STS) data, extending from the `SpectralData` base class.
    
    This class provides methods for processing and visualizing STS data, specifically creating a waterfall plot
    of the Local Density of States (LDOS) from the data.

    Attributes:
        ldos (Dataset): The Local Density of States (LIA_Current) dataset.
        coords (list): A list of unique coordinates derived from the `RHK_SpecDrift_Xcoord` and `RHK_SpecDrift_Ycoord` attributes.
        
    Methods:
        __init__(src: str, ds: Dataset): Initializes the STSData object with the source and ds data.
        waterfall(figsize=(8, 8), spacing=None, cmap=plt.cm.jet): Generates a waterfall plot of the LDOS data.
    """
    def __init__(self, src: str, ds: Dataset):
        """
        Initializes the STSData object by extracting the required datasets and coordinates.

        Args:
            src (str): The source or identifier of the data.
            ds (Dataset): The ds data (likely a NetCDF or HDF5 Dataset) containing the LIA_Current and other attributes.
        
        Attributes:
            ldos (Dataset): The LIA_Current dataset, representing the Local Density of States.
            coords (list): A list of unique coordinates obtained from the `RHK_SpecDrift_Xcoord` and `RHK_SpecDrift_Ycoord`.
        """
        self.path = Path(src)
        self.name = self.path.stem
        self.ds = ds.LIA_Current
        self.data = xydata(x=ds.LIA_Current_x.data, y=ds.LIA_Current.data)
        self.coords = self.get_unique_coords(zip(self.ds.RHK_SpecDrift_Xcoord, self.ds.RHK_SpecDrift_Ycoord))


    def waterfall(self,
                  figsize=(8,8), 
                  spacing=None, 
                  cmap=plt.cm.jet):
        """
        Generates a waterfall plot of the Local Density of States (LDOS) data.

        This method processes the LIA_Current dataset to create a 2D plot where each line represents a LDOS 
        at varying points in space, with a vertical offset applied to create the 'waterfall' effect.

        Args:
            figsize (tuple): The size of the figure (default is (8, 8)).
            spacing (float or None): The vertical spacing between each curve in the waterfall plot. If None, 
                                      it is automatically set to 1/10th of the maximum value in the data.
            cmap (matplotlib.colors.Colormap): The colormap used to color the curves (default is `plt.cm.jet`).
        
        Returns:
            tuple: A tuple containing the `fig` and `ax` (matplotlib figure and axes objects) for the generated plot.

        Raises:
            ValueError: If no valid STS data is found (i.e., if the coordinates list is empty).
        """
        N = len(self.coords)
        if N == 0:
            print("No STS data found.")
            return

        xsize = self.ds.RHK_Xsize
        total = self.ds.RHK_Ysize
        repetitions = total//N
        x = self.ds.LIA_Current_x.data * 1e3
        ldos = self.ds.data.reshape(xsize, N, repetitions).mean(axis=2).T

        ## Plot
        if spacing is None:
            spacing = np.max(ldos) / 10
        waterfall_offset = np.flip([i * spacing for i in range(N)])
        colors = cmap(np.linspace(0, 1, N))

        fig, ax = plt.subplots(figsize=figsize)
        for (i, dIdV) in enumerate(ldos):
            ax.plot(x, dIdV + waterfall_offset[i], c=colors[i])

        fig.tight_layout()
        return (fig, ax)


    def matrix(self,
               as_linecut=False,
               aspect=None, 
               norm=None, 
               cmap=plt.cm.jet, 
               color_bar=True, 
               vmax=None,
               clip_max=None,
               clip_min=None):
        """
        Plot the Local Density of States (LDOS) along a line as a 2d image.

        This method visualizes the LDOS data in the form of a 2D image, showing the variation in the spectral data 
        along a line between the first and last coordinate points. It can also normalize, clip, and apply colormap 
        adjustments to the data.

        Args:
            as_linecut (bool): Whether to display ticks and labels as spectral linecut data
            aspect (float or None): The aspect ratio of the plot. If `None`, the aspect ratio is automatically set 
                                    based on the voltage range and the length of the line cut.
            norm (matplotlib.colors.Normalize or None): Normalization for the colormap scaling. If `None`, no normalization is applied.
            cmap (str or matplotlib.colors.Colormap): The colormap to be used for displaying the data (default is plt.cm.jet).
            color_bar (bool): If `True`, a color bar will be displayed alongside the image (default is `True`).
            vmax (float or None): The maximum value for the colormap. If `None`, the maximum value in the data is used.
            clip_max (float or None): If provided, values above this threshold will be clipped to `clip_max`.
            clip_min (float or None): If provided, values below this threshold will be clipped to `clip_min`.

        Returns:
            tuple: A tuple containing the figure (`fig`), axes (`ax`), and the color bar (`cb`) (if `color_bar=True`).

        Raises:
            ValueError: If no STS data is found (i.e., if the coordinates list is empty).
        """
        N = len(self.coords)
        if N == 0:
            print("No STS data found.")
            return

        xsize = self.ds.RHK_Xsize
        total = self.ds.RHK_Ysize
        repetitions = total//N
        x = self.ds.LIA_Current_x.data * 1e3
        ldos = self.ds.data.reshape(xsize, N, repetitions).mean(axis=2).T

        fig, ax = plt.subplots(figsize=(16,7))

        line_cut = (self.coords[-1][0] - self.coords[0][0], self.coords[-1][1] - self.coords[0][1])
        line_length = np.sqrt(line_cut[0]**2 + line_cut[1]**2) * 1e9

        if aspect is None:
            aspect = abs(x[-1] - x[0]) / line_length

        if clip_max:
            ldos = ldos.clip(None, clip_max)
        if clip_min:
            ldos = ldos.clip(clip_min, None)

        img = ax.imshow(ldos, aspect=aspect, extent=[x[0], x[-1], 0, line_length], norm=norm, cmap=cmap, vmax=vmax)

        if as_linecut:
            ax.set_yticks(np.linspace(line_length, 0, 10))
            ax.set_yticklabels(map(lambda x: "%.2f" % x, np.linspace(line_length, 0, 10)))

            ax.set_xlabel("Voltage (mV)")
            ax.set_ylabel("Distance (nm)")

        cb = None
        if color_bar:
            cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
            cb = fig.colorbar(img, cax=cax)
        
        return (fig, ax, cb)


    def coordinates(self, 
                    image_path=None, 
                    image_type='forward', 
                    align=True, 
                    plane=True, 
                    fix_zero=True, 
                    show_axis=False, 
                    scalebar_height=None, 
                    figsize=(8,8), 
                    cmap='afmhot',
                    arrow=False):
        """
        Visualize the coordinates of the Scanning Tunneling Spectroscopy (STS) data on top of a topography image.

        This method generates a plot of the STS data coordinates on top of a specified topography image. If no 
        topography file path is given then the most recent complete image is attempted to be used.
        The coordinates are shown as points on the image, and the user can optionally display an arrow representing 
        the direction from the first to the last coordinate. Additionally, options are provided to adjust the plot's 
        appearance, including axis visibility, scaling, and the inclusion of a scalebar.

        Args:
            image_path (str or None): Path to the topography image file. If `None`, the most recent image is used.
            image_type (str): Type of topography image to load, either 'forward' or 'backward' (default is 'forward').
            align (bool): If `True`, aligns the topography data using the alignment function (default is `True`).
            plane (bool): If `True`, removes any plane component from the topography data (default is `True`).
            fix_zero (bool): If `True`, fixes the zero position of the topography data (default is `True`).
            show_axis (bool): If `True`, displays the axes on the plot (default is `False`).
            scalebar_height (float or None): Height of the scalebar in nanometers. If `None`, a default value is used.
            figsize (tuple): Size of the figure (default is (8, 8)).
            cmap (str or matplotlib.colors.Colormap): Colormap for the topography image (default is 'afmhot').
            arrow (bool): If `True`, draws an arrow from the first to the last coordinate (default is `False`).
            
        Returns:
            tuple: A tuple containing the figure (`fig`) and axes (`ax`) for the plot.

        Raises:
            ValueError: If no STS data is found (i.e., if the coordinates list is empty).
        """
        N = len(self.coords)
        if N == 0:
            print("No STS data found.")
            return

        topo = None
        if image_path is None:
            topo = self.get_last_image()
        else:
            try:
                topo_sm4 = load(image_path)
                match image_type:
                    case 'forward':
                        topo = topo_sm4.Topography_Forward
                    case 'backward':
                        topo = topo_sm4.Topography_Backward
                    case _:
                        print("Invalid image_type. Please use 'forward' or 'backward'")
            except:
                print(f"Couldn't load topography data from {image_path}")
                return
        
        if topo is None:
            print("No topography data found.")
            return

         ## Spec Coordinates
        xoffset = topo.RHK_Xoffset
        yoffset = topo.RHK_Yoffset
        xscale = topo.RHK_Xscale
        yscale = topo.RHK_Yscale
        xsize = topo.RHK_Xsize
        ysize = topo.RHK_Ysize
        width = np.abs(xscale * xsize)
        height = np.abs(yscale * ysize)

        offset = np.array([xoffset, yoffset]) + 0.5 * np.array([-width, -height])
        colors = plt.cm.jet(np.linspace(0, 1, N))
        
        fig, ax = plt.subplots(figsize=figsize)
        if not show_axis:
            ax.axis('off')
        else:
            ax.set_xlabel("[nm]")
            ax.set_ylabel("[nm]")

        if align:
            topo.spym.align()
        if plane:
            topo.spym.plane()
        if fix_zero:
            topo.spym.fixzero()

        size = round(topo.RHK_Xsize * abs(topo.RHK_Xscale) * 1e9, 3)
        ax.imshow(topo.data, extent=[0, size, 0, size], cmap=cmap)

        if not arrow:
            for (i, real_coord) in enumerate(self.coords):
                view_coord = np.array(real_coord - offset) * 1e9
                ax.plot(view_coord[0], view_coord[1], marker="o", c=colors[i])
        else:
            (x1, y1) = np.array(self.coords[0] - offset) * 1e9
            (x2, y2) = np.array(self.coords[-1] - offset) * 1e9
            ax.arrow(x1, y1, x2 - x1, y2 - y1, lw=0.1, width=0.2, length_includes_head=True, edgecolor='w', facecolor='w')

        size = round(topo.RHK_Xsize * abs(topo.RHK_Xscale) * 1e9, 3)
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

        ax.add_artist(scalebar)

        fig.tight_layout()
        return (fig, ax)


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


    def scale_data(self, scale: float):
        self.ds.data *= scale


    def get_min(self) -> float:
        return np.min(self.ds.data)


    def get_max(self) -> float:
        return np.max(self.ds.data)
    
    