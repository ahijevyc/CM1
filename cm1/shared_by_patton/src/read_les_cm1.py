# -----------------------------------
# Load CM1 (post-processed file)
# -----------------------------------
CM1_file = path_base + "/les/cm1/cm1_sas_stats.nc"
CM1 = Dataset(CM1_file, mode='r')

CM1_ustar = CM1.variables['ustar'][:]
CM1_PBLH = CM1.variables['zi_t'][:]

CM1_zu = CM1.variables['zu'][0,:]
CM1_zw = CM1.variables['zw'][0,:]
CM1_time_hr = 5.0 + CM1.variables['time'][:] / 3600.0

#print('CM1_time_hr = ',CM1_time_hr)

# ------------------------------------
# a bunch of 2d variables: [time, lev]
# ------------------------------------
CM1_2dvar_list = ['t', 'q', 'u', 'v', 'w', 'p',
                  'uu_r', 'vv_r', 'ww_r',                          # resolved momentum variances
                  'tke_r', 'tke_s',                                # resolved/SGS TKE
                  'tt_r', 'qq_r',                                  # resolved scalar variances
                  'uw_r', 'uw_s', 'vw_r', 'vw_s',                  # resolved/SGS momentum fluxes
                  'wt_r', 'wt_s', 'wq_r', 'wq_s']                  # resolved/SGS fluxes: pot.temp and moisture
CM1_2dvar = [CM1.variables[s][:,:] for s in CM1_2dvar_list]
CM1_2dvar = dict(zip(CM1_2dvar_list, CM1_2dvar))

CM1_2dvar['zu_zi'] = [CM1_zu/pblh for pblh in CM1_PBLH]
CM1_2dvar['zw_zi'] = [CM1_zw/pblh for pblh in CM1_PBLH]

CM1_2dvar['uu_s'] = 2./3. * CM1_2dvar['tke_s']
CM1_2dvar['vv_s'] = 2./3. * CM1_2dvar['tke_s']
CM1_2dvar['ww_s'] = 2./3. * CM1_2dvar['tke_s']

# --------
# Variance
# --------
#NCARLES_variance_theta = NCARLES.variables['cc_cov'][:, 0, :]
#NCARLES_variance_q = NCARLES.variables['cc_cov'][:, 21, :]

# -----------------------------------
# Load CM1 spectra
# -----------------------------------
CM1_file = path_base + "/les/cm1/cm1_sas_spectra.nc"
CM1_spec = Dataset(CM1_file, mode='r')

CM1_nt  = len( CM1_spec.dimensions['nt'] )             # number of timesteps