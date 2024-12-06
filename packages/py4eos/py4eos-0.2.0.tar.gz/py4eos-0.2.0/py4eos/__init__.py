import numpy as np
import h5py
import rasterio as rio
from functools import cached_property
from affine import Affine
from pyhdf.SD import SD, SDC
from py4eos.srs import SRS

__version__ = '0.2.0'

PLATFORMS_SUPPORTED = ('MODIS', 'VIIRS')

class HDF4EOS(object):
    '''
    Represents an EOS-HDF4 granule.

    Parameters
    ----------
    dataset : pyhdf.SD
        A pyhdf Scientific Dataset (SD) instance
    platform : str
        The name of the data platform the SD originates from; currently
        limited to one of: ("MODIS",)
    '''

    GRID_DIM_TO_RES = { # Mapping of grid dimensions to spatial resolution
        'MODIS': {
            2400: 500 # 2400 x 2400 pixels == 500 meters
        },
        'VIIRS': {
            2400: 500
        }
    }

    def __init__(self, dataset, platform = 'MODIS'):
        self.dataset = dataset
        self.platform = platform
        if self.platform not in PLATFORMS_SUPPORTED:
            raise NotImplementedError(f'No support for the platform "{platform}"')

    @cached_property
    def attrs(self):
        if self.platform == 'MODIS':
            meta = self.dataset.attributes()['StructMetadata.0']
        elif self.platform == 'VIIRS':
            meta = self.dataset['HDFEOS INFORMATION/StructMetadata.0'][()]
            if hasattr(meta, 'decode'):
                meta = meta.decode('utf-8')
        attrs = [line.split('=') for line in meta.replace('\t', '').split('\n')]
        # TODO This is quick and dirty; there are multiple nested
        #   attributes with similar names that will be overwritten when
        #   converitng to a dictionary; it's assumed they're not important
        attrs = list(filter(lambda x: len(x) == 2, attrs))
        return dict(attrs)

    @cached_property
    def crs(self):
        if self.platform in ('MODIS', 'VIIRS'):
            wkt = SRS[6842]
        return wkt

    @cached_property
    def geotransform(self):
        # TODO Will need to generalize these two attribute checks when support
        #   beyond MODIS is added
        if self.platform in ('MODIS', 'VIIRS'):
            if 'UpperLeftPointMtrs' not in self.attrs.keys():
                raise KeyError('Could not determine upper-left corner coordinates; on one of the following is missing from the attributes: "UpperLeftPointMtrs"')
            if 'XDim' not in self.attrs.keys() or 'YDim' not in self.attrs.keys():
                raise KeyError('Could not determine spatial resolution; "XDim" and "YDim" missing from attributes')
        ul = list(map(float, self.attrs['UpperLeftPointMtrs'].strip('()').split(',')))
        ul_x, ul_y = ul
        xdim = int(self.attrs['XDim'])
        xres = self.GRID_DIM_TO_RES[self.platform][xdim]
        return (ul_x, xres, 0, ul_y, 0, -xres)

    @property
    def subdatasets(self):
        return self.dataset.datasets() # Chain pyhdf.SD.SD.datasets()

    @cached_property
    def transform(self):
        return Affine.from_gdal(*self.geotransform)

    def get(self, field, dtype = 'float32', scale_and_offset = False):
        '''
        Returns the array data for the subdataset (field) named.

        Parameters
        ----------
        field : str
            Name of the subdataset to access
        dtype : str
            Name of a NumPy data type, e.g., "float32" for `numpy.float32`
            (Default)
        scale_and_offset: bool
            True to apply the scale and offset, if specified, in the dataset
            (Default: False)

        Returns
        -------
        numpy.ndarray
        '''
        dtype = getattr(np, dtype) # Convert from string to NumPy dtype
        if isinstance(self.dataset, h5py.File):
            ds = self.dataset[field]
            attrs = self.dataset[field].attrs
        else:
            ds = self.dataset.select(field)
            attrs = self.dataset.select(field).attributes()
        scale = 1.0
        offset = 0.0
        if scale_and_offset:
            if 'scale_factor' in attrs.keys() and 'add_offset' in attrs.keys():
                scale = float(attrs['scale_factor'])
                offset = float(attrs['add_offset'])
        return (offset + ds[:] * scale).astype(dtype)

    def to_rasterio(
            self, field, filename, driver = 'GTiff', dtype = 'float32',
            scale_and_offset = False):
        '''
        Parameters
        ----------
        field : str
            Name of the subdataset to write to the output data file
        filename : str
            File path for the output file
        driver : str
            Name of the file driver; defaults to "GTiff" for GeoTIFF output
        dtype : str
            Name of a NumPy data type, e.g., "float32" for `numpy.float32`
            (Default)
        scale_and_offset: bool
            True to apply the scale and offset, if specified, in the dataset
            (Default: False)
        '''
        arr = self.get(field, dtype, scale_and_offset)
        rows, cols = arr.shape
        rast = rio.open(
            filename, 'w+', driver = driver, height = rows, width = cols,
            count = 1, dtype = getattr(np, dtype), crs = self.crs,
            transform = self.transform)
        rast.write(arr, 1)


def read_hdf4eos(filename, platform = None, mode = 'r'):
    '''
    Read an EOS-HDF4 dataset and return an `HDF4EOS` object.

    Parameters
    ----------
    filename : str
        File path for the input EOS-HDF4 file
    platform : str
        The name of the data platform the SD originates from; currently
        limited to one of: ("MODIS",)
    mode : str
        The file mode, should be "r" (read) or "w" ("write") (Default: "r")

    Returns
    -------
    HDF4EOS
    '''
    if platform is None or platform == 'MODIS':
        mode = SDC.WRITE if mode == 'w' else SDC.READ
        sd = SD(filename, mode = mode)
        dataset = HDF4EOS(sd)
    elif platform == 'VIIRS':
        sd = h5py.File(filename, mode)
        dataset = HDF4EOS(sd, platform = platform)
    return dataset


if __name__ == '__main__':
    import fire
    fire.Fire(read_hdf4eos)
