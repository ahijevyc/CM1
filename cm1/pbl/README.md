# PBL Analysis Toolkit

A reusable version of the boundary-layer analysis scripts originally shared
by Ned Patton in [`cm1/shared_by_patton/src/`](../shared_by_patton/src/).
Those scripts each ran standalone, pulling in shared logic via
`exec(open('other_script.py').read())` calls. This package extracts that
logic into plain, importable functions, organized by what they do rather
than which script they came from.

## Layout

```
pbl/
  analysis/
    definitions.py   constants, default paths, plotting/stats defaults
    utils.py         statistics & data-analysis helpers (rolling means, binned
                      percentiles, ragged-array handling, ICT-file parsing, ...)
  plotting/
    profiles.py      vertical profile plots (resolved+SGS lines, obs overlays)
    hovmoeller.py     time-height Hovmoeller diagrams
    spectra.py        power-spectrum plots
    timeseries.py      time series plots
  data/
    readers.py        generic (model-agnostic) xarray helpers
  spectra_core.py, cm1_w_spectra_animated.py, combined_max_psd.py
                       a separate tool for horizontal power spectra of raw CM1
                       3-D output (winterp etc.) — unrelated to Ned's src/ scripts
```

### Also in this package: CM1 horizontal-spectra tools

Two standalone command-line tools, unrelated to the Ned-script port described
below, for looking at horizontal power spectra of raw CM1 3-D output (e.g.
`winterp`). Both build on the PSD/azimuthal-averaging logic in
`spectra_core.py`, but unlike `analysis/`, `plotting/`, and `data/`, they're
runnable scripts (argument parsing, a `__main__` block), not importable
libraries.

- `cm1_w_spectra_animated.py` — interactive GUI to scrub through a CM1 output
  sequence and watch the horizontal spectrum evolve, with Play/Pause/speed
  controls and slider seeking. Can also export the animation to MP4/GIF
  headlessly instead of opening a window.

  ```
  python cm1_w_spectra_animated.py cm1out_*.nc --pbl-bot 0 --pbl-top 0.84
  python cm1_w_spectra_animated.py cm1out_*.nc --save-video spectra.mp4
  ```

- `combined_max_psd.py` — batch-compares the dominant spectral scale over time
  across several experiment directories on one plot. Currently hardcoded to
  three PBL-height sensitivity runs in its `experiments` dict — edit that for
  other runs.

  ```
  python combined_max_psd.py --pbl-bot 2.0 --pbl-top 5.0 --var winterp
  ```

### Mapping from Ned's original scripts

| Original (`shared_by_patton/src/`) | Refactored equivalent |
|---|---|
| `plot_met_flux_profiles.py`, `plot_met_scl_flux_profiles.py` | `plotting/profiles.py` |
| `plot_met_hov+prof.py` (Hovmoeller portion) | `plotting/hovmoeller.py` |
| `plot_met_spectra.py` | `plotting/spectra.py` |
| `plot_met_timeseries.py` | `plotting/timeseries.py` |
| `definitions.py` | `analysis/definitions.py` + `analysis/utils.py` |
| `import_packages.py` | no equivalent — each module imports only what it needs |
| `read_les_cm1.py` and friends | not yet ported; see "Known gaps" below |

**Important difference from the originals:** these are building-block
functions (style an axes, draw one line, add one contour set), not
end-to-end scripts. Assembling the actual figure — opening the dataset,
pulling out the needed arrays, looping over models/times — is left to the
caller. See `cm1/tests/test_profiles.py` and `cm1/tests/test_hovmoeller.py`
for worked examples.

## Verifying against the reference plots

`cm1/tests/` has three scripts that load real SAS-campaign data and call the
refactored functions, producing output that can be compared directly against
the reference PDFs in `shared_by_patton/plots/`:

```
python cm1/tests/test_profiles.py  # -> cm1_test_flux_profiles.png
                                   #    compare to shared_by_patton/plots/met_flux_profiles.pdf
python cm1/tests/test_hovmoeller.py # -> cm1_test_hovmoeller_CM1.png, cm1_test_hovmoeller_NCAR_LES.png
                                   #    compare to the CM1/NCAR-LES theta panels in
                                   #    shared_by_patton/plots/met_hov+prof.all.pdf
python cm1/tests/test_pbl.py       # -> cm1_sas_uu_spec2d.png (spectra sanity check)
```

These read from `cm1/shared_by_patton/data/les/{cm1,ncar-les,mpas}/` — the
CM1 files are the ones Ned originally shared; the NCAR-LES and MPAS files are
symlinks into the SAS campaign archive
(`/glade/campaign/mmm/dpm/patton/data/reinvest/data/sas/les/`), recovered
since they weren't included originally. Any environment with `netCDF4`,
`xarray`, `pandas`, and `matplotlib` will run these.

## Using it on new data

The pattern is the same regardless of which model produced the data — pull
the needed arrays out with `xarray`, then hand them to the plotting helpers:

```python
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pbl.plotting.profiles import configure_profile_axes, add_resolved_and_sgs_lines
from pbl.analysis.utils import rolling_average

ds = xr.open_dataset("my_new_run_sas_stats.nc")
time_hr = 5.0 + ds["time"].values / 3600.0
it = np.argmin(np.abs(time_hr - 12.0))       # nearest step to 1200 LT
zw_km = ds["zw"].isel(nt=it).values / 1000.0

uw_tot = rolling_average((ds["uw_r"] + ds["uw_s"]).values, 12)[it]
uw_sgs = rolling_average(ds["uw_s"].values, 12)[it]

fig, ax = plt.subplots()
configure_profile_axes(ax)
add_resolved_and_sgs_lines(ax, uw_tot, uw_sgs, zw_km, color="magenta", label="My New Run")
```

## How CM1's `dodomaindiag=.true` varnames map to SAS stats

The SAS analysis's cross-model variable names map directly onto CM1's native
`dodomaindiag` names:

| SAS name | CM1 name | What it is |
|---|---|---|
| `t` | `th` | potential temperature, domain-mean profile |
| `q` | `qv` | water vapor mixing ratio, domain-mean profile |
| `u` / `v` | `u` / `v` | horizontal wind components, domain-mean profile |
| `uu_r` / `vv_r` / `ww_r` | `upup` / `vpvp` / `wpwp` | resolved-scale momentum variance: ⟨u'u'⟩, ⟨v'v'⟩, ⟨w'w'⟩ |
| `tke_r` | `rtke` | resolved-scale turbulence kinetic energy |
| `tke_s` | `stke` | subgrid-scale turbulence kinetic energy |
| `tt_r` / `qq_r` | `thvarr` / `qvvarr` | resolved-scale variance of potential temperature / water vapor |
| `uw_r` / `vw_r` / `wt_r` / `wq_r` | `ufr` / `vfr` / `thfr` / `qvfr` | resolved-scale vertical flux: ⟨u'w'⟩, ⟨v'w'⟩, ⟨w'θ'⟩, ⟨w'qv'⟩ |
| `uw_s` / `vw_s` / `wt_s` / `wq_s` | `ufs` / `vfs` / `thfs` / `qvfs` | subgrid-scale (parameterized) vertical flux of momentum, θ, and water vapor |

"Resolved" = computed directly from the simulated flow (Reynolds
deviations from the horizontal mean); "subgrid" = whatever the turbulence
closure parameterizes as unresolved. Every CM1 field above also has an
`fd`/diffusion counterpart (e.g. `thfd`) capturing numerical diffusion, which
has no place in SAS's resolved/subgrid split — worth noting if totals don't
balance exactly.

## Known gaps / things to double-check

- Only CM1 and NCAR-LES have been run end-to-end against real data. WRF-LES,
  DALES, MicroHH, FastEddy (stored as a pickle, not netCDF), MPAS, and the SCM
  datasets exist under `shared_by_patton/data/` but nobody has written the
  per-model extraction code for them yet in this package.
- There's no built-in "one row per model" layout like the stacked Hovmoeller
  comparison in `met_hov+prof.all.pdf` — `test_hovmoeller.py` shows the
  loop-and-call-per-model pattern needed to build one.
- `analysis/definitions.py`, `plotting/timeseries.py`, and `data/readers.py`
  haven't been exercised against real data yet — only `profiles.py`,
  `hovmoeller.py`, and `spectra.py` have. `analysis/utils.py`'s statistics
  functions were checked against synthetic inputs to confirm they match the
  original implementations exactly, but not run through a full plotting
  pipeline.
- No helper yet to build a `cm1_sas_stats.nc`-style file from a fresh
  `dodomaindiag` run (concatenate the per-timestep `cm1out_diag_*.nc` files
  along time, rename variables per the table above).
