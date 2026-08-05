"""
Time series plotting utilities for boundary-layer analysis.

This module provides functions for plotting time series of atmospheric variables.

Original source file (in patton/src):
    - plot_met_timeseries.py - time series plots with model and observation data

References
----------
Adapted from Ned Patton's boundary-layer analysis software for the BL-REINV project.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dates


def configure_timeseries_axes(ax, fontsize="large", label_pad=3):
    """
    Configure matplotlib axes with standard settings for time series plots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure
    fontsize : str, optional
        Font size for tick labels (default: 'large')
    label_pad : float, optional
        Padding for axis labels (default: 3)
    """
    ax.tick_params(
        axis="both", which="both", direction="out", labelsize=fontsize, pad=label_pad
    )
    ax.tick_params(axis="both", which="major", length=5.5, width=1)
    ax.tick_params(axis="both", which="minor", length=3.0, width=0.7)
    ax.tick_params(axis="x", which="both", top=True)
    ax.tick_params(axis="y", which="both", right=True)


def add_timeseries_data(
    ax, time, data, color="black", linestyle="solid", linewidth=1.5, label=""
):
    """
    Add time series data to an axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to plot on
    time : array_like
        Time values (can be datetime objects or numeric)
    data : array_like
        Data values at each time
    color : str, optional
        Line color (default: 'black')
    linestyle : str, optional
        Line style (default: 'solid')
    linewidth : float, optional
        Line width (default: 1.5)
    label : str, optional
        Label for legend (default: '')
    """
    ax.plot(
        time, data, color=color, linestyle=linestyle, linewidth=linewidth, label=label
    )


def add_uncertainty_band(
    ax, time, mean, lower, upper, color="gray", alpha=0.3, label=""
):
    """
    Add shaded uncertainty band to time series plot.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to plot on
    time : array_like
        Time values
    mean : array_like
        Mean values
    lower : array_like
        Lower uncertainty bound
    upper : array_like
        Upper uncertainty bound
    color : str, optional
        Color for the band (default: 'gray')
    alpha : float, optional
        Transparency (default: 0.3)
    label : str, optional
        Label for legend (default: '')
    """
    ax.fill_between(
        time, lower, upper, facecolor=color, alpha=alpha, edgecolor=color, label=label
    )
    ax.plot(time, mean, color=color, linestyle="solid", linewidth=1.5)


def format_timeseries_xaxis(ax, time_format="%H:%M", locator=None):
    """
    Format time axis with readable date/time labels.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object with time on x-axis
    time_format : str, optional
        Format string for time labels (default: '%H:%M')
    locator : matplotlib.ticker.Locator, optional
        Locator for tick positions (default: auto)
    """
    ax.xaxis.set_major_formatter(dates.DateFormatter(time_format))
    if locator is not None:
        ax.xaxis.set_major_locator(locator)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
