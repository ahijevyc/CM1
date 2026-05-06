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
# Physical constants (SI units)
# ========================================================================

# Gravitational acceleration (m/s^2)
GRAVITY = 9.81

# Earth's rotation rate (rad/s)
EARTH_OMEGA = 7.2921e-5

# Dry gas constant for air (J/(kg·K))
R_DRY = 287.0

# Gas constant for water vapor (J/(kg·K))
R_VAPOR = 461.5

# Specific heat at constant pressure (J/(kg·K))
CP_DRY = 1005.0

# Specific heat at constant volume (J/(kg·K))
CV_DRY = 718.0

# Latent heat of vaporization (J/kg)
L_VAPORIZATION = 2.501e6

# Latent heat of fusion (J/kg)
L_FUSION = 3.337e5

# Stefan-Boltzmann constant (W/(m^2·K^4))
STEFAN_BOLTZMANN = 5.670374419e-8

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

__all__ = [
    "PATH_BASE",
    "PATHS",
    "GRAVITY",
    "EARTH_OMEGA",
    "R_DRY",
    "R_VAPOR",
    "CP_DRY",
    "CV_DRY",
    "L_VAPORIZATION",
    "L_FUSION",
    "STEFAN_BOLTZMANN",
    "PLOT_DEFAULTS",
    "STATS_DEFAULTS",
]
