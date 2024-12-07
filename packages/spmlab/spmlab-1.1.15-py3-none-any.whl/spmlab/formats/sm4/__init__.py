## External packages
from ...spym.io import load

## Internal packages
from ._abstract import AbstractSM4Data
from .image import ImageData
from .sts import STSData
from .iz import IZData

def read(src_path: str) -> AbstractSM4Data:
    sm4 = load(src_path)
    if sm4 is None:
        raise FileExistsError("There was a problem loading the file. Ensure that the full path to the file is correct.")
    
    if 'Current' in sm4.data_vars:
        match sm4.Current.RHK_LineTypeName:
            case 'RHK_LINE_IV_SPECTRUM':
                return STSData(src_path, sm4)
            case 'RHK_LINE_IZ_SPECTRUM':
                return IZData(src_path, sm4)
    elif 'Topography_Forward' in sm4.data_vars:
        return ImageData(src_path, sm4)
