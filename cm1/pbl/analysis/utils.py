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
    # For ICT format, the number of header lines is given in the first line
    with open(ict_path_file, "r") as f:
        n_header_lines = int(f.readline().split(",")[0])

    df = pd.read_csv(ict_path_file, skiprows=n_header_lines - 1, skipinitialspace=True)
    return df[parameter2extract].astype(float).tolist()


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


def _binned_percentile(bounds, raw_bin_value, raw_param, raw_percentile):
    """
    Calculate a percentile of ``raw_param`` binned by ``raw_bin_value``.

    Bins are half-open: [bounds[n], bounds[n + 1]).

    Parameters
    ----------
    bounds : array_like
        Bin boundaries
    raw_bin_value : array_like
        Values used to assign each sample to a bin
    raw_param : array_like
        Parameter values to analyze
    raw_percentile : float
        Percentile to compute (0-100)

    Returns
    -------
    list
        Percentile values for each bin
    """
    bin_index = pd.cut(
        raw_bin_value, bins=bounds, right=False, labels=False, include_lowest=True
    )
    quantile = pd.Series(raw_param).groupby(bin_index).quantile(raw_percentile / 100)
    return quantile.reindex(range(len(bounds) - 1)).tolist()


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
    return _binned_percentile(hour_bounds, raw_hour_of_day, raw_param, raw_percentile)


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
    return _binned_percentile(height_bounds, raw_height, raw_param, raw_percentile)


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
    df = pd.DataFrame({idx: pd.Series(arr_item) for idx, arr_item in enumerate(arrs)})
    return df.mean(axis="columns").to_numpy(), df.std(axis="columns", ddof=0).to_numpy()


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
    return pd.Series(x).groupby(np.arange(len(x)) // f).mean().to_numpy()


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
        Rectangular array with shorter rows padded with NaN
    """
    df = pd.DataFrame({idx: pd.Series(row) for idx, row in enumerate(data)})
    return df.to_numpy().T
