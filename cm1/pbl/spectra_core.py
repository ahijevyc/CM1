#!/usr/bin/env python
"""
spectra_core.py
----------------
Shared grid, windowing, and horizontal power-spectrum utilities for CM1 output.

Factored out of cm1_w_spectra_animated.py and combined_max_psd.py, which both
computed PBL-mean horizontal power spectra of a CM1 field the same way: read grid
metadata from the first file, build a Hanning window and radial wavenumber bins once,
then for each file compute a 2D FFT per level, azimuthally average, and mean across
levels.

Used by:
    - cm1_w_spectra_animated.py - interactive spectral animator
    - combined_max_psd.py - batch comparison of dominant-scale timelines
"""

import os
import re
from dataclasses import dataclass

import numpy as np
from netCDF4 import Dataset


def extract_sequence_number(filepath):
    """
    Extracts the sequence of digits right before the .nc extension in the filename,
    falling back to the first sequence of digits found in the filename.
    This prevents folder names (like test11) from throwing off file sequence order.
    """
    filename = os.path.basename(filepath)
    match = re.search(r"(\d+)\.nc$", filename)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d+)", filename)
    return int(match.group(1)) if match else 0


def format_psd_units(raw_units):
    """
    Derives LaTeX formatting for 1-D PSD units [Var_Units^2 * m].
    1-D spectrum units represent variance per unit wavenumber.
    """
    u = raw_units.strip()
    if re.match(r"^m\s*/\s*s$|^m\s*s\s*[-⁻]?1$", u, re.IGNORECASE):
        return r"m$^3$ s$^{-2}$"
    elif u.upper() == "K":
        return r"K$^2$ m"
    elif re.match(r"^g\s*/\s*kg$|^g\s*kg\s*[-⁻]?1$", u, re.IGNORECASE):
        return r"(g/kg)$^2$ m"
    elif re.match(r"^kg\s*/\s*kg$|^kg\s*kg\s*[-⁻]?1$", u, re.IGNORECASE):
        return r"(kg/kg)$^2$ m"
    else:
        return f"({u})$^2$ m"


def running_mean(x, n):
    """Simple symmetric running mean wrapper."""
    if n <= 1:
        return x
    kernel = np.ones(n) / n
    return np.convolve(x, kernel, mode="same")


@dataclass
class GridInfo:
    """Grid spacing and PBL-layer metadata read from one CM1 file."""

    zh: np.ndarray
    pbl_mask: np.ndarray
    pbl_levels: np.ndarray
    dx_m: float
    dy_m: float
    nx: int
    ny: int
    var_units: str


def read_grid_info(filepath, var, pbl_bot_km, pbl_top_km):
    """Read grid spacing, PBL-layer levels, and variable metadata from a CM1 file."""
    with Dataset(filepath, "r") as ds:
        zh = ds.variables["zh"][:]  # scalar-level heights (km)
        xh_km = ds.variables["xh"][:]
        yh_km = ds.variables["yh"][:]

        pbl_mask = (zh >= pbl_bot_km) & (zh <= pbl_top_km)
        pbl_levels = np.where(pbl_mask)[0]
        if len(pbl_levels) == 0:
            raise ValueError(
                f"No scalar levels found between heights of {pbl_bot_km} and {pbl_top_km} km!"
            )

        dx_m = float(np.median(np.diff(xh_km))) * 1000.0
        dy_m = float(np.median(np.diff(yh_km))) * 1000.0

        test_var = ds.variables[var]
        ny, nx = test_var.shape[2], test_var.shape[3]
        try:
            var_units = test_var.units.strip()
        except AttributeError:
            var_units = "m/s"  # Default fallback if units attribute doesn't exist

    return GridInfo(
        zh=zh,
        pbl_mask=pbl_mask,
        pbl_levels=pbl_levels,
        dx_m=dx_m,
        dy_m=dy_m,
        nx=nx,
        ny=ny,
        var_units=var_units,
    )


class HorizontalSpectrum:
    """
    Computes horizontal (x-y) power spectra of a 2D field on an isotropic grid,
    azimuthally averaged onto 1-D radial wavenumber bins.
    """

    def __init__(self, nx, ny, dx_m, window=True):
        self.nx = nx
        self.ny = ny
        self.dx_m = dx_m

        if window:
            hann_x = np.hanning(nx)
            hann_y = np.hanning(ny)
            self.window2d = np.outer(hann_y, hann_x)
            self.window2d /= np.sqrt(np.mean(self.window2d**2))
        else:
            self.window2d = np.ones((ny, nx))

        kx = np.fft.fftshift(np.fft.fftfreq(nx, d=dx_m))
        ky = np.fft.fftshift(np.fft.fftfreq(ny, d=dx_m))

        # Precompute radial bins for azimuthal average
        self.k_nyq = 0.5 / dx_m  # Nyquist frequency
        self.dk = 1.0 / (nx * dx_m)  # Fundamental frequency
        self.k_edges = np.arange(0, self.k_nyq + self.dk, self.dk)
        self.k_rad = 0.5 * (self.k_edges[:-1] + self.k_edges[1:])  # Center of bins

        KX, KY = np.meshgrid(kx, ky)
        K_mesh = np.sqrt(KX**2 + KY**2)
        self.digitized_indices = np.digitize(K_mesh.ravel(), self.k_edges) - 1
        self.valid_indices = (self.digitized_indices >= 0) & (
            self.digitized_indices < len(self.k_rad)
        )

        # Dynamic bounds for a Kolmogorov reference line, based on grid resolution:
        # scales from 4*dx to 30*dx (e.g. 0.4 km to 3.0 km for a 100-m grid).
        self.slope_x = np.array([4.0 * dx_m, 30.0 * dx_m]) / 1000.0
        self.lambda_anchor = np.sqrt(
            self.slope_x[0] * self.slope_x[1]
        )  # geometric mean

    def azimuthal_average(self, power2d):
        """Collapses a 2-D power spectrum onto 1-D radial wavenumber bins."""
        psd1d = np.zeros(len(self.k_rad))
        count = np.zeros(len(self.k_rad), dtype=int)

        np.add.at(
            psd1d,
            self.digitized_indices[self.valid_indices],
            power2d.ravel()[self.valid_indices],
        )
        np.add.at(count, self.digitized_indices[self.valid_indices], 1)

        count = np.where(count == 0, 1, count)
        psd1d /= count
        return psd1d

    def psd2d(self, w2d, detrend=True):
        """2D FFT of a field to physical spectral density units (Var_Units^2 * m^2)."""
        if detrend:
            w2d = w2d - w2d.mean()
        w2d = w2d * self.window2d
        W = np.fft.fftshift(np.fft.fft2(w2d)) / (self.nx * self.ny)
        return (np.abs(W) ** 2) * (self.nx * self.dx_m) * (self.ny * self.dx_m)

    def psd_of_levels(self, w_all, detrend=True):
        """Mean 1-D PSD across a stack of 2D levels with shape (nz, ny, nx)."""
        psd_stack = [
            self.azimuthal_average(self.psd2d(w_all[k, :, :], detrend=detrend))
            for k in range(w_all.shape[0])
        ]
        return np.mean(psd_stack, axis=0)


def compute_frame_psd(filepath, var, pbl_mask, spectrum, detrend=True, nsmooth=5):
    """
    Loads variable data from one CM1 file and computes the PBL-mean horizontal
    power spectrum.

    Returns
    -------
    wavelength_km, psd_smooth, psd_plot, time_val
    """
    with Dataset(filepath, "r") as ds:
        time_val = float(ds.variables["time"][0])
        w_all = ds.variables[var][0, pbl_mask, :, :]  # (nz_pbl, ny, nx)

    psd_mean = spectrum.psd_of_levels(w_all, detrend=detrend)

    # Filter k > 0 to avoid division by zero at the infinite scale
    nonzero = spectrum.k_rad > 0
    k_plot = spectrum.k_rad[nonzero]
    psd_plot = psd_mean[nonzero]

    wavelength_km = (1.0 / k_plot) / 1000.0
    psd_smooth = running_mean(psd_plot, nsmooth)

    return wavelength_km, psd_smooth, psd_plot, time_val
