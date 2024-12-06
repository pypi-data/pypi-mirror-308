import os
import matplotlib.pyplot as plt
from . import formats

def plot_waterfall(src: str,
                   figsize=(8,8), 
                   spacing=None, 
                   cmap=plt.cm.jet, 
                   show_hysteresis=False):
    _, ext = os.path.splitext(src)
    if not ext:
        raise FileNotFoundError("File source must be a valid format.")

    match ext:
        case '.sm4':
            sm4 = formats.SM4(src)
            return sm4.plot_waterfall(figsize=figsize, spacing=spacing, cmap=cmap, show_hysteresis=show_hysteresis)
        case _:
            pass