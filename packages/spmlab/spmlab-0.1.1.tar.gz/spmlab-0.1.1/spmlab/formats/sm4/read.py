## Internal packages
from ...readers.spym import io
from .image import ImageData
from .sts import STSData
from .iz import IZData

def read(src_path: str):
    sm4file = io.load(src_path)
    if sm4file is None:
        raise FileExistsError("There was a problem loading the file. Ensure that the full path to the file is correct.")
    
    if 'Current' in sm4file.data_vars:
        match sm4file.Current.RHK_LineTypeName:
            case 'RHK_LINE_IV_SPECTRUM':
                return STSData(src_path, sm4file)
            case 'RHK_LINE_IZ_SPECTRUM':
                return IZData(src_path, sm4file)
    elif 'Topography_Forward' in sm4file.data_vars:
        return ImageData(src_path, sm4file)