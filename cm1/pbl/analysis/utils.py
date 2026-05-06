"""
Analysis utilities for boundary-layer research.

Utility functions for statistical analysis, data manipulation, and calculations
adapted from Ned Patton's boundary-layer analysis toolkit.
"""

import math
import numpy as np
import pandas as pd
from IPython.display import display_html


def restart_kernel():
    """Restart Jupyter kernel (for notebook environments)."""
    display_html("<script>Jupyter.notebook.kernel.restart()</script>", raw=True)


def extract_ict2(parameter2extract, ict_path_file):
    """
    Extract a parameter from an ICT format file.

    Parameters
    ----------
    parameter2extract : str
        Name of the parameter column to extract
    ict_path_file : str
        Path to the ICT format file

    Returns
    -------
    list
        Values of the extracted parameter
    """
    # Read the file
    with open(ict_path_file, "r") as f:
        ict_contents = f.readlines()

    # Find the header: for ict format, line index of header is given in the first line
    header_line_ind = -1 + int(ict_contents[0].split(",")[0])
    file_header_keyword = ict_contents[header_line_ind]
    file_header_keyword = file_header_keyword.replace(" ,", ",").replace(", ", ",")

    for i in range(len(ict_contents)):
        ict_contents_squeeze = ict_contents[i].replace(" ,", ",").replace(", ", ",")
        if ict_contents_squeeze.find(file_header_keyword) != -1:
            ict_header = ict_contents_squeeze
            ict_header_lineind = i
            break

    # Chop off header
    ict_contents = ict_contents[ict_header_lineind + 1 :]
    # Chop header into pieces
    ict_header = ict_header.split(",")
    # Get the column index for the parameter
    parameter_index = ict_header.index(parameter2extract)

    # Extract the parameter
    parameter_temp = []
    for i in range(len(ict_contents)):
        parameter_temp.append(float(ict_contents[i].split(",")[parameter_index]))

    return parameter_temp


def extract_ict2_basedate(ict_path_file):
    """
    Extract base date from ICT format file.

    Parameters
    ----------
    ict_path_file : str
        Path to the ICT format file

    Returns
    -------
    str
        Base date as string in format 'YYYY-MM-DD'
    """
    # Read the file
    with open(ict_path_file, "r") as f:
        ict_contents = f.readlines()

    # Find the base date (typically at line 6)
    basedate_lineind = 6
    basedate = ict_contents[basedate_lineind]
    basedate = basedate.replace(" ,", ",").replace(", ", ",")
    basedate_out = (
        basedate.split(",")[0]
        + "-"
        + basedate.split(",")[1]
        + "-"
        + basedate.split(",")[2]
    )

    return basedate_out


def hourly_stats(hour_bounds, raw_hour_of_day, raw_param, raw_percentile):
    """
    Calculate statistics binned by hour of day.

    Parameters
    ----------
    hour_bounds : array_like
        Hour boundaries for binning
    raw_hour_of_day : array_like
        Hour of day values
    raw_param : array_like
        Parameter values to analyze
    raw_percentile : float
        Percentile to compute (0-100)

    Returns
    -------
    list
        Percentile values for each hourly bin
    """
    stat_out = []
    for n in range(len(hour_bounds) - 1):
        raw_param_temp = raw_param.copy()
        raw_param_temp = np.where(
            (raw_hour_of_day >= hour_bounds[n])
            & (raw_hour_of_day < hour_bounds[n + 1]),
            raw_param_temp,
            np.nan,
        )
        stat_out.append(np.nanpercentile(raw_param_temp, raw_percentile))

    return stat_out


def vertical_stats(height_bounds, raw_height, raw_param, raw_percentile):
    """
    Calculate statistics binned by height.

    Parameters
    ----------
    height_bounds : array_like
        Height boundaries for binning (m)
    raw_height : array_like
        Height values (m)
    raw_param : array_like
        Parameter values to analyze
    raw_percentile : float
        Percentile to compute (0-100)

    Returns
    -------
    list
        Percentile values for each height bin
    """
    stat_out = []
    for n in range(len(height_bounds) - 1):
        raw_param_temp = raw_param.copy()
        raw_param_temp = np.where(
            (raw_height >= height_bounds[n]) & (raw_height < height_bounds[n + 1]),
            raw_param_temp,
            np.nan,
        )
        stat_out.append(np.nanpercentile(raw_param_temp, raw_percentile))

    return stat_out


def rolling_average(a, n):
    """
    Calculate rolling/moving average using pandas.

    Parameters
    ----------
    a : array_like
        Input data
    n : int
        Window size for rolling average

    Returns
    -------
    np.ndarray
        Rolling average values

    References
    ----------
    https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-numpy-scipy
    """
    return pd.DataFrame(a).rolling(n, center=True, min_periods=1).mean().to_numpy()


def round_up(n, decimals=0):
    """
    Round a number up to the nearest specified decimal place.

    Parameters
    ----------
    n : float
        Number to round
    decimals : int, optional
        Number of decimal places (default: 0)

    Returns
    -------
    float
        Rounded value
    """
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    """
    Round a number down to the nearest specified decimal place.

    Parameters
    ----------
    n : float
        Number to round
    decimals : int, optional
        Number of decimal places (default: 0)

    Returns
    -------
    float
        Rounded value
    """
    multiplier = 10**decimals
    return math.floor(n * multiplier) / multiplier


def tolerant_mean(arrs):
    """
    Calculate mean and std of arrays with different lengths.

    Handles arrays of different lengths by masking shorter arrays.

    Parameters
    ----------
    arrs : list of array_like
        List of arrays with potentially different lengths

    Returns
    -------
    tuple
        (mean, std) computed across arrays, ignoring masked values
    """
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens), len(arrs)))
    arr.mask = True
    for idx, arr_item in enumerate(arrs):
        arr[: len(arr_item), idx] = arr_item

    return arr.mean(axis=-1), arr.std(axis=-1)


def down_sample(x, f=7):
    """
    Down-sample array by averaging over chunks.

    Parameters
    ----------
    x : array_like
        Input data to down-sample
    f : int, optional
        Down-sampling factor (default: 7)

    Returns
    -------
    np.ndarray
        Down-sampled data
    """
    # Pad to a multiple of f, use nan for padding
    xp = np.r_[x, np.nan + np.zeros((-len(x) % f,))]
    # Reshape and take mean of chunks
    return np.nanmean(xp.reshape(-1, f), axis=-1)


def numpy_fillna(data):
    """
    Fill jagged arrays with NaN to create rectangular array.

    Parameters
    ----------
    data : list of array_like
        List of arrays with different lengths

    Returns
    -------
    np.ndarray
        Rectangular array with shorter rows padded with zeros
    """
    # Get lengths of each row
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:, None]

    # Setup output array and fill with data
    out = np.zeros(mask.shape, dtype=data[0].dtype if data else float)
    out[mask] = np.concatenate(data)

    return out


__all__ = [
    "restart_kernel",
    "extract_ict2",
    "extract_ict2_basedate",
    "hourly_stats",
    "vertical_stats",
    "rolling_average",
    "round_up",
    "round_down",
    "tolerant_mean",
    "down_sample",
    "numpy_fillna",
]
