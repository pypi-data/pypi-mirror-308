# gtap_extractor

GTAP is a licensed database for international economics.
It is widely used for calibrating Computable General Equilibrium (CGE).
GTAP is distributed as unusual .har files, usable with the proprietary GTAPAgg software.
This package aims at simplifying the access to GTAP data, by transferring GTAP data into the standard netCDF data format.

---

## Installation

You can install the package by typing `pip install gtap-extractor`

## Usage

The *extract_gtap()* method takes three optional arguments:

**source** *(path-like)*
   : Path to the raw GTAP .har files.
   : You will find these files in your GTAP installation.
   : By default, the current working directory.

**name** *str*
    : Name under which the resulting .nc file is stored


**destination** *(path-like)*
   : Path where the netCDF file will be saved.
   : By default, the current working directory.

**files** *(list of str)*
   : List of GTAP files to be extracted.
   : By default, all GTAP files are extracted.

**build_mrio** *(bool)*
    : If True, GTAP data are converted into a simple MRIO table, in basic prices.


>The built table is saved under <name>_mrio.nc.
>
>The table consists in three parts:
> - The inter-industry matrix t, built from the VDFB and VMFB variables.
> - The final demand matrix y, built from VMPB, VDPB, VMGB, VDGB, VMIB, VDIB.
> - The value added matrix va, built from EVFB and VTWR.
>
>The construction of t and y relies on the import proportionality assumption: trade shares for each imported good are kept constant across imported sectors.
>
>As imports (VMSB) and exports (VXSB) diverge, trade shares are computed as the arithmetic average of both.
>
>These trade shares are used to ventilate intermediate and final imports.
>
> The value added array includes:
> - Primary endownments (EVFB)
> - The sum of margins and export tariffs (VTWR + XTRV)
> - Net output taxes and subsidies, estimated as the residual value to balance the table.
    


---

## Dependencies 

The package builds on the [HARPY](https://github.com/GEMPACKsoftware/HARPY), [xarray](https://xarray.pydata.org/en/v2024.07.0/index.html), [netcdf4](http://unidata.github.io/netcdf4-python/) and [MRIO_toolbox](https://gitlab.pik-potsdam.de/beaufils/mrio-toolbox) libraries.

Note that the HARPY version on pip is outdated.
Instead, you can clone the HARPY repository directly using the following command in your terminal:

git clone https://github.com/GEMPACKsoftware/HARPY
