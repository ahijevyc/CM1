"""
Spectral analysis plotting utilities for boundary-layer research.

This module provides functions for plotting power spectral densities and spectra.

Original source file (in patton/src):
    - plot_met_spectra.py - spectral analysis and power spectrum plots

References
----------
Adapted from Ned Patton's boundary-layer analysis software for the BL-REINV project.
"""

import matplotlib.ticker as ticker
import numpy as np


def configure_spectrum_axes(ax, fontsize="medium", label_pad=3):
    """
    Configure matplotlib axes with standard settings for spectrum plots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure
    fontsize : str, optional
        Font size for tick labels (default: 'medium')
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

    # Log scale for spectral plots
    ax.set_xscale("log")
    ax.set_yscale("log")


def add_spectrum(
    ax, frequency, power, color="black", linestyle="solid", linewidth=2.0, label=""
):
    """
    Add power spectrum to axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to plot on (should have log scales)
    frequency : array_like
        Frequency values
    power : array_like
        Power spectral density values
    color : str, optional
        Line color (default: 'black')
    linestyle : str, optional
        Line style (default: 'solid')
    linewidth : float, optional
        Line width (default: 2.0)
    label : str, optional
        Label for legend (default: '')
    """
    ax.plot(
        frequency,
        power,
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        label=label,
    )


def add_inertial_subrange(
    ax,
    freq_min,
    freq_max,
    power_at_min,
    slope=-5 / 3,
    color="gray",
    linestyle="--",
    linewidth=1.0,
    label="",
):
    """
    Add inertial subrange reference line to spectrum plot.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object with log-log scales
    freq_min : float
        Minimum frequency for reference line
    freq_max : float
        Maximum frequency for reference line
    power_at_min : float
        Power value at minimum frequency
    slope : float, optional
        Spectral slope (default: -5/3 for Kolmogorov)
    color : str, optional
        Line color (default: 'gray')
    linestyle : str, optional
        Line style (default: '--')
    linewidth : float, optional
        Line width (default: 1.0)
    label : str, optional
        Label for legend (default: '')
    """
    freq = np.array([freq_min, freq_max])
    # In log-log space: log(E) = log(E0) + slope * log(f/f0)
    log_power = np.log10(power_at_min) + slope * (np.log10(freq) - np.log10(freq_min))
    power = 10**log_power
    ax.plot(
        freq, power, color=color, linestyle=linestyle, linewidth=linewidth, label=label
    )


def configure_loglog_axes(ax, xmin=None, xmax=None, ymin=None, ymax=None):
    """
    Configure log-log axes with standard locators and formatters.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure
    xmin, xmax, ymin, ymax : float, optional
        Axis limits (default: None for auto)
    """
    # Set up major and minor locators for log scale
    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0,)))
    ax.xaxis.set_minor_locator(
        ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1)
    )
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0,)))
    ax.yaxis.set_minor_locator(
        ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1)
    )

    if xmin is not None and xmax is not None:
        ax.set_xlim([xmin, xmax])
    if ymin is not None and ymax is not None:
        ax.set_ylim([ymin, ymax])


__all__ = [
    "configure_spectrum_axes",
    "add_spectrum",
    "add_inertial_subrange",
    "configure_loglog_axes",
]
