"""
Vertical profile plotting utilities for boundary-layer analysis.

This module provides functions for plotting vertical profiles of atmospheric variables.

Original source files (in patton/src):
    - plot_met_flux_profiles.py - vertical profiles with flux components
    - plot_met_scl_flux_profiles.py - scalar flux profiles

References
----------
Adapted from Ned Patton's boundary-layer analysis software for the BL-REINV project.
"""


def configure_profile_axes(ax, fontsize="small", label_pad=3):
    """
    Configure matplotlib axes with standard settings for profile plots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure
    fontsize : str, optional
        Font size for tick labels (default: 'small')
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


def add_resolved_and_sgs_lines(
    ax,
    x_resolved,
    x_sgs,
    height,
    color,
    label="",
    linewidth_resolved=2.0,
    linewidth_sgs=1.2,
    linestyle_resolved="solid",
    linestyle_sgs="dashed",
):
    """
    Add resolved and SGS (subgrid-scale) components to a profile plot.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to plot on
    x_resolved : array_like
        Resolved component values
    x_sgs : array_like
        SGS component values
    height : array_like
        Height coordinate
    color : str
        Color for the lines
    label : str, optional
        Label for the resolved component (default: '')
    linewidth_resolved : float, optional
        Line width for resolved component (default: 2.0)
    linewidth_sgs : float, optional
        Line width for SGS component (default: 1.2)
    linestyle_resolved : str, optional
        Line style for resolved (default: 'solid')
    linestyle_sgs : str, optional
        Line style for SGS (default: 'dashed')
    """
    ax.plot(
        x_sgs, height, color=color, linestyle=linestyle_sgs, linewidth=linewidth_sgs
    )
    ax.plot(
        x_resolved,
        height,
        color=color,
        linestyle=linestyle_resolved,
        linewidth=linewidth_resolved,
        label=label,
    )


def add_observation_profile(
    ax,
    x_obs,
    height_obs,
    marker="o",
    color="black",
    markersize=5,
    label="",
    errorbar=None,
):
    """
    Add observed profile to a plot.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to plot on
    x_obs : array_like
        Observed values
    height_obs : array_like
        Heights at which observations were taken
    marker : str, optional
        Marker style (default: 'o')
    color : str, optional
        Color for observations (default: 'black')
    markersize : float, optional
        Marker size (default: 5)
    label : str, optional
        Label for legend (default: '')
    errorbar : array_like, optional
        Uncertainty values for errorbar (default: None)
    """
    if errorbar is None:
        ax.plot(
            x_obs,
            height_obs,
            marker=marker,
            color=color,
            markersize=markersize,
            linestyle="-",
            linewidth=0,
            label=label,
        )
    else:
        ax.errorbar(
            x_obs,
            height_obs,
            xerr=errorbar,
            color=color,
            marker=marker,
            markersize=markersize,
            linestyle="-",
            linewidth=0,
            label=label,
            elinewidth=0.5,
            fillstyle="none",
        )


__all__ = [
    "configure_profile_axes",
    "add_resolved_and_sgs_lines",
    "add_observation_profile",
]
