#!/usr/bin/env python3

exec(open('import_packages.py').read())
exec(open('definitions.py').read())
exec(open('read_les_ncar.py').read())
exec(open('read_les_wrf.py').read())
exec(open('read_les_fe.py').read())
exec(open('read_les_dales.py').read())
exec(open('read_les_cm1.py').read())
exec(open('read_les_mpas.py').read())
exec(open('read_obs_lidar.py').read())
exec(open('read_obs_C130_met.py').read())
#exec(open('define_scm_wrf.py').read())
#exec(open('read_scm_wrf.py').read())

def plot_profile_2var_1x2 (d1a,d1b,d1c,d1t,d2a,d2b,d2c,d2t,config):

    # ---- function to plot two sets of vertical profiles of two variables each 
    #      (e.g. total + sgs) laid out in a 1row x 2column two-panel arrangement 
    #
    #   NOTE: in order to enable modification to the figure following a call to this
    #         routine, the routine does not show or close the plot, or export a file.

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(8,4))
    plt.subplots_adjust(top=0.95, bottom=0.16, left=0.09, right=0.91, hspace=0.2, wspace=0.11)

    for ax in axs.flat:
        ax.tick_params(axis='both', which='both', direction='out', labelsize='small', pad=3)
        ax.tick_params(axis='both', which='major', length=5.5, width=1)
        ax.tick_params(axis='both', which='minor', length=3., width=0.7)
        ax.tick_params(axis='x', which='both', top='True')
        ax.tick_params(axis='y', which='both', right='True')

    marker_style_c = dict(color='black', linestyle='-', marker='o',
                    markersize=5, linewidth=0.0)

    marker_style_t = dict(color='black', linestyle='-', marker='^',
                    markersize=5, linewidth=0.0)

    # --- add lines to left plot [0]

    for n in d1b:
        axs[0].plot(n[0], n[1], color=n[2], linestyle='dashed',linewidth=1.2)
    for n in d1a:
        axs[0].plot(n[0], n[1], color=n[2], linestyle='solid',linewidth=2,label=n[3])
    for n in d1c:
#       axs[0].plot(n[0], n[1], fillstyle='none', label=n[2], **marker_style)
        axs[0].errorbar(n[0], n[1], zorder=5, xerr=n[2], elinewidth=0.5, fillstyle='none', label=n[3], **marker_style_c)
    for n in d1t:
        axs[0].errorbar(n[0], n[1], zorder=5, xerr=n[2], elinewidth=0.5, fillstyle='none', label=n[3], **marker_style_t)


    # --- add lines to right plot [1]

    for n in d2b:
        axs[1].plot(n[0], n[1], color=n[2], linestyle='dashed',linewidth=1.2)
    for n in d2a:
        axs[1].plot(n[0], n[1], color=n[2], linestyle='solid',linewidth=2)
    for n in d2c:
#       axs[1].plot(n[0], n[1], fillstyle='none', label=n[2], **marker_style)
        axs[1].errorbar(n[0], n[1], zorder=5, xerr=n[2], elinewidth=0.5, fillstyle='none', label=n[3], **marker_style_c)
    for n in d2t:
        axs[1].errorbar(n[0], n[1], zorder=5, xerr=n[2], elinewidth=0.5, fillstyle='none', label=n[3], **marker_style_t)

    # ---- set x-axis title

    axs[0].set_xlabel(config['x_title'][0], fontsize='medium', labelpad=5)
    axs[1].set_xlabel(config['x_title'][1], fontsize='medium', labelpad=5)

    # ---- set y-axis title

    axs[0].set_ylabel(config['y_title'][0], fontsize='medium', labelpad=7)
    axs[1].set_ylabel(config['y_title'][1], fontsize='medium', labelpad=7)

    # ---- x-ticks

    axs[0].set_xlim([config['xmin'][0], config['xmax'][0]])
    axs[0].xaxis.set_major_locator(ticker.MultipleLocator(config['xfrq_major'][0]))
    axs[0].xaxis.set_minor_locator(ticker.MultipleLocator(config['xfrq_major'][0]/config['xfrq_minor'][0]))

    axs[1].set_xlim([config['xmin'][1], config['xmax'][1]])
    axs[1].xaxis.set_major_locator(ticker.MultipleLocator(config['xfrq_major'][1]))
    axs[1].xaxis.set_minor_locator(ticker.MultipleLocator(config['xfrq_major'][1]/config['xfrq_minor'][1]))

    # ---- y-axis

    for ax in axs.flat:
        ax.set_ylim([config['ymin'], config['ymax']])
        ax.yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major']))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major']/config['yfrq_minor']))

    # ---- y-axis ticks for figures in right-hand column

    axs[1].yaxis.set_label_position("right")
    axs[1].yaxis.tick_right()
    axs[1].yaxis.set_ticks_position('both')

    # ---- add legend to left plot

    axs[0].legend(loc='best',fontsize='x-small', frameon='True', borderpad=0.5, \
                  borderaxespad=0.7, handlelength=2.8, handletextpad=0.6, \
                  labelspacing=0.3, edgecolor='dimgray')

    return axs

# -------------------------------


# --- set fonts

plt.rcParams.update({
   "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 14,
    "text.usetex": True})

# --- add edges to all plots 

plt.rcParams.update({
    "axes.edgecolor": "black",
    "axes.linewidth": 1})


# =======================
# Set: what time to plot?
# =======================

time2plot = 12.0

WRFLES_time_ind = np.argmin(np.abs(WRFLES_time_hr - time2plot))
MPAS_time_ind = np.argmin(np.abs(MPAS_time_hr - time2plot))
NCARLES_time_ind = np.argmin(np.abs(NCARLES_time_hr - time2plot))
FE_time_ind = np.argmin(np.abs(FE['time'] - time2plot))
CM1_time_ind = np.argmin(np.abs(CM1_time_hr - time2plot))
DALES_time_ind = np.argmin(np.abs(DALES_time_hr - time2plot))
LIDAR_time_ind = np.argmin(np.abs(LIDAR_time_hr - time2plot))

# --- specify averaging duration (in 5-min chunks, i.e. 12 = 60 min avg)

num = 12  # number of data points in rolling average centered at time
#num = 6  # number of data points in rolling average centered at time

# --- declare list that will be used for generic plotting

d1a = []
d1b = []
d1c = []
d1t = []
d2a = []
d2b = []
d2c = []
d2t = []

# --- build z/zi grid into which data will be interpolated

z_grid = 0   # =0 -> km 
             # =1 -> z/zi
             # =2 -> data interpolated in to z/zi grid

nt,nk = np.shape(NCARLES_2dvar['zu_zi'])
zwi = np.empty([nk], dtype=object)

ztop = 1500.
zl = 3000
zwi = np.linspace(0,zl,nk) / ztop

# --- CM1

color_cm1 = 'magenta'

facq = 1000. # convert from kg/kg to g/kg
facz = 1.e-3 # convert to [km]

if z_grid == 0 or z_grid ==1:
    if z_grid == 0:
        zzw = CM1.variables['zw'][CM1_time_ind] * facz
    elif z_grid == 1:
        zzw = CM1_2dvar['zw_zi'][CM1_time_ind]
    d1a_int = CM1_2dvar['wt_r'] + CM1_2dvar['wt_s']
    d1b_int = CM1_2dvar['wt_s']
    d2a_int = (CM1_2dvar['wq_r'] + CM1_2dvar['wq_s'])*facq 
    d2b_int = CM1_2dvar['wq_s'] * facq
else:
   zzw = zwi
   nt,nk = np.shape(CM1_2dvar['zw_zi'])
   d1a_int = [np.interp(zzw,CM1_2dvar['zw_zi'][i],CM1_2dvar['wt_r'][i]+CM1_2dvar['wt_s'][i]) for i in range(nt)]
   d1b_int = [np.interp(zzw,CM1_2dvar['zw_zi'][i],CM1_2dvar['wt_s'][i]) for i in range(nt)]
   d2a_int = [np.interp(zzw,CM1_2dvar['zw_zi'][i],(CM1_2dvar['wq_r'][i]+CM1_2dvar['wq_s'][i])*facq) for i in range(nt)]
   d2b_int = [np.interp(zzw,CM1_2dvar['zw_zi'][i],(CM1_2dvar['wq_s'][i])*facq) for i in range(nt)]

d1a_cm1 = rollavg_pandas(d1a_int, num)  # centered time average
d1b_cm1 = rollavg_pandas(d1b_int, num)
d2a_cm1 = rollavg_pandas(d2a_int, num)
d2b_cm1 = rollavg_pandas(d2b_int, num)

d1a.append((d1a_cm1[CM1_time_ind], zzw, color_cm1,'CM1'))  # add data to list
d1b.append((d1b_cm1[CM1_time_ind], zzw, color_cm1))
d2a.append((d2a_cm1[CM1_time_ind], zzw, color_cm1,'CM1'))
d2b.append((d2b_cm1[CM1_time_ind], zzw, color_cm1))

# --- DALES

color_dales = 'crimson'

facq = 1000. # convert from kg/kg to g/kg
facz = 1.e-3 # convert to [km]

if z_grid == 0 or z_grid ==1:
    if z_grid == 0:
        zzw = DALES.variables['zw'][DALES_time_ind] * facz
    elif z_grid == 1:
        zzw = DALES_2dvar['zw_zi'][DALES_time_ind]
    d1a_int = DALES_2dvar['wt_r'] + DALES_2dvar['wt_s']
    d1b_int = DALES_2dvar['wt_s']
    d2a_int = (DALES_2dvar['wq_r'] + DALES_2dvar['wq_s'])*facq 
    d2b_int = DALES_2dvar['wq_s'] * facq
else:
   zzw = zwi
   nt,nk = np.shape(DALES_2dvar['zw_zi'])
   d1a_int = [np.interp(zzw,DALES_2dvar['zw_zi'][i],DALES_2dvar['wt_r'][i]+DALES_2dvar['wt_s'][i]) for i in range(nt)]
   d1b_int = [np.interp(zzw,DALES_2dvar['zw_zi'][i],DALES_2dvar['wt_s'][i]) for i in range(nt)]
   d2a_int = [np.interp(zzw,DALES_2dvar['zw_zi'][i],(DALES_2dvar['wq_r'][i]+DALES_2dvar['wq_s'][i])*facq) for i in range(nt)]
   d2b_int = [np.interp(zzw,DALES_2dvar['zw_zi'][i],(DALES_2dvar['wq_s'][i])*facq) for i in range(nt)]

d1a_dales = rollavg_pandas(d1a_int, num)  # centered time average
d1b_dales = rollavg_pandas(d1b_int, num)
d2a_dales = rollavg_pandas(d2a_int, num)
d2b_dales = rollavg_pandas(d2b_int, num)

# ---- comment out DALES for now
d1a.append((d1a_dales[DALES_time_ind], zzw, color_dales,'DALES'))  # add data to list
d1b.append((d1b_dales[DALES_time_ind], zzw, color_dales))
d2a.append((d2a_dales[DALES_time_ind], zzw, color_dales,'DALES'))
d2b.append((d2b_dales[DALES_time_ind], zzw, color_dales))

# --- FastEddy

color_fe = 'mediumseagreen'

facq = 1. # already in [g/kg]
facz = 1.e-3 # convert to [km]

if z_grid == 0 or z_grid ==1:
    if z_grid == 0:
        zzw = FE['z'][FE_time_ind] * facz
    elif z_grid == 1:
        zzw = FE['zw_zi'][FE_time_ind]
    d1a_int = FE['wth_t']
    d1b_int = FE['wth_s']
    d2a_int = FE['wqv_t'] * facq
    d2b_int = FE['wqv_s'] * facq
else:
    nt,nk = np.shape(FE['zw_zi'])        # FE only used 186 vertical levels.
    zl = 2790.
    zzw = np.linspace(0,zl,nk) / ztop
    d1a_int = [np.interp(zzw,FE['zw_zi'][i],FE['wth_t'][i]) for i in range(nt)]
    d1b_int = [np.interp(zzw,FE['zw_zi'][i],FE['wth_s'][i]) for i in range(nt)]
    d2a_int = [np.interp(zzw,FE['zw_zi'][i],FE['wqv_t'][i]*facq) for i in range(nt)]
    d2b_int = [np.interp(zzw,FE['zw_zi'][i],FE['wqv_s'][i]*facq) for i in range(nt)]

d1a_fe = rollavg_pandas(d1a_int, num)  # centered time average
d1b_fe = rollavg_pandas(d1b_int, num)
d2a_fe = rollavg_pandas(d2a_int, num)
d2b_fe = rollavg_pandas(d2b_int, num)

#d1a.append((d1a_fe[FE_time_ind], zzw, color_fe,'FastEddy'))   # add data to list
#d1b.append((d1b_fe[FE_time_ind], zzw, color_fe))
#d2a.append((d2a_fe[FE_time_ind], zzw, color_fe,'FastEddy'))
#d2b.append((d2b_fe[FE_time_ind], zzw, color_fe))

# ---- MPAS 

color_mpas = 'gray'
facq = 1. # already in g/kg

if z_grid == 0 or z_grid ==1:
    izs = 1
    if z_grid == 0:
        zzw = MPAS_zw[izs:] * facz
    elif z_grid == 1:
        zzw = MPAS_2dvar['zw_zi'][MPAS_time_ind]
    d1a_int = MPAS_2dvar['wt_r'][:,izs:] + MPAS_2dvar['wt_s'][:,izs:]
    d1b_int = MPAS_2dvar['wt_s'][:,izs:]
    d2a_int = (MPAS_2dvar['wq_r'][:,izs:] + MPAS_2dvar['wq_s'][:,izs:]) * facq
    d2b_int = (MPAS_2dvar['wq_s'][:,izs:]) * facq
else:
   zzw = zwi
   nt,nk = np.shape(MPAS_2dvar['zw_zi'])
   d1a_int = [np.interp(zzw,MPAS_2dvar['zw_zi'][i],MPAS_2dvar['wt_r'][i]+MPAS_2dvar['wt_s'][i]) for i in range(nt)]
   d1b_int = [np.interp(zzw,MPAS_2dvar['zw_zi'][i],MPAS_2dvar['wt_s'][i]) for i in range(nt)]
   d2a_int = [np.interp(zzw,MPAS_2dvar['zw_zi'][i],(MPAS_2dvar['wq_r'][i]+MPAS_2dvar['wq_s'][i])*facq) for i in range(nt)]
   d2b_int = [np.interp(zzw,MPAS_2dvar['zw_zi'][i],(MPAS_2dvar['wq_s'][i])*facq) for i in range(nt)]

d1a_mpas = rollavg_pandas(d1a_int, num)  # centered time average
d1b_mpas = rollavg_pandas(d1b_int, num)
d2a_mpas = rollavg_pandas(d2a_int, num) 
d2b_mpas = rollavg_pandas(d2b_int, num)

d1a.append((d1a_mpas[MPAS_time_ind], zzw, color_mpas,'MPAS'))  # add data to list
d1b.append((d1b_mpas[MPAS_time_ind], zzw, color_mpas))
d2a.append((d2a_mpas[MPAS_time_ind], zzw, color_mpas,'MPAS'))
d2b.append((d2b_mpas[MPAS_time_ind], zzw, color_mpas))


# --- NCARLES

color_ncar = 'orange'
facq = 1000. # convert from kg/kg to g/kg

if z_grid == 0 or z_grid ==1:
    if z_grid == 0:
        zzw = NCARLES.variables['zw'][NCARLES_time_ind] * facz
    elif z_grid == 1:
        zzw = NCARLES_2dvar['zw_zi'][NCARLES_time_ind]
    d1a_int = NCARLES_2dvar['wt_r'] + NCARLES_2dvar['wt_s']
    d1b_int = NCARLES_2dvar['wt_s']
    d2a_int = (NCARLES_2dvar['wq_r'] + NCARLES_2dvar['wq_s']) * facq
    d2b_int = (NCARLES_2dvar['wq_s']) * facq
else:
   zzw = zwi
   nt,nk = np.shape(NCARLES_2dvar['zw_zi'])
   d1a_int = [np.interp(zzw,NCARLES_2dvar['zw_zi'][i],NCARLES_2dvar['wt_r'][i]+NCARLES_2dvar['wt_s'][i]) for i in range(nt)]
   d1b_int = [np.interp(zzw,NCARLES_2dvar['zw_zi'][i],NCARLES_2dvar['wt_s'][i]) for i in range(nt)]
   d2a_int = [np.interp(zzw,NCARLES_2dvar['zw_zi'][i],(NCARLES_2dvar['wq_r'][i]+NCARLES_2dvar['wq_s'][i])*facq) for i in range(nt)]
   d2b_int = [np.interp(zzw,NCARLES_2dvar['zw_zi'][i],(NCARLES_2dvar['wq_s'][i])*facq) for i in range(nt)]

d1a_ncar = rollavg_pandas(d1a_int, num)  # centered time average
d1b_ncar = rollavg_pandas(d1b_int, num)
d2a_ncar = rollavg_pandas(d2a_int, num) 
d2b_ncar = rollavg_pandas(d2b_int, num)

d1a.append((d1a_ncar[NCARLES_time_ind], zzw, color_ncar,'NCAR-LES'))  # add data to list
d1b.append((d1b_ncar[NCARLES_time_ind], zzw, color_ncar))
d2a.append((d2a_ncar[NCARLES_time_ind], zzw, color_ncar,'NCAR-LES'))
d2b.append((d2b_ncar[NCARLES_time_ind], zzw, color_ncar))

# --- WRF-LES 

color_wrf = 'blue'

facq = 1000. # convert from kg/kg to g/kg
facz = 1.e-3 # convert to [km]

if (z_grid == 0) or (z_grid == 1):
    izs = 1
    if z_grid == 0:
        zzw = WRFLES_zw[izs:] * facz
    elif z_grid == 1:
        zzw = WRFLES_2dvar['zw_zi'][WRFLES_time_ind]
    d1a_int = WRFLES_2dvar['wt_r'][:,izs:] + WRFLES_2dvar['wt_s'][:,izs:]
    d1b_int = WRFLES_2dvar['wt_s'][:,izs:]
    d2a_int = WRFLES_2dvar['wq_r'][:,izs:] + WRFLES_2dvar['wq_s'][:,izs:]
    d2b_int = WRFLES_2dvar['wq_s'][:,izs:]
else:
   zzw = zwi
   nt,nk = np.shape(WRFLES_2dvar['zw_zi'])
   d1a_int = [np.interp(zzw,WRFLES_2dvar['zw_zi'][i], \
                 WRFLES_2dvar['wt_r'][i]+WRFLES_2dvar['wt_s'][i])  \
                 for i in range(nt)]                                    
   d1b_int = [np.interp(zzw,WRFLES_2dvar['zw_zi'][i],WRFLES_2dvar['wt_s'][i]) for i in range(nt)]
   d2a_int = [np.interp(zzw,WRFLES_2dvar['zw_zi'][i], \
                 (WRFLES_2dvar['wq_r'][i]+WRFLES_2dvar['wq_s'][i]))  \
                 for i in range(nt)]                                    
   d2b_int = [np.interp(zzw,WRFLES_2dvar['zw_zi'][i],WRFLES_2dvar['wq_s'][i]) for i in range(nt)]

d1a_wrf = rollavg_pandas(d1a_int, num)  # centered time average
d1b_wrf = rollavg_pandas(d1b_int, num)
d2a_wrf = rollavg_pandas(d2a_int, num)
d2b_wrf = rollavg_pandas(d2b_int, num)

d1a.append((d1a_wrf[WRFLES_time_ind], zzw, color_wrf,'WRF'))  # add data to list
d1b.append((d1b_wrf[WRFLES_time_ind], zzw, color_wrf))
d2a.append((d2a_wrf[WRFLES_time_ind]*facq, zzw, color_wrf,'WRF'))
d2b.append((d2b_wrf[WRFLES_time_ind]*facq, zzw, color_wrf))

# ---- configure the C130 observations

facz = 1.e-3  # convert [m] -> [km]

d1c.append((c130_wt, c130_alt*facz, c130_wt_std, 'C-130'))
d2c.append((c130_wq, c130_alt*facz, c130_wq_std, 'C-130'))

# ---- configure the tower observations

facz = 1.e-3  # convert [m] -> [km]

d1t.append((tower_wt, tower_alt*facz, tower_wt_std, 'Tower'))
d2t.append((tower_wq, tower_alt*facz, tower_wq_std, 'Tower'))

# ---- configure desired ticks/titles

# first declare some variables

xmin = np.empty(2, dtype=object)
xmax = np.empty(2, dtype=object)
xfrq_major = np.empty(2, dtype=object)
xfrq_minor = np.empty(2, dtype=object)
x_title = np.empty(2, dtype=object)

ymin = np.empty(2, dtype=object)
ymax = np.empty(2, dtype=object)
yfrq_major = np.empty(2, dtype=object)
yfrq_minor = np.empty(2, dtype=object)
y_title = np.empty(2, dtype=object)

# ---- setup axis ticks and titles

# fig 0
xmin[0] = -0.06
xmax[0] =  0.17
xfrq_major[0] = 0.05
xfrq_minor[0] = 5
x_title[0] = r"$\overline{w'\theta'}$~~\Large{[m K s$^{-1}$]}"

if z_grid == 0:
    y_title[0] = r'$z$~~\Large{[km]}'
else:
    y_title[0] = r'$z / z_i$'

# fig 1
xmin[1] = -0.02
xmax[1] = 0.25
xfrq_major[1] = 0.05
xfrq_minor[1] = 5

x_title[1] = r"$\overline{w'q'}$~~\Large{[m s$^{-1}$\,g kg$^{-1}$]}"
y_title[1] = y_title[0]

# ---- y-axis ticks for all figures

if z_grid == 0:
    ymin = 0.
    ymax = 1.8
    yfrq_major = 1.0
    yfrq_minor = 5
else:
    ymin = 0.
    ymax = 1.4
    yfrq_major = 0.2
    yfrq_minor = 4

# ---- collect those settings for more general use

ticks_titles = {'xmin': xmin, 'xmax': xmax, 'xfrq_major': xfrq_major, 'xfrq_minor': xfrq_minor, 'x_title': x_title,
                'ymin': ymin, 'ymax': ymax, 'yfrq_major': yfrq_major, 'yfrq_minor': yfrq_minor, 'y_title': y_title}

# ---- build plot

ax = plot_profile_2var_1x2(d1a, d1b, d1c, d1t,  # data for plot 0
                           d2a, d2b, d2c, d2t,  # data for plot 1
                           ticks_titles)               # ticks and titles for both

# ---- add plot modifications specific for the current variables

ax[0].axvline(x=0.0, color='black', linewidth=0.3)
ax[1].axvline(x=0.0, color='black', linewidth=0.3)
ax[1].text(0.95, 0.95, '{time:0>4.0f} LT'.format(time=time2plot*100),
      transform=ax[1].transAxes,
      horizontalalignment='right',
      verticalalignment='top',
      fontsize='x-small', color='black')

plt.savefig("../plots/pdf/met_scl_flux_profiles.pdf")
plt.savefig("../plots/png/met_scl_flux_profiles.png", dpi=2048, bbox_inches='tight')
