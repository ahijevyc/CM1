#!/usr/bin/env python3

exec(open('import_packages.py').read())
exec(open('definitions.py').read())
exec(open('read_les_ncar.py').read())
exec(open('read_les_wrf.py').read())
exec(open('read_les_mpas.py').read())
exec(open('read_les_fe.py').read())
exec(open('read_les_dales.py').read())
exec(open('read_les_cm1.py').read())
exec(open('read_les_microhh.py').read())
exec(open('read_obs_lidar.py').read())
exec(open('read_obs_tower.py').read())
exec(open('read_obs_zi.py').read())
exec(open('read_scm_wrf.py').read())
exec(open('read_scm_scam.py').read())
exec(open('read_scm_cm1.py').read())
exec(open('read_scm_somcrus.py').read())

def plot_timeseries_1var(da,db,do,config):

    # ---- configure broad tick characteristics

    axp.tick_params(axis='both', which='both', direction='out', labelsize='large', pad=3)
    axp.tick_params(axis='both', which='major', length=5.5, width=1)
    axp.tick_params(axis='both', which='minor', length=3., width=0.7)
    axp.tick_params(axis='x', which='both', top='True')
    axp.tick_params(axis='y', which='both', right='True')

    # ---- configure markers for the observations

    mark = ['o', '+', '^', 's']
    mark_style = dict(color='black', linestyle='-', 
                      markersize=7, linewidth=0.0)

    if (len(do) > len(mark)):
        print('not enough markers defined, stopping')
        exit()
      
    # --- add data to each plot

    if (SCM == 'True'):
        n = db[0]
        axp.fill_between(x=n[0], y1=n[2], y2=n[3], facecolor=(0,0,0,.1), edgecolor=(0,0,0,.5),label=n[5])
        lp1 = axp.plot(n[0], n[1], color=n[4], linestyle='solid', linewidth=1.5)
        lp2 = axp.fill(np.NaN, np.NaN, facecolor=(0.9,0.9,0.9), edgecolor="None")
        lp3 = axp.fill(np.NaN, np.NaN, facecolor="None", edgecolor=(0.5,0.5,0.5),linewidth=1.5)
        ll  = n[5]

    for i in range(len(da)):
        n = da[i]
        axp.plot(n[0], n[1], color=n[2], linestyle=n[4], linewidth=2, label=n[3]) # ---- resolved quantities

#   for n in da:
#       axp.plot(n[0], n[1], color=n[2], linestyle=n[4],linewidth=2,label=n[3]) # ---- resolved quantities

    for i in range(len(do)):
        n = do[i]
        axp.plot(n[0], n[1], fillstyle='none', label=n[2], marker=mark[i], **mark_style)         # ---- observations

    # ---- set y-axis title

    axp.set_xlabel(config['x_title'], fontsize='x-large', labelpad=7)
    axp.set_ylabel(config['y_title'], fontsize='x-large', labelpad=7)

    # ---- x-ticks

    axp.set_xlim([config['xmin'], config['xmax']])
    axp.xaxis.set_major_locator(ticker.MultipleLocator(config['xfrq_major']))
    axp.xaxis.set_minor_locator(ticker.MultipleLocator(config['xfrq_major']/config['xfrq_minor']))

    # ---- y-ticks

    axp.set_ylim([config['ymin'], config['ymax']])
    axp.yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major']))
    axp.yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major']/config['yfrq_minor']))

    # ---- y-axis ticks for figures in right-hand column

    axp.xaxis.set_ticks_position('both')

    axp.yaxis.set_label_position("left")
    axp.yaxis.set_ticks_position('both')

    # ---- add marker lines

    if (var == 'wt') or (var == 'wq') or (var == 'oblen'):
        axp.axhline(y=0.0, color='black', linewidth=0.3)

    # ---- add legend

    if (var == 'wt') or (var == 'wq') or (var == 'wstar'):
        lgnd_box_x = 0.5
        lgnd_box_y = 0.0
        lloc = 'lower center'
        if (var == 'wstar'):
            ncol = 2
        else:
            ncol = 3
    elif (var == 'zi_t'):
        lgnd_box_x = 1.0
        lgnd_box_y = 0.0
        lloc = 'lower right'
        if (SCM == 'True'):
            ncol = 3
        else:
            ncol = 2
    elif (var == 'zi_q'):
        lgnd_box_x = 1.0
        lgnd_box_y = 0.0
        lloc = 'lower right'
        ncol = 2
    elif (var == 'ustar'):
        lgnd_box_x = 0.5
        lgnd_box_y = 0.0
        lloc = 'lower center'
        ncol = 2
    elif (var == 'oblen'):
        lgnd_box_x = 0.03
        lgnd_box_y = 0.0
        lloc = 'lower left'
        ncol = 2
    else:
        lgnd_box_x = 0.0
        lgnd_box_y = 1.0
        lloc = 'upper left'
        ncol = 2

    if (SCM == 'True'):

        # ---- move LES-AVG to front of the list and modify its handle

        handles, labels = axp.get_legend_handles_labels()
        llabel = labels[-1]                        # grab last label in the list
        handles = handles[:-1]                     # eliminate last entry from the handles list
        labels = labels[:-1]                       # eliminate last entry from the labels list
        handles.insert(0,(lp2[0],lp1[0],lp3[0]))   # insert new handle at the front of the list
        labels.insert(0,llabel)                    # inster new label  at the front of th list

        axp.legend(handles,labels,
               fontsize='small', frameon='True', borderpad=0.5,
               bbox_to_anchor=(lgnd_box_x, lgnd_box_y), loc=lloc, framealpha=1.0,
               borderaxespad=0.7, handlelength=2.8, handletextpad=0.6,
               labelspacing=0.3, edgecolor='dimgray',ncol=ncol, columnspacing=1.0)

    else:

        axp.legend(fontsize='small', frameon='True', borderpad=0.5,
               bbox_to_anchor=(lgnd_box_x, lgnd_box_y), loc=lloc, framealpha=1.0,
               borderaxespad=0.7, handlelength=2.8, handletextpad=0.6,
               labelspacing=0.3, edgecolor='dimgray',ncol=ncol, columnspacing=1.0)

    # ---- add title to right-hand y-axis

    axc = axp.twinx()
    axc.tick_params(axis='y', which='both', direction='out', labelsize='large', pad=3, right='True')
    axc.tick_params(axis='y', which='major', length=5.5, width=1)
    axc.tick_params(axis='y', which='minor', length=3., width=0.7)
    axc.set_ylabel(config['y_title'], fontsize='x-large', labelpad=7)
    axc.set_ylim([config['ymin'], config['ymax']])
    axc.yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major']))
    axc.yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major']/config['yfrq_minor']))

    # ---- push axc axis to the back so that the axis doesn't 
    #      overlay the legends that are placed outside the frame

    axp.set_zorder(2)
    axc.set_zorder(1)

    return axp

# -------------------------------

# --- set fonts

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['font.size'] = 16
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r"\usepackage{pslatex} \usepackage{amsmath}"

# --- add edges to all plots 

plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1

# ---- set output type

single_file = 0    # =0, individual files; =1, export all figs to single file
output_file_type = 0    # =0, PDF; =1, PNG (only works with: single_file=0)

# ---- set whether we're plotting LES or SCM data

#SCM = 'False'
SCM = 'True'

# ---- set datasets and variables to plot

if (SCM is 'False'):
#   data2plot = [ 'CM1', 'FE', 'MPAS', 'NCAR', 'WRF', 'OBS' ]
    data2plot = [ 'CM1', 'DALES', 'FE', 'MICROHH', 'MPAS', 'NCAR', 'WRF', 'OBS' ]
#   data2plot = [ 'CM1', 'DALES', 'MPAS', 'NCAR', 'WRF', 'OBS' ]
elif (SCM is 'True'):
#   data2plot = [ 'CM1', 'FE', 'MPAS', 'NCAR', 'WRF', \
#                 'YSUh', 'YSUh_nwspb', 'MYNNh', 'MYNNh_nwspb', 'SOMCRUS', 'SCAM', 'CM1_CLUBB', 'CM1_MYJ', 'OBS' ]
    data2plot = [ 'CM1', 'FE', 'MPAS', 'MICROHH', 'MPAS', 'NCAR', 'WRF', \
                  'YSUh', 'MYNNh', 'SOMCRUS', 'SCAM', 'CM1_CLUBB', 'CM1_MYJ', 'OBS' ]

vars2plot = [ 'wt', 'wq', 'zi_t', 'zi_q', 'ustar', 'wstar', 'oblen' ]

# ----- select the output style

figs2plot = [ 'timeseries' ]

# --- specify averaging duration (in 5-min chunks, i.e. 12 = 60 min avg)

num = 12  # number of data points in rolling average centered at time
#num = 6  # number of data points in rolling average centered at time

# --- build time variables

FE_time_ind_6AM = np.argmin(np.abs(FE['time'] - 6))
WRFLES_time_ind_6AM = np.argmin(np.abs(WRFLES_time_hr - 6))
WRFSCM_time_ind_8AM = 1+np.argmin(np.abs(WRFSCM_Hr_frac_ysu_hires - 8))  # 1+ because WRFSCM data starts 5min late
DALES_time_ind_6AM = np.argmin(np.abs(DALES_time_hr - 6))
NCARLES_time_ind_8AM = np.argmin(np.abs(NCARLES_time_hr - 8))
CM1_time_ind_6AM = np.argmin(np.abs(CM1_time_hr - 6))
CM1SCM_time_ind_8AM = np.argmin(np.abs(CM1_CLUBB_time_hr - 8))
SOMCRUS_time_ind_8AM = np.argmin(np.abs(SOMCRUS_time_hr - 8))
MICROHH_time_ind_6AM = np.argmin(np.abs(MICROHH_time_hr - 6))

# --- set output file name for single_file

if (single_file == 1):
    if (SCM is 'True'):
        pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_timeseries.scm.all.pdf")
    elif (SCM is 'False'):
        pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_timeseries.all.pdf")

# ---- loop over plot type

for figs in figs2plot:

    print(' working on: ',figs)

    # ---- begin plotting

    for var in vars2plot:                      # loop over variable to plot

        print('     var: ',var)

        da = []
        db = []
        do = []
        dc = []
        dl = []

        for id in range(len(data2plot)):       # loop over data types, i.e. LES, SCM, OBS

            if data2plot[id] == 'FE':                              # ---- FastEddy

                clabel = 'FastEddy'
                color = 'mediumseagreen'
                linestyle = 'solid'
    
                if var == 'zi_t':
                    var_p = 'pblhth'
                    fac = 1.e-3  # convert [m] -> [km]
                elif var == 'zi_q':
                    var_p = 'pblhq'
                    fac = 1.e-3  # convert [m] -> [km]
                elif var == 'ustar':
                    var_p = 'fricvel'
                    fac = 1.
                elif var == 'wstar':
                    var_p = 'wstar'
                    fac = 1.
                elif var == 'wt':
                    var_p = 'htflux'
                    fac = 1.
                elif var == 'wq':
                    var_p = 'qflux'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif var == 'oblen':
                    var_p = 'oblen'
                    fac = 1.

                da_fe = FE[var_p]

                if (SCM == 'False'):
                    da.append((FE['time'], fac*da_fe, color, clabel, linestyle))   # add data to list
                else:
                    fe_t = NCARLES_time_hr                      # because FE data not at frequency consistent 
                    fe_d = np.interp(fe_t, FE['time'], da_fe)   #    with the other LES data, interpolate FE data 
                    dl.append((fe_t, fac*fe_d))                 #    to NCAR-LES time when calculating LES-AVG

            elif data2plot[id] == 'WRF':

                clabel = 'WRF'
                color = 'blue'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_wrf = np.array(WRFLES.variables[var_p])

                if (SCM == 'False'):
                    da.append((WRFLES_time_hr, fac*da_wrf, color, clabel, linestyle))  # add data to list
                else:
                    dl.append((WRFLES_time_hr[1:], fac*da_wrf[1:]))

            elif data2plot[id] == 'MPAS':

                clabel = 'MPAS'
                color = 'dimgray'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_mpas = np.array(MPAS.variables[var_p])

                if (SCM == 'False'):
                    da.append((MPAS_time_hr, fac*da_mpas, color, clabel, linestyle))  # add data to list
                else:
                    dl.append((MPAS_time_hr[1:], fac*da_mpas[1:]))

            elif data2plot[id] == 'DALES':    # --- DALES

                clabel = 'DALES'
                color = 'crimson'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_dales = DALES.variables[var_p][:]

                if (SCM == 'False'):
                    if np.isfinite(DALES.variables[var_p][:]).any():
                        da.append((DALES_time_hr, fac*da_dales, color, clabel, linestyle))  # add data to list
                else:
                    if np.isfinite(DALES.variables[var_p][:]).any():
                        dl.append((DALES_time_hr, fac*da_dales))  # add data to list

            elif data2plot[id] == 'MICROHH':    # --- MICROHH

                clabel = 'MicroHH'
                color = 'cyan'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'thl_diff_surf'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'qt_diff_surf'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_microhh = MICROHH.variables[var_p][:]

                if (SCM == 'False'):
                    if np.isfinite(MICROHH.variables[var_p][:]).any():
                        da.append((MICROHH_time_hr, fac*da_microhh, color, clabel, linestyle))  # add data to list
                else:
                    if np.isfinite(MICROHH.variables[var_p][:]).any():
                        dl.append((MICROHH_time_hr, fac*da_microhh))  # add data to list

            elif data2plot[id] == 'CM1':    # --- CM1
    
                clabel = 'CM1'
                color = 'magenta'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_cm1 = CM1.variables[var_p][:]

                if (SCM == 'False'):
                    da.append((CM1_time_hr, fac*da_cm1, color, clabel, linestyle))  # add data to list
                else:
                    dl.append((CM1_time_hr, fac*da_cm1))

            elif data2plot[id] == 'NCAR':    # --- NCARLES
    
                clabel = 'NCAR-LES'
                color = 'orange'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_ncar = np.array(NCARLES.variables[var_p])

                if (SCM == 'False'):
                    da.append((NCARLES_time_hr, fac*da_ncar, color, clabel, linestyle))  # add data to list
                else:
                    dl.append((NCARLES_time_hr, fac*da_ncar))

            elif data2plot[id] == 'SCAM':    # --- SCAM
    
                clabel = 'SCAM'
                color = 'cyan'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    continue
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'wstar'):
                    continue
                elif (var == 'oblen'):
                    continue
        
                da_scam = SCAM.variables[var_p][:]
                if np.isfinite(SCAM.variables[var_p][:]).any():
                    da.append((SCAM_time_hr, fac*da_scam, color, clabel, linestyle))  # add data to list
    
            elif data2plot[id] == 'YSUh':

                clabel = 'WRF-YSU'
                color = 'blue'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'PBLH'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    continue
                elif (var == 'ustar'):
                    var_p = 'UST'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_ysu = np.array(WRFSCM_2dvar_ysu_hires[var_p][WRFSCM_time_ind_8AM:])
                da.append((WRFSCM_Hr_frac_ysu_hires[WRFSCM_time_ind_8AM:], fac*da_ysu, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'YSUh_nwspb':

                clabel = 'WRF-YSU-m'
                color = 'blue'
                linestyle = 'dashed'

                if (var == 'zi_t'):
                    var_p = 'PBLH'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    continue
                elif (var == 'ustar'):
                    var_p = 'UST'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_ysu = np.array(WRFSCM_2dvar_ysu_hires_no_wsp_boost[var_p][WRFSCM_time_ind_8AM:])
                da.append((WRFSCM_Hr_frac_ysu_hires_no_wsp_boost[WRFSCM_time_ind_8AM:], fac*da_ysu, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'MYNNh':

                clabel = 'WRF-MYNN'
                color = 'magenta'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'PBLH'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    continue
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'UST'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_mynn = np.array(WRFSCM_2dvar_mynn_hires[var_p][WRFSCM_time_ind_8AM:])
                da.append((WRFSCM_Hr_frac_mynn_hires[WRFSCM_time_ind_8AM:], fac*da_mynn, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'MYNNh_nwspb':

                clabel = 'WRF-MYNN-m'
                color = 'magenta'
                linestyle = 'dashed'

                if (var == 'zi_t'):
                    var_p = 'PBLH'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    continue
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'UST'
                    fac = 1
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'oblen'
                    fac = 1.

                da_mynn = np.array(WRFSCM_2dvar_mynn_hires_no_wsp_boost[var_p][WRFSCM_time_ind_8AM:])
                da.append((WRFSCM_Hr_frac_mynn_hires_no_wsp_boost[WRFSCM_time_ind_8AM:], fac*da_mynn, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'YSUl':

                clabel = 'WRF-YSU-lo'
                color = 'blue'
                linestyle = 'dashed'

                if (var == 'zi_t'):
                    var_p = 'PBLH'

                da_ysu = list(WRFSCM_2dvar_ysu_lores[var_p])
                da.append((WRFSCM_Hr_frac_ysu_lores, da_ysu, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'MYNNl':

                clabel = 'WRF-MYNN-lo'
                color = 'orange'
                linestyle = 'dashed'

                if (var == 'zi_t'):
                    var_p = 'PBLH'

                da_ysu = list(WRFSCM_2dvar_mynn_lores[var_p])
                da.append((WRFSCM_Hr_frac_mynn_lores, da_ysu, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'CM1_CLUBB':    # --- CM1-CLUBB
    
                clabel = 'CM1-CLUBBX'
                color = 'darkkhaki'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_cm1 = CM1_CLUBB.variables[var_p][:]
                if np.isfinite(CM1_CLUBB.variables[var_p][:]).any():
                    da.append((CM1_CLUBB_time_hr, fac*da_cm1, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'CM1_MYJ':    # --- CM1-MYJ
    
                clabel = 'CM1-MYJ'
                color = 'darkkhaki'
                linestyle = 'dashed'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.

                da_cm1 = CM1_MYJ.variables[var_p][:]
                if np.isfinite(CM1_MYJ.variables[var_p][:]).any():
                    da.append((CM1_MYJ_time_hr, fac*da_cm1, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'CM1_MYNN_2.5':    # --- CM1-MYJ
    
                clabel = 'CM1-MYNN2.5'
                color = 'darkkhaki'
                linestyle = 'dashdot'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.

                da_cm1 = CM1_MYNN25.variables[var_p][:]
                if np.isfinite(CM1_MYNN25.variables[var_p][:]).any():
                    da.append((CM1_MYNN25_time_hr, fac*da_cm1, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'CM1_MYNN_3.0':    # --- CM1-MYNN-3.0
    
                clabel = 'CM1-MYNN3.0'
                color = 'darkkhaki'
                linestyle = 'dotted'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    var_p = 'zi_q'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.

                da_cm1 = CM1_MYNN30.variables[var_p][:]
                if np.isfinite(CM1_MYNN30.variables[var_p][:]).any():
                    da.append((CM1_MYNN30_time_hr, fac*da_cm1, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'SOMCRUS':    # --- SOMCRUS-CLUBB
    
                clabel = 'SOMCRUS'
                color = 'orange'
                linestyle = 'solid'

                if (var == 'zi_t'):
                    var_p = 'zi_t'
                    fac = 1.e-3  # convert [m] -> [km]
                elif (var == 'zi_q'):
                    continue
                elif (var == 'ustar'):
                    var_p = 'ustar'
                    fac = 1.
                elif (var == 'wstar'):
                    var_p = 'wstar'
                    fac = 1.
                elif (var == 'wt'):
                    var_p = 'wtsfc'
                    fac = 1.
                elif (var == 'wq'):
                    var_p = 'wqsfc'
                    fac = 1.e3  # convert [kg/kg] -> [g/kg]
                elif (var == 'oblen'):
                    var_p = 'amonin'
                    fac = 1.
        
                da_somcrus = SOMCRUS.variables[var_p][:]
                if np.isfinite(SOMCRUS.variables[var_p][:]).any():
                    da.append((SOMCRUS_time_hr, fac*da_somcrus, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'OBS':    # --- Observations
    
                if (var == 'zi_t') or (var == 'zi_q'):
    
                    clabel = 'Ceilometer'
                    fac = 1.e-3  # convert [m] -> [km]
                    do.append((zi_time, fac*zi_ceilometer, clabel))

                    clabel = 'Wind Profiler'
                    fac = 1.e-3  # convert [m] -> [km]
                    do.append((zi_time, fac*zi_profiler, clabel))

                    clabel = 'Sounding'
                    fac = 1.e-3  # convert [m] -> [km]
                    do.append((zi_time, fac*zi_sounding, clabel))

                elif (var == 'ustar'):
    
                    continue
                    clabel = 'Tower'
                    do.append((TOWER_time_hr, tower_ustar, clabel))

                elif (var == 'wt'):
    
                    clabel = 'Tower'
                    do.append((TOWER_time_hr, tower_wt, clabel))

                elif (var == 'wq'):
    
                    clabel = 'Tower'
                    do.append((TOWER_time_hr, tower_wq, clabel))

                elif (var == 'oblen'):
    
                    continue
                    clabel = 'Tower'
                    do.append((TOWER_time_hr, tower_oblen, clabel))

        # ---- if we're plotting SCM results, calculate an average LES result

        if (SCM == 'True'):

            # ---- declare some variables

            nc,nv,nt = np.shape(dl)

            dl_t = np.empty((nc,nt), dtype=float)
            dl_d = np.empty((nc,nt), dtype=float)

            nnt = nt - NCARLES_time_ind_8AM + 1
            dl_t_avg = np.empty((nnt), dtype=float)
            dl_d_avg = np.empty((nnt), dtype=float)
            dl_d_min = np.empty((nnt), dtype=float)
            dl_d_max = np.empty((nnt), dtype=float)

            # ---- grab profile data from within data structure

            for ic in range(nc):
                n = dl[ic]
                dl_t[ic,:] = n[0]  # time
                dl_d[ic,:] = n[1]  # data

            # ---- fill temp variable with data from different
            #      LES codes, but at like-times, calculate stats

            iit = -1
            for it in range(nt):
                if (it >= NCARLES_time_ind_8AM - 1):
                    iit = iit + 1
                    dl_t_avg[iit] = dl_t[-1,it]          # currently plotting against time variable from the last LES dataset
                    dl_d_avg[iit] = np.mean(dl_d[:,it], axis=0)
                    dl_d_min[iit] = np.min (dl_d[:,it], axis=0)
                    dl_d_max[iit] = np.max (dl_d[:,it], axis=0)

            color = (0,0,0,.6)
            db.append((dl_t_avg, dl_d_avg,
                       dl_d_min, dl_d_max,
                       color, 'LES-AVG'))
    

        # ---- setup axis ticks and titles for the current variable
    
        if (var == 'zi_t') or (var == 'zi_q'):

            ymin = 0.0
            ymax = 2.6
            yfrq_major = 1
            yfrq_minor = 5

            if (var == 'zi_t'):
                y_title = r"$z_i~~(\delta \theta)$~~[km]"
            elif (var == 'zi_q'):
                y_title = r"$z_i~~(\delta q)$~~[km]"

        elif (var == 'ustar'):

            ymin = 0.0
            ymax = 0.45
            yfrq_major = 0.1
            yfrq_minor = 4
            y_title = r"$u_{\ast}$~~[m s$^{-1}$]"

        elif (var == 'wstar'):

            ymin = 0.8
            ymax = 2.2
            yfrq_major = 1.0
            yfrq_minor = 5
            y_title = r"$w_{\ast}$~~[m s$^{-1}$]"

        elif (var == 'wt'):

            ymin = -0.02
            ymax = 0.18
            yfrq_major = 0.1
            yfrq_minor = 5
            y_title = r"$\overline{w'\theta'}_{sfc}$~~[m K s$^{-1}$]"

        elif (var == 'wq'):

            ymin = -0.02
            ymax = 0.18
            yfrq_major = 0.1
            yfrq_minor = 5
            y_title = r"$\overline{w'q'}_{sfc}$~~[m s$^{-1}$ g kg$^{-1}$]"

        elif (var == 'oblen'):

#           ymin = -45.0
            ymin = -85.0
            ymax = 0
            yfrq_major = 20
            yfrq_minor = 4
            y_title = r"$L_{_{MO}}$~~[m]"

        # ---- x-axis is the same for all profile plots

        if (SCM == 'False'):
            xmin = 6.
        else:
            xmin = 8.
        xmax = 18.0
        xfrq_major = 1
        xfrq_minor = 4
        x_title = "Time [hr LT]"
    
        ticks_titles = {'xmin': xmin, 'xmax': xmax, 'xfrq_major': xfrq_major, 'xfrq_minor': xfrq_minor, 'x_title': x_title,
                        'ymin': ymin, 'ymax': ymax, 'yfrq_major': yfrq_major, 'yfrq_minor': yfrq_minor, 'y_title': y_title}
    
        # ---- build plot

        if (figs == 'timeseries'):

            axp = [None]
            fig = plt.figure(figsize=(12, 4))
            axp = fig.add_subplot()
            plt.subplots_adjust(top=0.95, bottom=0.21, left=0.09, right=0.91)
        
            # ---- create the plots 
            
            plot_timeseries_1var(da, db, do, ticks_titles)    # create line plots
        
        # ---- export file

        if (single_file == 0):
            if (SCM is 'True'):
                if (output_file_type == 0):
                    plt.savefig("../plots/pdf/met_timeseries.scm."+var+".pdf")
                elif (output_file_type == 1):
                    plt.savefig("../plots/png/met_timeseries.scm."+var+".png", dpi=600, bbox_inches='tight')
            elif (SCM is 'False'):
                if (output_file_type == 0):
                    plt.savefig("../plots/pdf/met_timeseries."+var+".pdf")
                elif (output_file_type == 1):
                    plt.savefig("../plots/png/met_timeseries."+var+".png", dpi=600, bbox_inches='tight')
        else:
            pdf.savefig( fig )

if (single_file == 1):
    pdf.close()
