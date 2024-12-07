##
import os
import numpy as np
from pathlib import Path
from datetime import datetime

##
from .image import ImageData
from ...readers.spym import io


def _get_prev_image(path: Path) -> ImageData:
    """
    """
    if len(path.name.split("_")) < 7:
        raise FileExistsError("No previous image found.")
    
    src_dir = path.parent
    files = [x for x in os.listdir(src_dir) if x.endswith('.sm4')]
    dates = [x.split('.')[0].split('_') for x in files]
    dates = [x[-7:] for x in dates if len(x) > 7]
    dates = [datetime(*[int(d) for d in date]) for date in dates]
    dates = list(zip(dates, range(len(dates))))
    dates_sorted, permuted_indices = list(zip(*sorted(dates)))
    file_date = path.name.split('.')[0].split('_')[-7:]  # Date of the current file
    file_date = datetime(*[int(d) for d in file_date])
    
    files = [files[i] for i in list(permuted_indices)]
    idx = dates_sorted.index(file_date) # index of the current file in the date ordered list

    while idx >= 0:
        fpath = os.path.join(src_dir, files[idx])
        sm4file = io.load(fpath)
        if 'data_vars' in sm4file.__dir__():
            if _is_topo_file(sm4file):
                return ImageData(fpath, sm4file)
        idx -= 1

    raise FileExistsError("No previous image found.")


def _get_topo_from_path(path: Path):
    sm4file = io.load(path)
    if _is_topo_file(sm4file):
        return ImageData(path, sm4file)
    raise FileExistsError(f"No topography data found at {path}")

def _is_topo_file(sm4file) -> bool:
    if 'Topography_Forward' in sm4file.data_vars:
        topography = sm4file.Topography_Forward
        if topography.data.shape[0] == topography.data.shape[1]: ### There is no full proof way to tell the difference between data that has only dIdV and data that has both image and dIdV - checking if the image is square is the closest option
            line_average = np.average(topography.data, axis=1)
            num_zeros = len(topography.data) - np.count_nonzero(line_average)
            if num_zeros == 0:
                return True
    return False