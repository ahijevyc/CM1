import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from cm1.pbl.plotting.spectra import (
    configure_spectrum_axes,
    add_spectrum,
    add_inertial_subrange,
    configure_loglog_axes,
)

spec_path = "cm1/shared_by_patton/data/les/cm1/cm1_sas_spectra.nc"
stats_path = "cm1/shared_by_patton/data/les/cm1/cm1_sas_stats.nc"

ds_spec = xr.open_dataset(spec_path)
ds_stats = xr.open_dataset(stats_path)

# x-axis wavenumber source: xk_a
# spectrum source: *_spec2d
spec_var = (
    "uu_spec2d"  # try vv_spec2d, ww_spec2d, uw_spec2d, wt/wq equivalents if present
)
it = 60  # time index (0..nt-1)
iz = 100  # height index (0..nz-1)
num = 12  # centered rolling average length (5-min data -> 60 min)

spec_smoothed = ds_spec[spec_var].rolling(nt=num, center=True, min_periods=1).mean()

kzi_all = ds_spec["xk_a"] * ds_stats["zi_t"]  # (nt, ncx)

# excludes the zero wavenumber bin by starting at index 1
kzi = kzi_all.isel(nt=it, ncx=slice(1, None)).values
power = spec_smoothed.isel(nt=it, nz=iz, ncx=slice(1, None)).values

# Keep positive finite values for log-log plotting
m = np.isfinite(kzi) & np.isfinite(power) & (kzi > 0.0) & (power > 0.0)
kzi = kzi[m]
power = power[m]

fig, ax = plt.subplots(figsize=(7, 5))
configure_spectrum_axes(ax)
add_spectrum(
    ax, kzi, power, color="black", linewidth=2.0, label=f"{spec_var} nt={it} nz={iz}"
)

# Optional -5/3 reference line
if kzi.size > 10:
    i0 = max(1, int(0.1 * kzi.size))
    i1 = max(i0 + 1, int(0.5 * kzi.size))
    add_inertial_subrange(
        ax,
        freq_min=float(kzi[i0]),
        freq_max=float(kzi[i1]),
        power_at_min=float(power[i0]),
        slope=-5.0 / 3.0,
        color="gray",
        linestyle="--",
        label="-5/3",
    )

configure_loglog_axes(ax)
ax.set_xlabel(r"$k_h\, z_i$")
ax.set_ylabel("Power spectral density")
ax.legend()
fig.tight_layout()
fig.savefig(f"cm1_sas_{spec_var}.png", dpi=150)
plt.show()

ds_spec.close()
ds_stats.close()
