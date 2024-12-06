Python Tools for EOS-HDF4 Format
================================

Unfortunately, many important NASA datasets are still distributed as EOS-HDF4 granules. This small library may help you to avoid needing to install GDAL just to read the file. It is capable of reading an an HDF4 file (and EOS-HDF4 files, in particular) and writing out a spatial dataset using `rasterio`, based on some strict assumptions about the file-level attributes; assumptions that are usually satisfied by an EOS-HDF4 file.

The problems solved by `py4eos` include:

- Reading an EOS-HDF4 file without needing `GDAL` installed
- Figuring out the coordinate reference system (CRS) and affine transformation of an EOS-HDF4 granule
- Converting an EOS-HDF4 file to a more convenient raster format


Example Use
-----------

```python
import earthaccess
import py4eos

# Download a MOD16A3GF granule
result = earthaccess.search_data(
    short_name = 'MOD16A3GF',
    temporal = ('2014-01-01', '2014-12-31'),
    bounding_box = (-106, 42, -103, 43))
earthaccess.download(result, TEST_DIR)

# Write the file to a GeoTIFF
hdf = py4eos.read_hdf4eos(granule_mod16a3)
hdf.to_rasterio('ET_500m', 'output_file.tiff')
```


Installation
------------

The easiest way to install `py4eos` is using `mamba` (see [installation instructions](https://github.com/conda-forge/miniforge#mambaforge)) or `conda`. This is the recommended way to install `py4eos` on Windows or Mac OS X:

```sh
mamba install py4eos
```

If the HDF4, `zlib`, and `libjpeg` libraries are already installed, then you can use `pip` on any system to install `py4eos`:

```sh
pip install py4eos
```

**Installing dependencies on GNU/Linux:**

- On Ubuntu GNU/Linux: `sudo apt install python3-dev libhdf4-dev`

**Running the test suite,** from the root directory of the repository:

```sh
python -m pytest
```

**Because data has to be downloaded as part of running the tests, they may fail the first time. Try running once more.**
