"""
Hovmöller diagram plotting utilities for boundary-layer research.

Hovmöller diagrams show space-time evolution of fields (typically height vs time
or horizontal position vs time).

Original source file (in patton/src):
    - plot_met_hov+prof.py - Hovmöller diagrams with profiles

References
----------
Adapted from Ned Patton's boundary-layer analysis software for the BL-REINV project.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np


def create_hovmoeller_plot(
    time,
    height,
    data,
    figsize=(12, 6),
    cmap="RdBu_r",
    vmin=None,
    vmax=None,
    title="",
    xlabel="",
    ylabel="",
):
    """
    Create a Hovmöller diagram showing field evolution in time and height.

    Parameters
    ----------
    time : array_like
        Time values (can be datetime objects or numeric)
    height : array_like
        Height values (m)
    data : 2D array
        Data values with shape (len(time), len(height))
    figsize : tuple, optional
        Figure size (default: (12, 6))
    cmap : str, optional
        Colormap name (default: 'RdBu_r')
    vmin, vmax : float, optional
        Color scale limits (default: auto)
    title : str, optional
        Plot title
    xlabel : str, optional
        X-axis label
    ylabel : str, optional
        Y-axis label

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    ax : matplotlib.axes.Axes
        Axes object
    cf : matplotlib.collections.QuadMesh
        Contourf artist for colorbar
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Create mesh for pcolormesh
    time_mesh, height_mesh = np.meshgrid(time, height, indexing="ij")

    # Plot
    cf = ax.pcolormesh(
        time_mesh, height_mesh, data, cmap=cmap, vmin=vmin, vmax=vmax, shading="auto"
    )

    ax.set_xlabel(xlabel, fontsize="medium")
    ax.set_ylabel(ylabel, fontsize="medium")
    ax.set_title(title, fontsize="large")

    plt.colorbar(cf, ax=ax)

    return fig, ax, cf


def configure_hovmoeller_axes(ax, time_format="%H:%M"):
    """
    Configure axes with standard settings for Hovmöller diagrams.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure
    time_format : str, optional
        Format string for time labels (default: '%H:%M')
    """
    ax.tick_params(axis="both", which="both", direction="out", labelsize="medium")
    ax.tick_params(axis="both", which="major", length=5.5, width=1)
    ax.tick_params(axis="both", which="minor", length=3.0, width=0.7)

    # Format time axis
    try:
        ax.xaxis.set_major_formatter(dates.DateFormatter(time_format))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    except AttributeError:
        # Time values are numeric, not datetime
        pass


def add_contours_to_hovmoeller(
    ax, time, height, data, levels=10, colors="black", linewidths=0.5
):
    """
    Add contour lines to a Hovmöller diagram.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to add contours to
    time : array_like
        Time values
    height : array_like
        Height values (m)
    data : 2D array
        Data values with shape (len(time), len(height))
    levels : int or array_like, optional
        Contour levels (default: 10)
    colors : str, optional
        Contour line color (default: 'black')
    linewidths : float, optional
        Line width (default: 0.5)
    """
    time_mesh, height_mesh = np.meshgrid(time, height, indexing="ij")

    cs = ax.contour(
        time_mesh,
        height_mesh,
        data,
        levels=levels,
        colors=colors,
        linewidths=linewidths,
    )

    return cs
