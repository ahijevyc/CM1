"""
Data handling and I/O utilities for boundary-layer datasets.

This module provides functions for reading, writing, and manipulating boundary-layer
data from various model and observational sources.

References
----------
Adapted from Ned Patton's data reading utilities for the BL-REINV project.
Data sources include:
    - LES models (NCAR-LES, WRF-LES, DALES, MicroHH, CM1, MPAS)
    - SCM models (WRF-SCM, SCAM, Somcrus)
    - Observations (ground-based, airborne, LIDAR)
"""

import numpy as np


def normalize_coordinate_names(ds, dimension_map=None):
    """
    Standardize coordinate names across different datasets.

    Different models use different naming conventions for coordinates.
    This function maps them to standard names.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset
    dimension_map : dict, optional
        Mapping from current names to standard names (default: None)

    Returns
    -------
    xr.Dataset
        Dataset with standardized coordinate names

    Examples
    --------
    Standard coordinate names:
        - 'z' or 'height' - vertical coordinate (m)
        - 'time' - time coordinate
        - 'x', 'y' - horizontal coordinates
    """
    if dimension_map is None:
        dimension_map = {
            "zw": "height_w",
            "zm": "height_m",
            "zc": "height_c",
            "lev": "height",
            "level": "height",
            "z": "height",
        }

    return ds.rename(dimension_map)


def interpolate_to_common_grid(datasets, coordinate="height"):
    """
    Interpolate multiple datasets to a common coordinate grid.

    Useful for comparing fields from different models that use
    different vertical discretizations.

    Parameters
    ----------
    datasets : list of xr.Dataset
        Input datasets to interpolate
    coordinate : str, optional
        Coordinate name to use for interpolation (default: 'height')

    Returns
    -------
    list of xr.Dataset
        Datasets interpolated to common grid
    """
    # Find coordinate range that encompasses all datasets
    coord_mins = [ds[coordinate].min().values for ds in datasets]
    coord_maxs = [ds[coordinate].max().values for ds in datasets]

    common_min = np.max(coord_mins)
    common_max = np.min(coord_maxs)

    # Create common grid
    common_grid = np.linspace(common_min, common_max, 100)

    # Interpolate each dataset
    interpolated = []
    for ds in datasets:
        interp_ds = ds.interp({coordinate: common_grid})
        interpolated.append(interp_ds)

    return interpolated


def extract_profile_at_time(ds, time_index=0, variables=None):
    """
    Extract a vertical profile at a specific time.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset
    time_index : int, optional
        Time index to extract (default: 0)
    variables : list of str, optional
        Variables to extract (default: all)

    Returns
    -------
    dict
        Dictionary with extracted profile data
    """
    if variables is None:
        variables = list(ds.data_vars.keys())

    profile = {}
    for var in variables:
        if var in ds:
            profile[var] = ds[var].isel(time=time_index).values

    # Include coordinate
    if "height" in ds.coords:
        profile["height"] = ds["height"].values

    return profile


def calculate_statistics_at_time(ds, time_index=0, percentiles=None):
    """
    Calculate statistics at a given time across space.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset
    time_index : int, optional
        Time index to analyze (default: 0)
    percentiles : list of float, optional
        Percentiles to compute (default: [25, 50, 75])

    Returns
    -------
    dict
        Dictionary with statistics for each variable
    """
    if percentiles is None:
        percentiles = [25, 50, 75]

    stats = {}

    for var in ds.data_vars:
        data = ds[var].isel(time=time_index).values
        stats[var] = {
            "mean": np.nanmean(data),
            "std": np.nanstd(data),
            "min": np.nanmin(data),
            "max": np.nanmax(data),
            "percentiles": np.nanpercentile(data, percentiles),
        }

    return stats


__all__ = [
    "normalize_coordinate_names",
    "interpolate_to_common_grid",
    "extract_profile_at_time",
    "calculate_statistics_at_time",
]
