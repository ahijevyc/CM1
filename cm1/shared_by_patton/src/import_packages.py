# =======================================================================
# This notebook is to synergize the models (NCAR-LES, WRF-LES, WRF-SCM) 
# and SAS observations (ground-based, airborne) for the BL-REINV project.
#
# SAS observations (ground-based, Long-EZ, and C130) can be found here:
# /glade/p/mmm/nmmm0058/siyuan/sas_obs
#
# My finalized WRF-LES-chemistry archive (postprocessed) is here:
# /glade/p/mmm/nmmm0058/siyuan/wrfout_postproc_05:00-18:00_pblavg.nc
#
# WRF-SCM archives (postprocessed) are here:
# /glade/p/mmm/nmmm0058/siyuan/WRFSCAM_chem_v0_eta_level/run/ysu_hires/test_WRFSCM_postproc_v0.nc
# /glade/p/mmm/nmmm0058/siyuan/WRFSCAM_chem_v0_eta_level/run/ysu_lores/test_WRFSCM_postproc_v0.nc
# /glade/p/mmm/nmmm0058/siyuan/WRFSCAM_chem_v0_eta_level/run/mynn_hires/test_WRFSCM_postproc_v0.nc
# /glade/p/mmm/nmmm0058/siyuan/WRFSCAM_chem_v0_eta_level/run/mynn_lores/test_WRFSCM_postproc_v0.nc
#
# Siyuan Wang (siyuan.wang@noaa.gov)  25 October 2020
# =======================================================================

from netCDF4 import Dataset, MFDataset
import pandas as pd
import numpy as np
import xarray as xr
import datetime as dt
import time
import pickle
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import matplotlib.backends.backend_pdf
import matplotlib.patches as patches

#from wrf import getvar, extract_times, ALL_TIMES
#import glob
#import fnmatch
#import os

from datetime import datetime

# from pyDOE import lhs

#plt.style.use('bmh')
#plt.style.use('grayscale')
#plt.style.use('seaborn')
#plt.style.use('seaborn-white')

path_base = '/Users/patton/research/les/reinvest/sas/anl/data'
