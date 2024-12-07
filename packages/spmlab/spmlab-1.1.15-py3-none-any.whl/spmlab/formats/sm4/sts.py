import numpy as np
import matplotlib.pyplot as plt
from xarray import Dataset

from ._abstract import SpectralData

class STSData(SpectralData):
    """
    A class to handle Scanning Tunneling Spectroscopy (STS) data, extending from the `SpectralData` base class.
    
    This class provides methods for processing and visualizing STS data, specifically creating a waterfall plot
    of the Local Density of States (LDOS) from the raw data.

    Attributes:
        ldos (Dataset): The Local Density of States (LIA_Current) dataset.
        coords (list): A list of unique coordinates derived from the `RHK_SpecDrift_Xcoord` and `RHK_SpecDrift_Ycoord` attributes.
        
    Methods:
        __init__(src: str, raw: Dataset): Initializes the STSData object with the source and raw data.
        waterfall(figsize=(8, 8), spacing=None, cmap=plt.cm.jet): Generates a waterfall plot of the LDOS data.
    """
    def __init__(self, src: str, raw: Dataset):
        """
        Initializes the STSData object by extracting the required datasets and coordinates.

        Args:
            src (str): The source or identifier of the data.
            raw (Dataset): The raw data (likely a NetCDF or HDF5 Dataset) containing the LIA_Current and other attributes.
        
        Attributes:
            ldos (Dataset): The LIA_Current dataset, representing the Local Density of States.
            coords (list): A list of unique coordinates obtained from the `RHK_SpecDrift_Xcoord` and `RHK_SpecDrift_Ycoord`.
        """
        super().__init__(src, raw)
        self.ldos = self.raw.LIA_Current
        self.coords = self.get_unique_coords(zip(self.ldos.RHK_SpecDrift_Xcoord, self.ldos.RHK_SpecDrift_Ycoord))

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

        xsize = self.ldos.RHK_Xsize
        total = self.ldos.RHK_Ysize
        repetitions = total//N
        x = self.ldos.LIA_Current_x.data * 1e3
        ldos_ave = self.ldos.data.reshape(xsize, N, repetitions).mean(axis=2).T

        ## Plot
        if spacing is None:
            spacing = np.max(ldos_ave) / 10
        waterfall_offset = np.flip([i * spacing for i in range(N)])
        colors = cmap(np.linspace(0, 1, N))

        fig, ax = plt.subplots(figsize=figsize)
        for (i, dIdV) in enumerate(ldos_ave):
            ax.plot(x, dIdV + waterfall_offset[i], c=colors[i])

        fig.tight_layout()
        return (fig, ax)

    def spectral_line_cut(self, 
                        aspect=None, 
                        norm=None, 
                        cmap='jet', 
                        color_bar=True, 
                        vmax=None,
                        clip_max=None,
                        clip_min=None,
                        fontsize=None):
        """
        Plot the Local Density of States (LDOS) along a line as a 2d image.

        This method visualizes the LDOS data in the form of a 2D image, showing the variation in the spectral data 
        along a line between the first and last coordinate points. It can also normalize, clip, and apply colormap 
        adjustments to the data.

        Args:
            aspect (float or None): The aspect ratio of the plot. If `None`, the aspect ratio is automatically set 
                                    based on the voltage range and the length of the line cut.
            norm (matplotlib.colors.Normalize or None): Normalization for the colormap scaling. If `None`, no normalization is applied.
            cmap (str or matplotlib.colors.Colormap): The colormap to be used for displaying the data (default is 'jet').
            color_bar (bool): If `True`, a color bar will be displayed alongside the image (default is `True`).
            vmax (float or None): The maximum value for the colormap. If `None`, the maximum value in the data is used.
            clip_max (float or None): If provided, values above this threshold will be clipped to `clip_max`.
            clip_min (float or None): If provided, values below this threshold will be clipped to `clip_min`.
            fontsize (int or None): The font size for axis labels. If `None`, the default font size is used.

        Returns:
            tuple: A tuple containing the figure (`fig`), axes (`ax`), and the color bar (`cb`) (if `color_bar=True`).

        Raises:
            ValueError: If no STS data is found (i.e., if the coordinates list is empty).
        """
        N = len(self.coords)
        if N == 0:
            print("No STS data found.")
            return

        xsize = self.ldos.RHK_Xsize
        total = self.ldos.RHK_Ysize
        repetitions = total//N
        x = self.ldos.LIA_Current_x.data * 1e3
        ldos_ave = self.ldos.data.reshape(xsize, N, repetitions).mean(axis=2).T

        fig, ax = plt.subplots(figsize=(16,7))

        line_cut = (self.coords[-1][0] - self.coords[0][0], self.coords[-1][1] - self.coords[0][1])
        line_length = np.sqrt(line_cut[0]**2 + line_cut[1]**2) * 1e9

        if aspect is None:
            aspect = abs(x[-1] - x[0]) / line_length

        if clip_max:
            ldos_ave = ldos_ave.clip(None, clip_max)
        if clip_min:
            ldos_ave = ldos_ave.clip(clip_min, None)

        img = ax.imshow(ldos_ave, aspect=aspect, extent=[x[0], x[-1], 0, line_length], norm=norm, cmap=cmap, vmax=vmax)

        ax.set_yticks(np.linspace(line_length, 0, 10))
        ax.set_yticklabels(map(lambda x: "%.2f" % x, np.linspace(line_length, 0, 10)))

        ax.set_xlabel("Voltage (mV)", fontsize=fontsize)
        ax.set_ylabel("Distance (nm)", fontsize=fontsize)

        cb = None
        if color_bar:
            cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
            cb = fig.colorbar(img, cax=cax)
        
        return (fig, ax, cb)

    def scale_data(self, scale: float):
        self.ldos.data *= scale

    def get_min(self) -> float:
        return np.min(self.ldos.data)
    
    def get_max(self) -> float:
        return np.max(self.ldos.data)
    
    