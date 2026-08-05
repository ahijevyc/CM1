"""
Sanity check for pbl/plotting/profiles.py against real SAS campaign data.

Reproduces (a subset of) shared_by_patton/plots/met_flux_profiles.pdf: resolved+SGS
vertical flux profiles of u'w', w'theta', w'q' at a given local time, for CM1 and
NCAR-LES, using the refactored plotting helpers instead of Ned's original inline
matplotlib calls.
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from cm1.pbl.plotting.profiles import configure_profile_axes, add_resolved_and_sgs_lines
from cm1.pbl.analysis.utils import rolling_average

MODELS = {
    "CM1": ("cm1/shared_by_patton/data/les/cm1/cm1_sas_stats.nc", "magenta"),
    "NCAR-LES": (
        "cm1/shared_by_patton/data/les/ncar-les/patton_sas_stats.nc",
        "orange",
    ),
}

time2plot = 12.0  # local time (hr) to plot
num = 12  # 5-min data -> 60-min centered rolling average
facq = 1000.0  # kg/kg -> g/kg

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))
for ax in axs:
    configure_profile_axes(ax)

for label, (path, color) in MODELS.items():
    ds = xr.open_dataset(path)
    time_hr = 5.0 + ds["time"].values / 3600.0
    it = np.argmin(np.abs(time_hr - time2plot))
    zw_km = ds["zw"].isel(nt=it).values / 1000.0

    uw_tot = rolling_average((ds["uw_r"] + ds["uw_s"]).values, num)[it]
    uw_sgs = rolling_average(ds["uw_s"].values, num)[it]
    wt_tot = rolling_average((ds["wt_r"] + ds["wt_s"]).values, num)[it]
    wt_sgs = rolling_average(ds["wt_s"].values, num)[it]
    wq_tot = rolling_average(((ds["wq_r"] + ds["wq_s"]) * facq).values, num)[it]
    wq_sgs = rolling_average((ds["wq_s"] * facq).values, num)[it]

    add_resolved_and_sgs_lines(axs[0], uw_tot, uw_sgs, zw_km, color=color, label=label)
    add_resolved_and_sgs_lines(axs[1], wt_tot, wt_sgs, zw_km, color=color, label=label)
    add_resolved_and_sgs_lines(axs[2], wq_tot, wq_sgs, zw_km, color=color, label=label)
    ds.close()

axs[0].set_xlabel(r"$\overline{u'w'}$ [m$^2$ s$^{-2}$]")
axs[1].set_xlabel(r"$\overline{w'\theta'}$ [m K s$^{-1}$]")
axs[2].set_xlabel(r"$\overline{w'q'}$ [m s$^{-1}$ g kg$^{-1}$]")
axs[0].set_ylabel("z [km]")
for ax in axs:
    ax.set_ylim(0, 1.8)
    ax.axvline(0.0, color="black", linewidth=0.3)
axs[1].legend(fontsize="small")
fig.suptitle(f"{time2plot:.0f} LT")
fig.tight_layout()
fig.savefig("cm1_test_flux_profiles.png", dpi=150)
