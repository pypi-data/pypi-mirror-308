"""
Extracts the data from the .har file and saves it as .npy files.
"""

import os
from HARPY.harpy import HarFileObj
import xarray as xr
import logging
import gtap_mrio.mrio_builder as mrio_builder

log = logging.getLogger(__name__)

def extract_gtap(
        source = "",
        destination = "",
        files = "all",
        name = "gtap",
        build_io = False
):
    """
    Extract GTAP data from .har files and save it as .nc file.

    Parameters
    ----------
    source : str, optional
        Location of the source files, by default the current directory
    destination : str, optional
        Where to save the files, by default the current directory
    files : list, optional
        List of files to extract, by default, all files in the source directory
    name : str, optional
        Name under which the files are saved, by default "gtap"
    build_io : bool, optional
        Whether to build the input-output table, by default False

    Raises
    ------
    NotADirectoryError
        Exception raised when the source directory does not exist
    FileNotFoundError
        Exception raised when the destination directory does not contain any .har files
        If only some files are missing, a warning is issued but the extraction continues
    """
    #Check source path
    if not os.path.exists(source):
        log.error(f"{os.path.abspath(source)} does not exist.")
        raise NotADirectoryError(f"{os.path.abspath(source)} does not exist.")
    
    #Check destination path
    if not os.path.exists(destination):
        log.info(f"{os.path.abspath(destination)} does not exist. Creating directory.")
        os.makedirs(destination)

    log.info(f"Extracting GTAP data from {os.path.abspath(source)} to {os.path.abspath(destination)}")
    
    #List available har files
    har_files = [f for f in os.listdir(source) if f.endswith(".har")]
    if len(har_files) == 0:
        log.error(f"No .har files found in {os.path.abspath(source)}")
        raise FileNotFoundError(f"No .har files found in {os.path.abspath(source)}")
    log.info(f"Found {len(har_files)} .har files in {os.path.abspath(source)}")

    if isinstance(files, str) and files == "all":
        files = har_files
    
    ds = xr.Dataset()
    for file in files:
        if file not in har_files:
            log.warning(f"{file} not found in {os.path.abspath(source)}")
            continue
        log.info(f" Extracting {file}")
        data = HarFileObj(os.path.join(source, file))
        variables = data.getHeaderArrayNames()
        for variable in variables:
            log.info(f"     Extracting {variable}")
            ds = convert_variable(data, variable, ds)

    #Save dataset
    log.info(f"Saving {name}.nc")
    ds.to_netcdf(os.path.join(destination, f"{name}.nc"))
    if build_io:
        log.info("Building input-output table")
        mrio = mrio_builder.build_io(ds)
        log.info(f"Saving {name}_mrio.nc")
        mrio.save(os.path.join(destination, f"{name}_mrio.nc"))

def convert_variable(file, variable, ds):
    """
    Convert a variable from a .har file to a xarray DataArray.

    Data descriptor variables are stored as attributes of the dataset.

    Parameters
    ----------
    file : harpy.HarFileObj
        Representation of the .har file
    variable : str
        Name of the variable to extract
    ds : xarray.Dataset
        Dataset to which the variable is added

    Returns
    -------
    ds : xarray.Dataset
        Updated dataset
    """
    data = file[variable]
    coords = dict()
    dims = []
    for dim in data.sets.dims:
        if dim.name is None:
            #Intercepts descriptive variables
            log.info(f"     {variable} is a descriptive variable")
            ds.attrs[variable] = str(data.array)
            return ds
        dims.append(dim.name)
        coords[dim.name] = dim.dim_desc
    ds[variable] = xr.DataArray(
        data.array,
        coords = coords,
        dims = dims,
        attrs = {
            "long_name": data.long_name,
            "name" : variable
        }
    )
    return ds
