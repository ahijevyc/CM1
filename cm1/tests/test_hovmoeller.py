"""
Sanity check for pbl/plotting/hovmoeller.py against real SAS campaign data.

Reproduces (a subset of) the "combined" pages in
shared_by_patton/plots/met_hov+prof.all.pdf: a time-height Hovmoeller diagram of mean
potential temperature, with the PBL height overlaid, for CM1 and NCAR-LES
individually, using the refactored plotting helpers.
"""

import xarray as xr

from cm1.pbl.plotting.hovmoeller import (
    create_hovmoeller_plot,
    add_contours_to_hovmoeller,
)

MODELS = {
    "CM1": "cm1/shared_by_patton/data/les/cm1/cm1_sas_stats.nc",
    "NCAR-LES": "cm1/shared_by_patton/data/les/ncar-les/patton_sas_stats.nc",
}

for label, path in MODELS.items():
    ds = xr.open_dataset(path)
    time_hr = 5.0 + ds["time"].values / 3600.0
    zu_km = ds["zu"].isel(nt=0).values / 1000.0
    theta = ds["t"].values  # (nt, nz)
    zi_km = ds["zi_t"].values / 1000.0

    fig, ax, cf = create_hovmoeller_plot(
        time_hr,
        zu_km,
        theta,
        figsize=(9, 3),
        cmap="RdBu_r",
        title=label,
        xlabel="Time [hr LT]",
        ylabel="z [km]",
    )
    add_contours_to_hovmoeller(
        ax, time_hr, zu_km, theta, levels=10, colors="black", linewidths=0.5
    )
    ax.plot(
        time_hr,
        zi_km,
        color="black",
        linestyle="dashdot",
        linewidth=2,
        label="PBL height",
    )
    ax.set_ylim(0, 2.4)
    ax.legend(loc="upper left", fontsize="small")
    fig.tight_layout()
    fig.savefig(f"cm1_test_hovmoeller_{label.replace('-', '_')}.png", dpi=150)
    ds.close()
