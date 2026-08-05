#!/usr/bin/env python
"""
plot_combined_max_psd.py
-------------------------
Loops through three specified CM1 experiment directories, processes horizontal
power spectra of a chosen variable (e.g., winterp) averaged over a custom altitude layer,
extracts the wavelength of the maximum PSD for each file, and plots all three
time series curves on a single set of axes.

Saves a high-resolution publication-quality PNG comparing the dominant scale evolution.

Usage:
    python plot_combined_max_psd.py --pbl-bot 2.0 --pbl-top 5.0 --var winterp

Requirements:
    pip install netCDF4 numpy matplotlib scipy
"""

import os
import re
import glob
import argparse
import numpy as np
import matplotlib

# Use Agg backend for headless operation on clusters like Derecho
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# --- Fast, Robust Numerical Sorting Helper ---
def extract_sequence_number(filepath):
    """
    Extracts the sequence of digits right before .nc in the filename,
    falling back to the first sequence of digits found in the filename.
    This prevents folder names (like test11) from throwing off file sequence orders.
    """
    filename = os.path.basename(filepath)
    # Search for digits right before the .nc extension
    match = re.search(r"(\d+)\.nc$", filename)
    if match:
        return int(match.group(1))
    # Fallback to any sequence of digits in the filename
    match = re.search(r"(\d+)", filename)
    return int(match.group(1)) if match else 0


def get_sorted_files(directory):
    """
    Finds, deduplicates, and numerically sorts NetCDF sequence files matching CM1 output patterns.
    Deduplication by sequence number prevents processing duplicate copies or backup files.
    """
    patterns = ["cm1out_0000[7-9]*.nc", "cm1out_000[12]*.nc"]
    matched_files = []
    for pat in patterns:
        matched_files.extend(glob.glob(os.path.join(directory, pat)))

    # Deduplicate by sequence number to avoid redundant frames (e.g., cm1out_000120_copy.nc)
    seen_seqs = {}
    for filepath in matched_files:
        seq = extract_sequence_number(filepath)
        # Prefer the standard/shorter filename when duplicates exist
        if seq not in seen_seqs or len(os.path.basename(filepath)) < len(
            os.path.basename(seen_seqs[seq])
        ):
            seen_seqs[seq] = filepath

    # Sort the unique files numerically by sequence number
    sorted_keys = sorted(seen_seqs.keys())
    sorted_list = [seen_seqs[k] for k in sorted_keys]
    return sorted_list


def running_mean(x, n):
    """Simple symmetric running mean wrapper."""
    if n <= 1:
        return x
    kernel = np.ones(n) / n
    return np.convolve(x, kernel, mode="same")


def compute_max_psd_timeline(
    files, var, pbl_bot_km, pbl_top_km, nsmooth, detrend, window
):
    """
    Processes a list of CM1 files to compute the timeline of the wavelength
    at which the Power Spectral Density (PSD) is maximized.
    """
    num_frames = len(files)
    if num_frames == 0:
        return np.array([]), np.array([])

    print(f"  Found {num_frames} matching NetCDF files.")

    # Initialize parameters using the baseline metadata from the first file
    with Dataset(files[0], "r") as ds:
        zh = ds.variables["zh"][:]  # Scalar-level heights (km)
        xh_km = ds.variables["xh"][:]

        # Identify vertical levels within our specified altitude range
        pbl_mask = (zh >= pbl_bot_km) & (zh <= pbl_top_km)
        pbl_levels = np.where(pbl_mask)[0]
        if len(pbl_levels) == 0:
            raise ValueError(
                f"No scalar levels found between heights of {pbl_bot_km} and {pbl_top_km} km!"
            )

        # Compute horizontal grid resolutions
        dx_m = float(np.median(np.diff(xh_km))) * 1000.0

        test_var = ds.variables[var]
        ny, nx = test_var.shape[2], test_var.shape[3]

    print(f"  Grid dimensions: {nx} x {ny} (dx = {dx_m:.1f} m)")
    print(
        f"  Vertical averaging levels: {len(pbl_levels)} levels in layer {pbl_bot_km:.2f} to {pbl_top_km:.2f} km"
    )

    # Build 2D Hanning window normalized to preserve variance
    if window:
        hann_x = np.hanning(nx)
        hann_y = np.hanning(ny)
        window2d = np.outer(hann_y, hann_x)
        window2d /= np.sqrt(np.mean(window2d**2))
    else:
        window2d = np.ones((ny, nx))

    # Setup wavenumber grids
    kx = np.fft.fftshift(np.fft.fftfreq(nx, d=dx_m))
    ky = np.fft.fftshift(np.fft.fftfreq(ny, d=dx_m))

    # Precompute radial bins for azimuthal average
    k_nyq = 0.5 / dx_m
    dk = 1.0 / (nx * dx_m)
    k_edges = np.arange(0, k_nyq + dk, dk)
    k_rad = 0.5 * (k_edges[:-1] + k_edges[1:])

    KX, KY = np.meshgrid(kx, ky)
    K_mesh = np.sqrt(KX**2 + KY**2)
    digitized_indices = np.digitize(K_mesh.ravel(), k_edges) - 1
    valid_indices = (digitized_indices >= 0) & (digitized_indices < len(k_rad))

    # Lists to store the time series results
    times_min = []
    max_wavelengths_m = []

    # Loop through and process each file sequentially
    for idx, fname in enumerate(files):
        try:
            with Dataset(fname, "r") as ds:
                time_val = float(ds.variables["time"][0])
                w_all = ds.variables[var][0, pbl_mask, :, :]  # (nz_layer, ny, nx)

            psd_stack = []
            for k in range(len(pbl_levels)):
                w2d = w_all[k, :, :]
                if detrend:
                    w2d = w2d - w2d.mean()
                w2d = w2d * window2d

                # Compute 2D Fourier transform normalized into power spectral density units
                W = np.fft.fftshift(np.fft.fft2(w2d)) / (nx * ny)
                P2d = (np.abs(W) ** 2) * (nx * dx_m) * (ny * dx_m)

                # Azimuthal average to 1D
                psd1d = np.zeros(len(k_rad))
                count = np.zeros(len(k_rad), dtype=int)
                np.add.at(
                    psd1d, digitized_indices[valid_indices], P2d.ravel()[valid_indices]
                )
                np.add.at(count, digitized_indices[valid_indices], 1)
                count = np.where(count == 0, 1, count)
                psd1d /= count

                psd_stack.append(psd1d)

            psd_mean = np.mean(psd_stack, axis=0)

            # Filter k > 0 to avoid division by zero at the infinite scale
            nonzero = k_rad > 0
            k_plot = k_rad[nonzero]
            psd_plot = psd_mean[nonzero]

            # Smooth and identify peak wavelength scale
            wavelength_km = (1.0 / k_plot) / 1000.0
            psd_smooth = running_mean(psd_plot, nsmooth)

            idx_max = np.argmax(psd_smooth)
            lambda_max_m = wavelength_km[idx_max] * 1000.0

            times_min.append(time_val / 60.0)
            max_wavelengths_m.append(lambda_max_m)
        except Exception as e:
            print(
                f"\nWarning: Skipped parsing file {os.path.basename(fname)} due to: {str(e)}"
            )

    return np.array(times_min), np.array(max_wavelengths_m)


def main():
    parser = argparse.ArgumentParser(
        description="Plot combined Max PSD wavelength scale for multiple run directories."
    )
    parser.add_argument(
        "--var",
        default="winterp",
        help="Variable name in NetCDF files (default: winterp)",
    )
    parser.add_argument(
        "--pbl-bot",
        type=float,
        default=2.0,
        help="Layer bottom limit in km (default: 2.0)",
    )
    parser.add_argument(
        "--pbl-top",
        type=float,
        default=5.0,
        help="Layer top limit in km (default: 5.0)",
    )
    parser.add_argument(
        "--nsmooth",
        type=int,
        default=5,
        help="Running-mean smooth spectral width points (default: 5)",
    )
    parser.add_argument(
        "--no-detrend",
        action="store_true",
        help="Do not subtract the horizontal mean before FFT",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Do not apply 2D Hanning window to inputs",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="combined_max_psd_timeline.png",
        help="Output PNG file path",
    )
    args = parser.parse_args()

    # Define base path dynamically resolving environment variables
    base_path = os.path.expandvars("$SCRATCH/../morrison/cm1_dci_study/cm1r21.0/run")

    # Configure directories and publication-quality labels
    experiments = {
        "pbl0.42km": {
            "path": os.path.join(base_path, "test11_highres_pbl0.42km_rh0.9"),
            "label": "PBL Ht = 0.42 km",
            "color": "#1f77b4",
            "marker": "o",
        },
        "pbl0.84km": {
            "path": os.path.join(base_path, "test11_highres_pbl0.84km_rh0.9"),
            "label": "PBL Ht = 0.84 km",
            "color": "#ff7f0e",
            "marker": "s",
        },
        "pbl1.68km": {
            "path": os.path.join(base_path, "test11_highres_pbl1.68km_rh0.9"),
            "label": "PBL Ht = 1.68 km",
            "color": "#2ca02c",
            "marker": "^",
        },
    }

    plt.figure(figsize=(8.5, 5.5))

    # Process each directory sequentially
    for key, info in experiments.items():
        print("\n==================================================")
        print(f"Processing experiment: {info['label']}")
        print(f"Directory: {info['path']}")

        try:
            files = get_sorted_files(info["path"])
            times, max_wavelengths = compute_max_psd_timeline(
                files=files,
                var=args.var,
                pbl_bot_km=args.pbl_bot,
                pbl_top_km=args.pbl_top,
                nsmooth=args.nsmooth,
                detrend=not args.no_detrend,
                window=not args.no_window,
            )

            # Sort and deduplicate arrays chronologically by simulation time.
            # Dict mapping handles duplicate times step-clashes (e.g. restarts/overlapping runs)
            if len(times) > 0:
                time_dict = {}
                for t, wl in zip(times, max_wavelengths):
                    # Rounding to 4 decimals prevents floating-point matching errors
                    time_dict[round(t, 4)] = wl

                sorted_times = np.array(sorted(time_dict.keys()))
                sorted_wavelengths = np.array([time_dict[t] for t in sorted_times])

                times = sorted_times
                max_wavelengths = sorted_wavelengths

            # Plot results for this run
            plt.plot(
                times,
                max_wavelengths,
                color=info["color"],
                marker=info["marker"],
                ls="-",
                lw=1.8,
                ms=5,
                label=info["label"],
            )
            print(f"Successfully processed {key}.")

        except Exception as e:
            print(f"ERROR processing {key}: {str(e)}")
            print("Skipping this experiment and continuing...")

    # Customize and format the combined plot axes
    plt.xlabel("Simulation Time (min)", fontsize=12)
    plt.ylabel("Wavelength of Max PSD (m)", fontsize=12)
    plt.title(
        f"Dominant Spatial Scale Evolution of ${args.var}$\nAveraged over layer: {args.pbl_bot:.2f} to {args.pbl_top:.2f} km",
        fontsize=12,
        pad=12,
    )

    plt.grid(True, which="both", ls=":", alpha=0.5, lw=0.8)
    plt.legend(
        fontsize=10,
        loc="upper left",
        framealpha=0.9,
        facecolor="white",
        edgecolor="#cccccc",
    )

    # Tweak design layout parameters
    plt.tight_layout()

    # Export and save the plot
    plt.savefig(args.output, dpi=300, bbox_inches="tight")
    print("\n==================================================")
    print(f"Combined Max PSD timeline plot successfully saved to:\n  --> {args.output}")
    print("==================================================\n")


if __name__ == "__main__":
    main()
