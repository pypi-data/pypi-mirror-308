'''
Tests for the various file formats supported:

    VNP15A2H 8-day fPAR and LAI:
        https://dx.doi.org/10.5067/VIIRS/VNP15A2H.002
    MOD15A2H 8-day fPAR and LAI:
        https://dx.doi.org/10.5067/MODIS/MOD15A2H.061
    MOD16A2 8-day Evapotranspiration (ET):
        https://dx.doi.org/10.5067/MODIS/MOD16A2.061
    MOD16A2 Gap-Filled 8-day ET:
        https://dx.doi.org/10.5067/MODIS/MOD16A2GF.061
    MOD16A3 Annual Evapotranspiration (ET):
        https://dx.doi.org/10.5067/MODIS/MOD16A3.061
    MOD16A3GF Gap-Filled Annual ET:
        https://dx.doi.org/10.5067/MODIS/MOD16A3GF.061
'''

import glob
import os
import numpy as np
import pytest
import earthaccess
import rasterio as rio
import py4eos
from py4eos import read_hdf4eos

TEST_DIR = os.path.join(os.path.dirname(py4eos.__file__), 'tests')

@pytest.fixture
def granule_vnp15a2h():
    'VNP15A2H 8-day fPAR and LAI'
    file_list = glob.glob(f'{TEST_DIR}/VNP15A2H.*.h5' )
    if len(file_list) == 0:
        results = earthaccess.search_data(
            short_name = 'VNP15A2H',
            temporal = ('2020-07-01', '2020-07-01'),
            bounding_box = (-106, 42, -103, 43))
        earthaccess.download(results, TEST_DIR)
        return f'{TEST_DIR}/{results[0]["meta"]["native-id"]}'
    filename = file_list.pop()
    return filename


@pytest.fixture
def granule_mod15a2h():
    'MOD15A2H 8-day fPAR and LAI'
    file_list = glob.glob(f'{TEST_DIR}/MOD15A2H.*.hdf' )
    if len(file_list) == 0:
        results = earthaccess.search_data(
            short_name = 'MOD15A2H',
            temporal = ('2020-07-01', '2020-07-01'),
            bounding_box = (-106, 42, -103, 43))
        earthaccess.download(results, TEST_DIR)
        return f'{TEST_DIR}/{results[0]["meta"]["native-id"]}'
    filename = file_list.pop()
    return filename


@pytest.fixture
def granule_mod16a2():
    'MOD16A2(GF) 8-day Evapotranspiration'
    file_list = glob.glob(f'{TEST_DIR}/MOD16A2*.*.hdf' )
    if len(file_list) == 0:
        results = earthaccess.search_data(
            short_name = 'MOD16A2GF',
            temporal = ('2018-06-01', '2018-06-01'),
            bounding_box = (-106, 42, -103, 43))
        earthaccess.download(results, TEST_DIR)
        return f'{TEST_DIR}/{results[0]["meta"]["native-id"]}'
    filename = file_list.pop()
    return filename


@pytest.fixture
def granule_mod16a3():
    'MOD16A3(GF) Annual Evapotranspiration'
    file_list = glob.glob(f'{TEST_DIR}/MOD16A3*.*.hdf' )
    if len(file_list) == 0:
        results = earthaccess.search_data(
            short_name = 'MOD16A3GF',
            temporal = ('2014-01-01', '2014-12-31'),
            bounding_box = (-106, 42, -103, 43))
        earthaccess.download(results, TEST_DIR)
        return f'{TEST_DIR}/{results[0]["meta"]["native-id"]}'
    filename = file_list.pop()
    return filename


def test_read_vnp15a2h(granule_vnp15a2h):
    '''
    Tests that a VNP15A2H granule can be read and handled.
    '''
    hdf = read_hdf4eos(granule_vnp15a2h, platform = 'VIIRS')
    assert hdf.transform.to_gdal() == hdf.geotransform
    assert hdf.transform.to_gdal() == (-8895604.157333, 500.0, 0.0, 5559752.598333, 0.0, -500.0)
    assert hdf.get('HDFEOS/GRIDS/VNP_Grid_VNP15A2H/Data Fields/Fpar').shape == (2400, 2400)


def test_read_mod15a2h(granule_mod15a2h):
    '''
    Tests that a MOD15A2H granule can be read and handled.
    '''
    hdf = read_hdf4eos(granule_mod15a2h)
    assert hdf.transform.to_gdal() == hdf.geotransform
    assert hdf.transform.to_gdal() == (-8895604.157333, 500.0, 0.0, 5559752.598333, 0.0, -500.0)
    assert hdf.get('Lai_500m').shape == (2400, 2400)


def test_write_mod15a2h(granule_mod15a2h):
    '''
    Tests that a MOD15A2H granule can be written to a GeoTIFF.
    '''
    hdf = read_hdf4eos(granule_mod15a2h)
    hdf.to_rasterio('Fpar_500m', f'{TEST_DIR}/temp.tiff')
    # Real test is that this doesn't fail
    ds = rio.open(f'{TEST_DIR}/temp.tiff')
    assert ds.transform == hdf.transform


def test_read_mod16a2(granule_mod16a2):
    '''
    Tests that a MOD16A2 granule can be read and handled.
    '''
    hdf = read_hdf4eos(granule_mod16a2)
    assert hdf.transform.to_gdal() == hdf.geotransform
    assert hdf.transform.to_gdal() == (-8895604.157333, 500.0, 0.0, 5559752.598333, 0.0, -500.0)
    arr = hdf.get('ET_500m', dtype = 'int32')
    assert arr.shape == (2400, 2400)
    assert arr.dtype == np.int32


def test_write_mod16a2(granule_mod16a2):
    '''
    Tests that a MOD16A2 granule can be written to a GeoTIFF.
    '''
    hdf = read_hdf4eos(granule_mod16a2)
    hdf.to_rasterio('ET_500m', f'{TEST_DIR}/temp.tiff')
    # Real test is that this doesn't fail
    ds = rio.open(f'{TEST_DIR}/temp.tiff')
    assert ds.transform == hdf.transform


def test_read_mod16a3(granule_mod16a3):
    '''
    Tests that a MOD16A3 granule can be read and handled.
    '''
    hdf = read_hdf4eos(granule_mod16a3)
    assert hdf.transform.to_gdal() == hdf.geotransform
    assert hdf.transform.to_gdal() == (-8895604.157333, 500.0, 0.0, 5559752.598333, 0.0, -500.0)
    arr = hdf.get('ET_500m', dtype = 'int32')
    assert arr.shape == (2400, 2400)
    assert arr.dtype == np.int32


def test_write_mod16a3(granule_mod16a3):
    '''
    Tests that a MOD16A3 granule can be written to a GeoTIFF.
    '''
    hdf = read_hdf4eos(granule_mod16a3)
    hdf.to_rasterio('ET_500m', f'{TEST_DIR}/temp.tiff')
    # Real test is that this doesn't fail
    ds = rio.open(f'{TEST_DIR}/temp.tiff')
    assert ds.transform == hdf.transform
