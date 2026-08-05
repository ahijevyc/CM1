"""
Definitions and constants for PBL analysis.

Contains default configuration, constants, and paths used throughout
the boundary-layer analysis toolkit.

Notes
-----
These paths and constants are adapted from Ned Patton's boundary-layer
analysis software. Users should update these as needed for their analysis.
"""

import os
from pathlib import Path

import metpy.constants as const

# ========================================================================
# Default data paths
# ========================================================================

# Base data directory (update as needed)
try:
    PATH_BASE = Path(os.environ.get("CM1_DATA_PATH", "/glade/derecho/scratch/"))
except Exception:
    PATH_BASE = Path("/glade/derecho/scratch/")

# Subdirectories for different data types
PATHS = {
    "cm1": PATH_BASE / "cm1",
    "observations": PATH_BASE / "observations",
    "wrf": PATH_BASE / "wrf",
    "les": PATH_BASE / "les",
}

# ========================================================================
# Physical constants — sourced from metpy.constants where available
# ========================================================================

GRAVITY = const.g  # 9.80665 m/s^2
EARTH_OMEGA = const.omega  # 7.292115e-05 rad/s
R_DRY = const.Rd  # dry air gas constant (J/(kg·K))
R_VAPOR = const.Rv  # water vapor gas constant (J/(kg·K))
CP_DRY = const.Cp_d  # specific heat at constant pressure (J/(kg·K))
CV_DRY = const.Cv_d  # specific heat at constant volume (J/(kg·K))
L_VAPORIZATION = const.Lv  # latent heat of vaporization (J/kg)
L_FUSION = const.Lf  # latent heat of fusion (J/kg)

# Stefan-Boltzmann constant — not available in metpy.constants
STEFAN_BOLTZMANN = 5.670374419e-8  # W/(m^2·K^4)

# ========================================================================
# Plotting defaults
# ========================================================================

PLOT_DEFAULTS = {
    "figsize": (12, 6),
    "dpi": 150,
    "font_size": 10,
    "line_width": 1.5,
    "marker_size": 5,
}

# ========================================================================
# Statistical analysis defaults
# ========================================================================

STATS_DEFAULTS = {
    "percentile": 50,  # Median
    "min_samples": 5,  # Minimum samples for valid statistic
}
