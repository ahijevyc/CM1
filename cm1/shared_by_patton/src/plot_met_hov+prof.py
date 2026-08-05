#!/usr/bin/env python3

exec(open('import_packages.py').read())
exec(open('definitions.py').read())
exec(open('read_les_ncar.py').read())
exec(open('read_les_wrf.py').read())
exec(open('read_les_mpas.py').read())
exec(open('read_les_fe.py').read())
exec(open('read_les_cm1.py').read())
exec(open('read_les_dales.py').read())
exec(open('read_les_microhh.py').read())
exec(open('read_obs_lidar.py').read())
exec(open('read_obs_C130_met.py').read())
exec(open('read_scm_wrf.py').read())
exec(open('read_scm_scam.py').read())
exec(open('read_scm_somcrus.py').read())
exec(open('read_scm_cm1.py').read())

def plot_profile_2var_1x3 (da,db,do,config):

    # ---- function to plot three sets of vertical profiles of two variables each 
    #      (e.g. tot + sgs) laid out in a 1row x 3column three-panel arrangement 
    #
    #   NOTE: in order to enable modification to the figure following a call to this
    #         routine, the routine does not show or close the plot, or export a file.

    for i in range(len(time2plot)):
        axp[i].tick_params(axis='both', which='both', direction='out', labelsize='large', pad=3)
        axp[i].tick_params(axis='both', which='major', length=5.5, width=1)
        axp[i].tick_params(axis='both', which='minor', length=3., width=0.7)
        axp[i].tick_params(axis='x', which='both', top='True')
        axp[i].tick_params(axis='y', which='both', right='True')

    marker_style = dict(color='black', linestyle='-', marker='o',
                    markersize=3, linewidth=0.5)

    # --- add zero-lines to each plot (doing this first so 
    #     that this line ends up behind all the other lines)

    for it in range(len(time2plot)):
        if (var != 'q'): axp[it].axvline(x=0.0, color='black', linewidth=0.3)

    # --- add lines to each plot

    if (SCM == 'True'):
        for i in range(len(db)):
            n = db[i]
            axp[n[0]].fill_betweenx(y=n[2], x1=n[3], x2=n[4], facecolor=(0,0,0,.1), edgecolor=(0,0,0,.5), label=n[6] )
            lp1 = axp[n[0]].plot(n[1], n[2], color=n[5], linestyle='solid', linewidth=1.5)
            lp2 = axp[n[0]].fill(np.NaN, np.NaN, facecolor=(0.9,0.9,0.9), edgecolor="None")
            lp3 = axp[n[0]].fill(np.NaN, np.NaN, facecolor="None", edgecolor=(0.5,0.5,0.5),linewidth=1.5)
    else:
        for n in db:
            axp[n[0]].plot(n[1], n[2], color=n[3], linestyle='dashed',linewidth=1.5)         # ---- SFS quantities

    for n in da:
        axp[n[0]].plot(n[1], n[2], color=n[3], linestyle=n[5],linewidth=2,label=n[4]) # ---- resolved quantities

    for n in do:
        obs = axp[n[0]].plot(n[1], n[2], fillstyle='none', label=n[3], **marker_style)         # ---- observations

    # ---- set y-axis title

    axp[0].set_ylabel(config['y_title'][0], fontsize='x-large', labelpad=7)
    axp[-1].set_ylabel(config['y_title'][-1], fontsize='x-large', labelpad=7)

    # ---- x-ticks

    for i in range(len(time2plot)):
        axp[i].set_xlim([config['xmin'][i], config['xmax'][i]])
        axp[i].xaxis.set_major_locator(ticker.MultipleLocator(config['xfrq_major'][i]))
        axp[i].xaxis.set_minor_locator(ticker.MultipleLocator(config['xfrq_major'][i]/config['xfrq_minor'][i]))

    # ---- y-axis

    if ((figs == 'profiles_surface') and (var == 'u')) or \
       ((figs == 'profiles_surface') and (var == 'v')) or \
       ((figs == 'profiles_surface') and (var == 't')) or \
       ((figs == 'profiles_surface') and (var == 'q')):
        for i in range(len(time2plot)):
            axp[i].set_yscale('log')
            axp[i].set_ylim([config['ymin'][i], config['ymax'][i]])
            axp[i].yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
            axp[i].yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    else:
        for i in range(len(time2plot)):
            axp[i].set_ylim([config['ymin'][i], config['ymax'][i]])
            axp[i].yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major'][i]))
            axp[i].yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major'][i]/config['yfrq_minor'][i]))


    # ---- y-axis ticks for figures in right-hand column
  
    for i in range(1,len(time2plot)-1):
        axp[i].yaxis.set_ticklabels([])
        axp[i].yaxis.set_ticks_position('both')

    axp[-1].yaxis.set_label_position("right")
    axp[-1].yaxis.tick_right()
    axp[-1].yaxis.set_ticks_position('both')

    # ---- set default legend position

    if (figs == 'combined'):
        lgnd_box_x = 1.37
        lgnd_box_y = 1.16
    elif (figs == 'profiles') or (figs == 'profiles_surface'):
        lgnd_box_x = 1.32
        lgnd_box_y = 1.08

    # ---- now modify that position if needed

    if (figs == 'profiles') or (figs == 'combined'):
        if (var == 'u'):
            lgnd_box_x = 0.0
            lgnd_box_y = 1.0
            lfig = 0
            lloc = 'upper left'
        elif (var == 't'):
            lgnd_box_x = 0.00
            lgnd_box_y = 1.09
            lfig = 0
            lloc = 'upper left'
        elif ((var == 'q')):
            lgnd_box_x = 1.13
            lgnd_box_y = 1.09
            lfig = 0
            lloc = 'upper right'
        elif ((var == 'v') or (var == 'tt') or (var == 'qq') or (var == 'tke')):
            lgnd_box_x = 1.0
            lgnd_box_y = 1.0
            lfig = 0
            lloc = 'upper right'
        elif ((var == 'uu') or (var == 'vv') or (var == 'ww')):
            lgnd_box_x = 1.0
            lgnd_box_y = 0.9
            lfig = 0
            lloc = 'upper right'
        elif ((var == 'wt')):
            if (SCM == 'True'):
                lgnd_box_x = 1.0
                lgnd_box_y = 0.9
                lfig = 0
                lloc = 'upper right'
            else:
                lgnd_box_x = -0.7
                lgnd_box_y =  0.9
                lfig = 1
                lloc = 'upper left'
        elif ((var == 'wq')):
            if (SCM == 'True'):
                lgnd_box_x = 1.1
                lgnd_box_y = 0.9
                lfig = 0
                lloc = 'upper right'
            else:
                lgnd_box_x = -0.8
                lgnd_box_y =  0.9
                lfig = 1
                lloc = 'upper left'
        elif ((var == 'uw') or (var == 'vw')):
            lgnd_box_x = 0.0
            lgnd_box_y = 0.9
            lfig = 0
            lloc = 'upper left'
    elif (figs == 'profiles_surface') and ((var == 't') or (var == 'uu') or (var == 'vv') or (var == 'ww')):
            lgnd_box_x = -0.7
            lgnd_box_y = 1.08
            lfig = 1
            lloc = 'upper left'
    elif (figs == 'profiles_surface') and ((var == 'wt')):
            lgnd_box_x = -0.20
            lgnd_box_y = 1.09
            lfig = 1
            lloc = 'upper left'
    elif (figs == 'profiles_surface') and ((var == 'wq')):
            lgnd_box_x = -0.13
            lgnd_box_y =  1.09
            lfig = 1
            lloc = 'upper left'
    else:
        lfig = -1
        lloc = 'upper right'

    # ---- treat SCM plots special

    if (SCM == 'True'):

        # ---- place LES-AVG at front of list, modify handle

        handles, labels = axp[lfig].get_legend_handles_labels()
        llabel = labels[-1]                        # grab last label in the list
        handles = handles[:-1]                     # eliminate last entry from the handles list
        labels = labels[:-1]                       # eliminate last entry from the labels  list
        handles.insert(0,(lp2[0],lp1[0],lp3[0]))   # insert new handle at the front of the list
        labels.insert(0,llabel)                    # insert new label  at the front of the list
        if (len(do) != 0):                         # if obs are included, append them at the back of the list,
            handles.append(obs)                    #    this step is required because the panel containing
            labels.append(clabel)                  #    the obs is not always the panel with the legend

        axp[lfig].legend(handles,labels,
               fontsize='small', frameon='True', borderpad=0.5,
               bbox_to_anchor=(lgnd_box_x, lgnd_box_y), loc=lloc, framealpha=1.0,
               borderaxespad=0.7, handlelength=2.8, handletextpad=0.6,
               labelspacing=0.3, edgecolor='dimgray')

    else:

        # ---- grab the legend handles and labels lists,
        #      if obs are included, append them at the back of the list
        #      this step is required because the obs are not always
        #      exported to the panel containing the legend

        handles, labels = axp[lfig].get_legend_handles_labels()
        if (len(do) != 0):
            handles.append(obs)
            labels.append(clabel)

        axp[lfig].legend(handles,labels,
                   loc=lloc,fontsize='small', frameon='True', borderpad=0.5,
                   bbox_to_anchor=(lgnd_box_x, lgnd_box_y), framealpha=1.0,
                   borderaxespad=0.7, handlelength=2.8, handletextpad=0.6,
                   labelspacing=0.3, edgecolor='dimgray')

    # ---- lay a few items over top

    if (figs == 'combined'):
        var_label_x = 0.5
        var_label_y = 0.03
    elif (figs == 'profiles') or (figs == 'profiles_surface'):
        var_label_x = 0.5
        var_label_y = 0.06

    if (var == 'u') or (var == 'v') or (var == 'q'):
        time_label_x = 0.04
        time_label_y = 0.1
    elif (var == 't') or (var == 'tt') or (var == 'qq'):
        time_label_x = 0.66
        time_label_y = 0.1
    elif (var == 'tke'):
        time_label_x = 0.08
        time_label_y = 0.1
    elif (var == 'uu') or (var == 'vv') or (var == 'ww') or (var == 'wt') or (var == 'wq'):
        time_label_x = 0.66
        time_label_y = 0.95
    else:
        time_label_x = 0.06
        time_label_y = 0.95

    # ---- should redo these text overlays using 'annotate' like below

    for it in range(len(time2plot)):
        axp[it].text(time_label_x, time_label_y, 
                     '{time:0>4.0f} LT'.format(time=time2plot[it]*100),
                     transform=axp[it].transAxes,
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize='medium', color='black')

    fig.text(var_label_x, var_label_y, var_label, 
             horizontalalignment='center',
             verticalalignment='center',
             fontsize='x-large', color='black')

    return axp

def plot_contour_1var_Nx1 (dc,config):

    # ---- function to produce a Nx1 set of contour plots
    #
    #   NOTE: in order to be able to modify the figure following a call to this routine,
    #         the routine does not open, show, or close the plot, or export a file.

    for i in range(len(dc)):
        n = dc[i]
        CS1 = axc[i].contour (n[0], n[1], n[2], levels=config['levels'], colors='black', linewidths=1)
        CS2 = axc[i].contourf(n[0], n[1], n[2], config['levels'], cmap='coolwarm')

        axc[i].plot(n[0], n[4], color='black', linestyle='dashdot', linewidth=2.5, zorder=3);

        if i == 0:
            cax = fig.add_axes([0.32,0.95,0.6,.02])
            cbar = fig.colorbar(CS2, ax=axc[i], pad=0.02, ticks=CS1.levels[::1], orientation="horizontal", shrink=0.5, cax=cax)
            cbar.add_lines(CS1)
            axc[i].text(-0.38, 0.40, var_label,
                        transform=cax.transAxes,
                        horizontalalignment='left',
                        verticalalignment='center',
                        fontsize='x-large', color='black')

        axc[i].annotate(n[3], xy=(0,1), xycoords='axes fraction',
              xytext=(17,-17), textcoords='offset points', 
              fontsize='large', color='black', ha='left', va='top',
              bbox=dict(facecolor='white', edgecolor='dimgray', boxstyle='round',mutation_scale=2))


    # ---- set axis titles

    axc[-1].set_xlabel(config['x_title'], fontsize='x-large', labelpad=5)

    for i in range(len(dc)):
        axc[i].set_ylabel(config['y_title'], fontsize='x-large', labelpad=7)

    # ---- set ticks

    for i in range(len(dc)):
        axc[i].tick_params(axis='both', which='both', direction='out', labelsize='large', pad=3)
        axc[i].tick_params(axis='both', which='major', length=5.5, width=1)
        axc[i].tick_params(axis='both', which='minor', length=3., width=0.7)
        axc[i].tick_params(axis='x', which='both', top='True')
        axc[i].tick_params(axis='y', which='both', right='True')

    for i in range(len(dc)):

        # ---- x-ticks
        axc[i].set_xlim([config['xmin'], config['xmax']])
        axc[i].xaxis.set_major_locator(ticker.MultipleLocator(config['xfrq_major']))
        axc[i].xaxis.set_minor_locator(ticker.MultipleLocator(config['xfrq_major']/config['xfrq_minor']))

        # ---- y-axis ticks

        axc[i].set_ylim([config['ymin'], config['ymax']])
        axc[i].yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major']))
        axc[i].yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major']/config['yfrq_minor']))

        # ---- y-axis ticks for figures in right-hand column

        axc[i].yaxis.set_ticks_position('both')

    # ---- x-axis ticks for figures with shared axes

    for i in range(len(dc)-1):
        axc[i].xaxis.set_ticklabels([])
        axc[i].xaxis.set_ticks_position('both')

    # ---- add title to right-hand y-axis 

    for i in range(len(dc)):
        axc2 = axc[i].twinx()
        axc2.tick_params(axis='y', which='both', direction='out', labelsize='large', pad=3, right='True')
        axc2.tick_params(axis='y', which='major', length=5.5, width=1)
        axc2.tick_params(axis='y', which='minor', length=3., width=0.7)
        axc2.set_ylabel(config['y_title'], fontsize='x-large', labelpad=7)
        axc2.set_ylim([config['ymin'], config['ymax']])
        axc2.yaxis.set_major_locator(ticker.MultipleLocator(config['yfrq_major']))
        axc2.yaxis.set_minor_locator(ticker.MultipleLocator(config['yfrq_major']/config['yfrq_minor']))

    return axc

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

#print(plt.rcParams.keys())

# ----- select the output style

single_file = 0    # =0, individual files; =1, export all figs to single file
output_file_type = 0    # =0, PDF; =1, PNG (only works with: single_file=0)

# ----- are we working on SCM data?  or LES data?

SCM = 'False'
#SCM = 'True'

# ---- specify the datasets and variables to be included

if (SCM is 'False'):
#   data2plot = [ 'CM1', 'FE', 'MPAS', 'NCAR', 'WRF', 'OBS' ]
    data2plot = [ 'CM1', 'DALES', 'FE', 'MICROHH', 'MPAS', 'NCAR', 'WRF' ]
    vars2plot = [ 'u','v', 't', 'q', 'uu', 'vv', 'ww', 'tke', 'tt', 'qq', 'uw', 'vw', 'wt', 'wq' ]
elif (SCM is 'True'):
    data2plot = [ 'CM1', 'DALES', 'FE', 'MPAS', 'NCAR', 'WRF', 'YSUh', 'MYNNh', 'SCAM',    # not including FE currently because nz = 186
                 'CM1_CLUBB', 'CM1_MYJ']                                          # removed CM1-MYNN* per George's request
    vars2plot = [ 'u', 't', 'q', 'uu', 'vv', 'ww', 'tke', 'uw', 'tt', 'qq', 'wt', 'wq' ]


# ----- select the output style

#figs2plot = [ 'profiles', 'contours', 'combined']
figs2plot = [ 'profiles' , 'profiles_surface' ]
#figs2plot = [ 'profiles' ]
#figs2plot = [ 'profiles', 'profiles_surface' ]
#figs2plot = [ 'contours' ]
#figs2plot = [ 'profiles', 'contours', 'combined', 'profiles_surface' ]
#figs2plot = [ 'combined' ]
#figs2plot = [ 'profiles_surface' ]

# ----- select the times to plot

time2plot = [ 10., 12., 14., 16.]
#time2plot = [ 8.3, 12., 14., 16.]

# --- specify averaging duration (in 5-min chunks, i.e. 12 = 60 min avg)

num = 12  # number of data points in rolling average centered at time
#num = 6  # number of data points in rolling average centered at time

# --- set vertical grid, build z/zi grid into which data can be interpolated

z_grid = 0   # =0 -> km 
             # =1 -> z/zi
             # =2 -> data interpolated in to z/zi grid

nt,nk = np.shape(NCARLES_2dvar['zu_zi'])
zwi = np.empty([nk], dtype=object)

ztop = 1500.
zl = 3000.
zwi = np.linspace(0,zl,nk) / ztop

# --- build time variables

WRFLES_time_ind = [None] * len(time2plot)
WRFSCM_time_ind = [None] * len(time2plot)
NCARLES_time_ind = [None] * len(time2plot)
FE_time_ind = [None] * len(time2plot)
CM1_time_ind = [None] * len(time2plot)
CM1SCM_time_ind = [None] * len(time2plot)
MPAS_time_ind = [None] * len(time2plot)
DALES_time_ind = [None] * len(time2plot)
MICROHH_time_ind = [None] * len(time2plot)
SCAM_time_ind = [None] * len(time2plot)
SOMCRUS_time_ind = [None] * len(time2plot)
LIDAR_time_ind = [None] * len(time2plot)

for it in range(len(time2plot)):
    WRFLES_time_ind[it] = np.argmin(np.abs(WRFLES_time_hr - time2plot[it]))
    WRFSCM_time_ind[it] = np.argmin(np.abs(WRFSCM_Hr_frac_ysu_hires - time2plot[it]))
    NCARLES_time_ind[it] = np.argmin(np.abs(NCARLES_time_hr - time2plot[it]))
    FE_time_ind[it] = np.argmin(np.abs(FE['time'] - time2plot[it]))
    CM1_time_ind[it] = np.argmin(np.abs(CM1_time_hr - time2plot[it]))
    CM1SCM_time_ind[it] = np.argmin(np.abs(CM1_CLUBB_time_hr - time2plot[it]))
    MPAS_time_ind[it] = np.argmin(np.abs(MPAS_time_hr - time2plot[it]))
    DALES_time_ind[it] = np.argmin(np.abs(DALES_time_hr - time2plot[it]))
    MICROHH_time_ind[it] = np.argmin(np.abs(MICROHH_time_hr - time2plot[it]))
    SCAM_time_ind[it] = np.argmin(np.abs(SCAM_time_hr - time2plot[it]))
    SOMCRUS_time_ind[it] = np.argmin(np.abs(SOMCRUS_time_hr - time2plot[it]))
    LIDAR_time_ind[it] = np.argmin(np.abs(LIDAR_time_hr - time2plot[it]))
    print(NCARLES_time_ind[it],SOMCRUS_time_ind[it])

#print('FE_time_ind = ',FE_time_ind)
#print('NCARLES_time_ind = ',NCARLES_time_ind)

# ---- set output file names for 'single collective file' to according to the above configuration

if (single_file == 1):
    if (SCM is 'True'):
        pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_hov+prof.scm.all.pdf")
    elif (SCM is 'False'):
        if ('OBS' in data2plot):
            pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_hov+prof+obs.all.pdf")
        else:
            pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_hov+prof.all.pdf")

# ---- loop over plot type

for figs in figs2plot:

    print(' working on: ',figs)

    for var in vars2plot:                      # loop over variable to plot

        print('     var: ',var)

        da = []
        db = []
        do = []
        dc = []
        dl = []

        for id in range(len(data2plot)):       # loop over data types, i.e. LES, SCM, OBS

            zzw   = 'None'
            var_z = 'None'

            if data2plot[id] == 'FE':                              # ---- FastEddy

                clabel = 'FastEddy'
                color = 'mediumseagreen'
                linestyle = 'solid'
    
                if var == 'u':
                    var_t = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'v':
                    var_t = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 't':
                    var_t = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'q':
                    var_t = 'qv'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'p':
                    continue
                    var_t = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e2
                elif var == 'uu':
                    var_t = 'uu_t'
                    var_s = 'uu_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'vv':
                    var_t = 'vv_t'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'ww':
                    var_t = 'ww_t'
                    var_s = 'ww_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'tke':
                    var_t = 'tke_t'
                    var_s = 'tke'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'tt':
                    var_t = 'tth'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'qq':
                    var_t = 'qqv'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'uw':
                    var_t = 'uw_t'
                    var_s = 'tau31'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'vw':
                    var_t = 'vw_t'
                    var_s = 'tau32'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wt':
                    var_t = 'wth_t'
                    var_s = 'wth_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wq':
                    var_t = 'wqv_t'
                    var_s = 'wqv_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.

                facz = 1.e-3 # convert to [km]

                if z_grid == 0 or z_grid ==1:
                    zzw = FE[var_z][FE_time_ind[0]] * facz
                    da_int = FE[var_t]
                    if var_s in FE:
                        db_int = FE[var_s]
                else:
                    nt,nk = np.shape(FE[var_z])        # FE only used 186 vertical levels.
                    zl = 2790.
                    zzw = np.linspace(0,zl,nk) / ztop
                    da_int = [np.interp(zzw,FE['z_zi'][i],FE[var_t][i]) for i in range(nt)]
                    if var_s in FE:
                        db_int = [np.interp(zzw,FE['z_zi'][i],FE[var_s][i]) for i in range(nt)]

#               num_fe = num
                num_fe = np.int(num / 2)  # FE only provided data every ten min
                da_fe = rollavg_pandas(da_int, num_fe)  # centered time average
                if var_s in FE:
                    db_fe = rollavg_pandas(db_int, num_fe)

                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_fe[FE_time_ind[i]], zzw, color, clabel, linestyle))   # add data to list
                        if var_s in FE:
                            db.append((i, fac*db_fe[FE_time_ind[i]], zzw, color))
                else:
                    if (var != 'tt') and (var != 'qq') and \
                       (var != 'uw') and (var != 'wt') and (var != 'wq'):          # skipping FE flux and scalar variance data for LES-AVG
                        for i in range(len(time2plot)):
                            dz_fe = NCARLES.variables[var_z][0,:] * facz           # because FE data on a non-standard grid
                            dl_fe = np.interp(dz_fe, zzw, da_fe[FE_time_ind[i]])   #    interpolate FE data to NCAR-LES grid
                            dl.append((fac*dl_fe, dz_fe))                          #    when calculating LES-AVG

                if (SCM == 'False'):
                    dc.append((FE['time'], zzw, fac*da_fe.transpose(), clabel, FE['pblhth']*facz)) 

            elif data2plot[id] == 'WRF':

                clabel = 'WRF'
                color = 'blue'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'p'):
                    var_r = 'pressure'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e2
                elif (var == 'uu'):
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'ww'):
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_r'
                    var_s = 'tke_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'tt'):
                    var_r = 'tt_r'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'qq'):
                    var_r = 'qq_r'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFLES_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e6
                elif (var == 'uw'):
                    continue
                    var_r = 'uw_r'
                    var_s = 'uw_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    continue
                    var_r = 'vw_r'
                    var_s = 'vw_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wt'):
                    var_r = 'wt_r'
                    var_s = 'wt_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wq'):
                    var_r = 'wq_r'
                    var_s = 'wq_s'
                    if (z_grid == 0):
                        var_z = WRFLES_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.e3
            
                facz = 1.e-3 # convert to [km]

                if (z_grid == 0) or (z_grid == 1):
                    if (var == 'ww') or (var == 'tke') or (var == 'uw') or (var == 'vw') or (var == 'wt') or (var == 'wq'):
                        iz = 1
                    else:
                        iz = 0
                    if (var == 'wt') or (var == 'wq'):
                        iv = 1
                    else:
                        iv = 0
                    if (z_grid == 0):
                        zzw = var_z[iz:] * facz
                    elif (z_grid == 1):
                        zzw = WRFLES_2dvar[var_z][WRFLES_time_ind]
                    if var_s in WRFLES_2dvar:
                        da_int = WRFLES_2dvar[var_r][:,iv:] + WRFLES_2dvar[var_s][:,iv:]
                        db_int = WRFLES_2dvar[var_s][:,iv:]
                    else:
                        da_int = WRFLES_2dvar[var_r][:,iz:]
                else:
                    zzw = zwi
                    nt,nk = np.shape(WRFLES_2dvar[var_z])
                    if var_s in WRFLES_2dvar:
                        da_int = [np.interp(zzw,WRFLES_2dvar[var_z][i], WRFLES_2dvar[var_r][i]+WRFLES_2dvar[var_s][i]) for i in range(nt)]                                    
                        db_int = [np.interp(zzw,WRFLES_2dvar[var_z][i],WRFLES_2dvar[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,WRFLES_2dvar[var_z][i], WRFLES_2dvar[var_r][i]) for i in range(nt)]                                    
            
                da_wrf = rollavg_pandas(da_int, num)  # centered time average
                if var_s in WRFLES_2dvar:
                    db_wrf = rollavg_pandas(db_int, num)
    
                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_wrf[WRFLES_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in WRFLES_2dvar:
                            db.append((i, fac*db_wrf[WRFLES_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_wrf[WRFLES_time_ind[i]], zzw))
    
                if (SCM == 'False'):
                    dc.append((WRFLES_time_hr, zzw, fac*da_wrf.transpose(), clabel, WRFLES_PBLH*facz)) 
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_wrf[WRFLES_time_ind[i]], zzw))

            elif data2plot[id] == 'MPAS':

                clabel = 'MPAS'
                color = 'gray'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'p'):
                    var_r = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e2
                elif (var == 'uu'):
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'ww'):
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_r'
                    var_s = 'tke_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'tt'):
                    var_r = 'tt_r'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'qq'):
                    var_r = 'qq_r'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MPAS_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'uw'):
                    var_r = 'uw_r'
                    var_s = 'uw_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    var_r = 'vw_r'
                    var_s = 'vw_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wt'):
                    var_r = 'wt_r'
                    var_s = 'wt_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wq'):
                    var_r = 'wq_r'
                    var_s = 'wq_s'
                    if (z_grid == 0):
                        var_z = MPAS_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
            
                facz = 1.e-3 # convert to [km]

                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = var_z[:] * facz
                    elif (z_grid == 1):
                        zzw = MPAS_2dvar[var_z][MPAS_time_ind]
                    if var_s in MPAS_2dvar:
                        da_int = MPAS_2dvar[var_r][:,:] + MPAS_2dvar[var_s][:,:]
                        db_int = MPAS_2dvar[var_s][:,:]
                    else:
                        da_int = MPAS_2dvar[var_r][:,:]
                else:
                    zzw = zwi
                    nt,nk = np.shape(MPAS_2dvar[var_z])
                    if var_s in MPAS_2dvar:
                        da_int = [np.interp(zzw,MPAS_2dvar[var_z][i],MPAS_2dvar[var_r][i]+MPAS_2dvar[var_s][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,MPAS_2dvar[var_z][i],MPAS_2dvar[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,MPAS_2dvar[var_z][i], MPAS_2dvar[var_r][i]) for i in range(nt)]                                    
            
                da_mpas = rollavg_pandas(da_int, num)  # centered time average
                if var_s in MPAS_2dvar:
                    db_mpas = rollavg_pandas(db_int, num)
    
                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_mpas[MPAS_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in MPAS_2dvar:
                            db.append((i, fac*db_mpas[MPAS_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_mpas[MPAS_time_ind[i]], zzw))
    
                if (SCM == 'False'):
                    dc.append((MPAS_time_hr, zzw, fac*da_mpas.transpose(), clabel, MPAS.variables['zi_t']*facz)) 
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_mpas[MPAS_time_ind[i]], zzw))

            elif data2plot[id] == 'DALES':    # --- DALES

                clabel = 'DALES'
                color = 'crimson'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'p'):
                    var_r = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'uu'):
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'ww'):
                   var_r = 'ww_r'
                   var_s = 'ww_s'
                   if (z_grid == 0):
                       var_z = 'zw'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif (var == 'tke'):
                   var_r = 'tke_r'
                   var_s = 'tke_s'
                   if (z_grid == 0):
                       var_z = 'zw'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif (var == 'tt'):
                   var_r = 'tt_r'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = 'zu'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zu_zi'
                   fac = 1.
                elif (var == 'qq'):
                   var_r = 'qq_r'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = 'zu'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zu_zi'
                   fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'uw_r'
                    var_s = 'uw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    var_r = 'vw_r'
                    var_s = 'vw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wt'):
                    var_r = 'wt_r'
                    var_s = 'wt_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wq'):
                    var_r = 'wq_r'
                    var_s = 'wq_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.e3
                       
                facz = 1.e-3 # convert to [km]
        
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = DALES.variables[var_z][DALES_time_ind[0]] * facz
                    elif (z_grid == 1):
                        zzw = DALES_2dvar[var_z][DALES_time_ind[0]]
                    if var_s in DALES_2dvar:
                        da_int = DALES_2dvar[var_r] + DALES_2dvar[var_s]
                        db_int = DALES_2dvar[var_s]
                    else:
                        da_int = DALES_2dvar[var_r]
                else:
                    zzw = zwi
                    nt,nk = np.shape(DALES_2dvar[var_z])
                    if var_s in DALES_2dvar:
                        da_int = [np.interp(zzw,DALES_2dvar[var_z][i],DALES_2dvar[var_r][i]+DALES_2dvar[var_s][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,DALES_2dvar[var_z][i],DALES_2dvar[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,DALES_2dvar[var_z][i],DALES_2dvar[var_r][i]) for i in range(nt)]

                da_dales = rollavg_pandas(da_int, num)  # centered time average
                if var_s in DALES_2dvar:
                    db_dales = rollavg_pandas(db_int, num)
        
                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_dales[DALES_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in DALES_2dvar:
                            db.append((i, fac*db_dales[DALES_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_dales[DALES_time_ind[i]], zzw))
        
                if (SCM == 'False'):
                    dc.append((DALES_time_hr, zzw, fac*da_dales.transpose(), clabel, DALES_PBLH*facz))

            elif data2plot[id] == 'MICROHH':    # --- MICROHH

                clabel = 'MicroHH'
                color = 'cyan'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'thl'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'qt'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'p'):
                    var_r = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'uu'):
                    var_r = 'u_2'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'v_2'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = MICROHH_zu
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'ww'):
                   var_r = 'w_2'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = MICROHH_zw
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif (var == 'tke'):
                   var_r = 'tke'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = MICROHH_zu
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif (var == 'tt'):
                   var_r = 'thl_2'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = MICROHH_zu
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif (var == 'qq'):
                   var_r = 'qt_2'
                   var_s = 'None'
                   if (z_grid == 0):
                       var_z = MICROHH_zu
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zu_zi'
                   fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'u_w'
                    var_s = 'u_diff'
                    if (z_grid == 0):
                        var_z = MICROHH_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    var_r = 'v_w'
                    var_s = 'v_diff'
                    if (z_grid == 0):
                        var_z = MICROHH_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wt'):
                    var_r = 'thl_w'
                    var_s = 'thl_diff'
                    if (z_grid == 0):
                        var_z = MICROHH_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'wq'):
                    var_r = 'qt_w'
                    var_s = 'qt_diff'
                    if (z_grid == 0):
                        var_z = MICROHH_zw
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.e3
                       
                facz = 1.e-3 # convert to [km]
        
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                       zzw = var_z[:] * facz
                    elif (z_grid == 1):
                        zzw = MICROHH_2dvar[var_z]
                    if var_s in MICROHH_2dvar:
                        da_int = MICROHH_2dvar[var_r] + MICROHH_2dvar[var_s]
                        db_int = MICROHH_2dvar[var_s]
                    else:
                        da_int = MICROHH_2dvar[var_r]
                else:
                    zzw = zwi
                    nt,nk = np.shape(MICROHH_2dvar[var_z])
                    if var_s in MICROHH_2dvar:
                        da_int = [np.interp(zzw,MICROHH_2dvar[var_z],MICROHH_2dvar[var_r][i]+MICROHH_2dvar[var_s][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,MICROHH_2dvar[var_z],MICROHH_2dvar[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,MICROHH_2dvar[var_z],MICROHH_2dvar[var_r][i]) for i in range(nt)]

                da_microhh = rollavg_pandas(da_int, num)  # centered time average
                if var_s in MICROHH_2dvar:
                    db_microhh = rollavg_pandas(db_int, num)

                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_microhh[MICROHH_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in MICROHH_2dvar:
                            db.append((i, fac*db_microhh[MICROHH_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_microhh[MICROHH_time_ind[i]], zzw))
        
                if (SCM == 'False'):
                    dc.append((MICROHH_time_hr, zzw, fac*da_microhh.transpose(), clabel, MICROHH_PBLH*facz))

            elif data2plot[id] == 'CM1':    # --- CM1
    
                clabel = 'CM1'
                color = 'magenta'
                linestyle = 'solid'
    
                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'p'):
                    var_r = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'uu':
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'ww':
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'tke'):
                   var_r = 'tke_r'
                   var_s = 'tke_s'
                   if (z_grid == 0):
                       var_z = 'zw'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif var == 'tt':
                    var_r = 'tt_r'
                    var_s = 'None'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'qq':
                    var_r = 'qq_r'
                    var_s = 'None'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'uw_r'
                    var_s = 'uw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    var_r = 'vw_r'
                    var_s = 'vw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_r'
                    var_s = 'wt_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_r'
                    var_s = 'wq_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.e3
    
                facz = 1.e-3 # convert to [km]
    
                if z_grid == 0 or z_grid ==1:
                    if z_grid == 0:
                        zzw = CM1.variables[var_z][CM1_time_ind[0]] * facz
                    elif z_grid == 1:
                        zzw = CM1_2dvar[var_z][CM1_time_ind[0]]
                    if var_s in CM1_2dvar:
                        da_int = CM1_2dvar[var_r] + CM1_2dvar[var_s]
                        db_int = CM1_2dvar[var_s]
                    else:
                        da_int = CM1_2dvar[var_r]
                else:
                    zzw = zwi
                    nt,nk = np.shape(CM1_2dvar[var_z])
                    da_int = [np.interp(zzw,CM1_2dvar[var_z][i],CM1_2dvar[var_r][i]+CM1_2dvar[var_s][i]) for i in range(nt)]
                    if var_s in CM1_2dvar:
                        db_int = [np.interp(zzw,CM1_2dvar[var_z][i],CM1_2dvar[var_s][i]) for i in range(nt)]
            
                da_cm1 = rollavg_pandas(da_int, num)  # centered time average
                if var_s in CM1_2dvar:
                    db_cm1 = rollavg_pandas(db_int, num)
    
                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_cm1[CM1_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in CM1_2dvar:
                            db.append((i, fac*db_cm1[CM1_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_cm1[CM1_time_ind[i]], zzw))
            
                if (SCM == 'False'):
                    dc.append((CM1_time_hr, zzw, fac*da_cm1.transpose(), clabel, CM1_PBLH*facz))

            elif data2plot[id] == 'NCAR':    # --- NCARLES
    
                clabel = 'NCAR-LES'
                color = 'orange'
                linestyle = 'solid'
    
                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'p'):
                    var_r = 'p'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'uu':
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    if (z_grid == 0):
                        var_z = 'zu'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'ww':
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'tke'):
                   var_r = 'tke_r'
                   var_s = 'tke_s'
                   if (z_grid == 0):
                       var_z = 'zw'
                   elif (z_grid == 1) or (z_grid == 2):
                       var_z = 'zw_zi'
                   fac = 1.
                elif var == 'tt':
                    var_r = 'tt_r'
                    var_s = 'None'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.
                elif var == 'qq':
                    var_r = 'qq_r'
                    var_s = 'None'
                    if z_grid == 0:
                        var_z = 'zu'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zu_zi'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'uw_r'
                    var_s = 'uw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif (var == 'vw'):
                    var_r = 'vw_r'
                    var_s = 'vw_s'
                    if (z_grid == 0):
                        var_z = 'zw'
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_r'
                    var_s = 'wt_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_r'
                    var_s = 'wq_s'
                    if z_grid == 0:
                        var_z = 'zw'
                    elif z_grid == 1 or z_grid == 2:
                        var_z = 'zw_zi'
                    fac = 1.e3
    
                facz = 1.e-3 # convert to [km]
    
                if z_grid == 0 or z_grid ==1:
                    if z_grid == 0:
                        zzw = NCARLES.variables[var_z][NCARLES_time_ind[0]] * facz
                    elif z_grid == 1:
                        zzw = NCARLES_2dvar[var_z][NCARLES_time_ind[0]]
                    if var_s in NCARLES_2dvar:
                        da_int = NCARLES_2dvar[var_r] + NCARLES_2dvar[var_s]
                        db_int = NCARLES_2dvar[var_s]
                    else:
                        da_int = NCARLES_2dvar[var_r]
                else:
                    zzw = zwi
                    nt,nk = np.shape(NCARLES_2dvar[var_z])
                    da_int = [np.interp(zzw,NCARLES_2dvar[var_z][i],NCARLES_2dvar[var_r][i]+NCARLES_2dvar[var_s][i]) for i in range(nt)]
                    if var_s in NCARLES_2dvar:
                        db_int = [np.interp(zzw,NCARLES_2dvar[var_z][i],NCARLES_2dvar[var_s][i]) for i in range(nt)]
            
                da_ncar = rollavg_pandas(da_int, num)  # centered time average
                if var_s in NCARLES_2dvar:
                    db_ncar = rollavg_pandas(db_int, num)
    
                if (SCM == 'False'):
                    for i in range(len(time2plot)):
                        da.append((i, fac*da_ncar[NCARLES_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                        if var_s in NCARLES_2dvar:
                            db.append((i, fac*db_ncar[NCARLES_time_ind[i]], zzw, color))
                else:
                    for i in range(len(time2plot)):
                        dl.append((fac*da_ncar[NCARLES_time_ind[i]], zzw))
            
                if (SCM == 'False'):
                    dc.append((NCARLES_time_hr, zzw, fac*da_ncar.transpose(), clabel, NCARLES_PBLH*facz))

            elif data2plot[id] == 'YSUh':

                clabel = 'WRF-YSU'
                color = 'blue'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'ua'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'QVAPOR'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'uu'):
                    continue
                elif (var == 'vv'):
                    continue
                elif (var == 'ww'):
                    continue
                elif (var == 'tke'):
                    continue
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    continue
                elif (var == 'qq'):
                    continue
                elif (var == 'wt'):
                    continue
                elif (var == 'wq'):
                    continue
            
                facz = 1.e-3 # convert to [km]
            
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = var_z * facz
                    elif (z_grid == 1):
                        zzw = WRFSCM_3dvar_ysu_hires[var_z][WRFSCM_time_ind]
                    if var_s in WRFSCM_3dvar_ysu_hires:
                        da_int = list(WRFSCM_3dvar_ysu_hires[var_r])
                        db_int = list(WRFSCM_3dvar_ysu_hires[var_s])
                    else:
                        da_int = list(WRFSCM_3dvar_ysu_hires[var_r])
                else:
                    zzw = zwi
                    nt,nk = np.shape(WRFSCM_3dvar_ysu_hires[var_z])
                    if var_s in WRFSCM_3dvar_ysu_hires:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_ysu_hires[var_z][i],WRFSCM_3dvar_ysu_hires[var_r][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,WRFSCM_3dvar_ysu_hires[var_z][i],WRFSCM_3dvar_ysu_hires[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_ysu_hires[var_z][i], WRFSCM_3dvar_ysu_hires[var_r][i]) for i in range(nt)]                                    
            
                da_ysu = rollavg_pandas(da_int, num)  # centered time average
                if var_s in WRFSCM_3dvar_ysu_hires:
                    db_ysu = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):
                    da.append((i, fac*da_ysu[WRFSCM_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                    if var_s in WRFSCM_3dvar_ysu_hires:
                        db.append((i, fac*db_ysu[WRFSCM_time_ind[i]], zzw, color))
    
                dc.append((WRFSCM_Hr_frac_ysu_hires, zzw, fac*da_ysu.transpose(), clabel, WRFSCM_zi_ysu_hires*facz)) 

            elif data2plot[id] == 'MYNNh':

                clabel = 'WRF-MYNN'
                color = 'magenta'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'ua'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'QVAPOR'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'uu'):
                    continue
                elif (var == 'vv'):
                    continue
                elif (var == 'ww'):
                    continue
                elif (var == 'tke'):
                    var_r = 'QKE'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 0.5         # QKE is 2*TKE
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    var_r = 'TSQ'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'qq'):
                    var_r = 'QSQ'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_hires
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e6
                elif (var == 'wt'):
                    continue
                elif (var == 'wq'):
                    continue

                facz = 1.e-3 # convert to [km]
            
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = var_z * facz
                    elif (z_grid == 1):
                        zzw = WRFSCM_3dvar_mynn_hires[var_z][WRFSCM_time_ind]
                    if var_s in WRFSCM_3dvar_mynn_hires:
                        da_int = list(WRFSCM_3dvar_mynn_hires[var_r])
                        db_int = list(WRFSCM_3dvar_mynn_hires[var_s])
                    else:
                        da_int = list(WRFSCM_3dvar_mynn_hires[var_r])
                else:
                    zzw = zwi
                    nt,nk = np.shape(WRFSCM_3dvar_mynn_hires[var_z])
                    if var_s in WRFSCM_3dvar_mynn_hires:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_mynn_hires[var_z][i],WRFSCM_3dvar_mynn_hires[var_r][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,WRFSCM_3dvar_mynn_hires[var_z][i],WRFSCM_3dvar_mynn_hires[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_mynn_hires[var_z][i], WRFSCM_3dvar_mynn_hires[var_r][i]) for i in range(nt)]                                    
            
                da_mynn = rollavg_pandas(da_int, num)  # centered time average
                if var_s in WRFSCM_3dvar_mynn_hires:
                    db_mynn = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):
                    da.append((i, fac*da_mynn[WRFSCM_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                    if var_s in WRFSCM_3dvar_mynn_hires:
                        db.append((i, fac*db_mynn[WRFSCM_time_ind[i]], zzw, color))
    
                dc.append((WRFSCM_Hr_frac_mynn_hires, zzw, fac*da_mynn.transpose(), clabel, WRFSCM_zi_mynn_hires*facz)) 

            elif data2plot[id] == 'YSUl':

                clabel = 'WRF-YSU-lo'
                color = 'blue'
                linestyle = 'dashed'

                if (var == 'u'):
                    var_r = 'ua'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'QVAPOR'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_ysu_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'ww'):
                    continue
                elif (var == 'tke'):
                    continue
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    continue
                elif (var == 'qq'):
                    continue
                elif (var == 'wt'):
                    continue
                elif (var == 'wq'):
                    continue
            
                facz = 1.e-3 # convert to [km]
            
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = var_z * facz
                    elif (z_grid == 1):
                        zzw = WRFSCM_3dvar_ysu_lores[var_z][WRFSCM_time_ind]
                    if var_s in WRFSCM_3dvar_ysu_lores:
                        da_int = list(WRFSCM_3dvar_ysu_lores[var_r])
                        db_int = list(WRFSCM_3dvar_ysu_lores[var_s])
                    else:
                        da_int = list(WRFSCM_3dvar_ysu_lores[var_r])
                else:
                    zzw = zwi
                    nt,nk = np.shape(WRFSCM_3dvar_ysu_lores[var_z])
                    if var_s in WRFSCM_3dvar_ysu_lores:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_ysu_lores[var_z][i],WRFSCM_3dvar_ysu_lores[var_r][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,WRFSCM_3dvar_ysu_lores[var_z][i],WRFSCM_3dvar_ysu_lores[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_ysu_lores[var_z][i], WRFSCM_3dvar_ysu_lores[var_r][i]) for i in range(nt)]                                    
            
                da_ysu = rollavg_pandas(da_int, num)  # centered time average
                if var_s in WRFSCM_3dvar_ysu_lores:
                    db_ysu = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):
                    da.append((i, fac*da_ysu[WRFSCM_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                    if var_s in WRFSCM_3dvar_ysu_lores:
                        db.append((i, fac*db_ysu[WRFSCM_time_ind[i]], zzw, color))
    
                dc.append((WRFSCM_Hr_frac_ysu_lores, zzw, fac*da_ysu.transpose(), clabel, WRFSCM_zi_ysu_lores*facz)) 

            elif data2plot[id] == 'MYNNl':

                clabel = 'WRF-MYNN-lo'
                color = 'orange'
                linestyle = 'dashed'

                if (var == 'u'):
                    var_r = 'ua'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 't'):
                    var_r = 'th'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'QVAPOR'
                    var_s = 'None'
                    if (z_grid == 0):
                        var_z = WRFSCM_z_mynn_lores
                    elif (z_grid == 1) or (z_grid == 2):
                        var_z = 'zu_zi'
                    fac = 1.e3
                elif (var == 'ww'):
                    continue
                elif (var == 'tke'):
                    continue
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    continue
                elif (var == 'qq'):
                    continue
                elif (var == 'wt'):
                    continue
                elif (var == 'wq'):
                    continue
            
                facz = 1.e-3 # convert to [km]
            
                if (z_grid == 0) or (z_grid == 1):
                    if (z_grid == 0):
                        zzw = var_z * facz
                    elif (z_grid == 1):
                        zzw = WRFSCM_3dvar_mynn_lores[var_z][WRFSCM_time_ind]
                    if var_s in WRFSCM_3dvar_mynn_lores:
                        da_int = list(WRFSCM_3dvar_mynn_lores[var_r])
                        db_int = list(WRFSCM_3dvar_mynn_lores[var_s])
                    else:
                        da_int = list(WRFSCM_3dvar_mynn_lores[var_r])
                    fac = 1.
                else:
                    zzw = zwi
                    nt,nk = np.shape(WRFSCM_3dvar_mynn_lores[var_z])
                    if var_s in WRFSCM_3dvar_mynn_lores:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_mynn_lores[var_z][i],WRFSCM_3dvar_mynn_lores[var_r][i]) for i in range(nt)]
                        db_int = [np.interp(zzw,WRFSCM_3dvar_mynn_lores[var_z][i],WRFSCM_3dvar_mynn_lores[var_s][i]) for i in range(nt)]
                    else:
                        da_int = [np.interp(zzw,WRFSCM_3dvar_mynn_lores[var_z][i], WRFSCM_3dvar_mynn_lores[var_r][i]) for i in range(nt)]                                    
            
                da_mynn = rollavg_pandas(da_int, num)  # centered time average
                if var_s in WRFSCM_3dvar_mynn_lores:
                    db_mynn = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):
                    da.append((i, fac*da_mynn[WRFSCM_time_ind[i]], zzw, color, clabel, linestyle))  # add data to list
                    if var_s in WRFSCM_3dvar_mynn_lores:
                        db.append((i, fac*db_mynn[WRFSCM_time_ind[i]], zzw, color))
    
                dc.append((WRFSCM_Hr_frac_mynn_hires, zzw, fac*da_mynn.transpose(), clabel, WRFSCM_zi_mynn_lores*facz)) 

            elif data2plot[id] == 'SOMCRUS':

                clabel = 'SOMCRUS'
                color = 'orange'
                linestyle = 'solid'

                if (var == 'u'):
                    continue
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif (var == 'uu'):
                    continue
                elif (var == 'vv'):
                    continue
                elif (var == 'ww'):
                    continue
                    var_r = 'ww_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    continue
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    continue
                elif (var == 'qq'):
                    continue
                elif (var == 'wt'):
                    continue
                    var_r = 'wt_s'
                    var_s = 'None'
                    var_z = 'zw'
                elif (var == 'wq'):
                    continue

                facz = 1.e-3 # convert to [km]

                zzw = facz * NCARLES.variables[var_z][:,:]   # using the NCARLES grid for now
                if var_s in SOMCRUS.variables:
                    da_int = SOMCRUS.variables[var_r][:,:]
                    db_int = SOMCRUS.variables[var_s][:,:]
                else:
                    da_int = SOMCRUS.variables[var_r][:,:]

                da_somcrus = rollavg_pandas(da_int, num)  # centered time average
                if var_s in SOMCRUS.variables:
                    db_somcrus = rollavg_pandas(db_int, num)

                for i in range(len(time2plot)):

                    da.append((i, fac*da_somcrus[SOMCRUS_time_ind[i],:], zzw[SOMCRUS_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in SOMCRUS.variables:
                        db.append((i, fac*db_somcrus[SOMCRUS_time_ind[i],:], zzw[SOMCRUS_time_ind[i],:], color))

                dc.append((SOMCRUS_time_hr, zzw[0,:], fac*da_somcrus.transpose(), clabel, np.array(SOMCRUS.variables['zi_t'])*facz))

            elif data2plot[id] == 'SCAM':    # --- SCAM

                clabel = 'SCAM'
                color = 'cyan'
                linestyle = 'solid'

                if (var == 'u'):
                    continue
                    var_r = 'ua'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 't'):
                    continue       # skipping SCAM theta for now, many values with 10^+200
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif (var == 'uu'):
                    var_r = 'uu_r'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_r'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'ww'):
                    var_r = 'ww_r'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'uw'):
                    continue
                elif (var == 'tt'):
                    var_r = 'tt_r'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'qq'):
                    var_r = 'qq_r'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'wt'):
                    var_r = 'wt_r'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'wq'):
                    var_r = 'wq_r'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3

                facz = 1.e-3 # convert to [km]

                zzw = facz * SCAM.variables[var_z][:,:]
                if var_s in SCAM.variables:
                    da_int = SCAM.variables[var_r][:,:]
                    db_int = SCAM.variables[var_s][:,:]
                else:
                    da_int = SCAM.variables[var_r][:,:]

                da_scam = rollavg_pandas(da_int, num)  # centered time average
                if var_s in SCAM.variables:
                    db_scam = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):
                    da.append((i, fac*da_scam[SCAM_time_ind[i],:], zzw[SCAM_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in SCAM.variables:
                        db.append((i, fac*db_scam[SCAM_time_ind[i],:], zzw[SCAM_time_ind[i],:], color))
    
                dc.append((SCAM_time_hr, zzw[0,:], fac*da_scam.transpose(), clabel, SCAM_zi*facz)) 

            elif data2plot[id] == 'CM1_CLUBB':    # --- CM1_CLUBB

                clabel = 'CM1-CLUBBX'
                color = 'darkkhaki'
                linestyle = 'solid'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif var == 'uu':
                    var_r = 'uu_s'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'vv'):
                    var_r = 'vv_s'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif var == 'ww':
                    var_r = 'ww_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'tt':
                    var_r = 'tt_s'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif var == 'qq':
                    var_r = 'qq_s'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'wu_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e3

                facz = 1.e-3 # convert to [km]

                zzw = facz * CM1_CLUBB.variables[var_z][:,:]
                if var_s in CM1_CLUBB.variables:
                    da_int = CM1_CLUBB.variables[var_r][:,:]
                    db_int = CM1_CLUBB.variables[var_s][:,:]
                else:
                    da_int = CM1_CLUBB.variables[var_r][:,:]

                da_cm1 = rollavg_pandas(da_int, num)  # centered time average
                if var_s in CM1_CLUBB.variables:
                    db_cm1 = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):

                    da.append((i, fac*da_cm1[CM1SCM_time_ind[i],:], zzw[CM1SCM_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in CM1_CLUBB.variables:
                        db.append((i, fac*db_cm1[CM1SCM_time_ind[i],:], zzw[CM1SCM_time_ind[i],:], color))
    
                dc.append((CM1_CLUBB_time_hr, zzw[0,:], fac*da_cm1.transpose(), clabel, np.array(CM1_CLUBB.variables['zi_t'])*facz)) 

            elif data2plot[id] == 'CM1_MYJ':    # --- CM1_MYJ

                clabel = 'CM1-MYJ'
                color = 'darkkhaki'
                linestyle = 'dashed'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif var == 'uu':
                    continue
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'vv'):
                    continue
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    var_z = 'zu'
                    fac = 1.
                elif var == 'ww':
                    continue
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'tt':
                    continue
                    var_r = 'tt_r'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'qq':
                    continue
                    var_r = 'qq_r'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'wu_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e3

                facz = 1.e-3 # convert to [km]

                zzw = facz * CM1_MYJ.variables[var_z][:,:]
                if var_s in CM1_MYJ.variables:
                    da_int = CM1_MYJ.variables[var_r][:,:]
                    db_int = CM1_MYJ.variables[var_s][:,:]
                else:
                    da_int = CM1_MYJ.variables[var_r][:,:]

                da_cm1 = rollavg_pandas(da_int, num)  # centered time average
                if var_s in CM1_MYJ.variables:
                    db_cm1 = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):

                    da.append((i, fac*da_cm1[CM1SCM_time_ind[i],:], zzw[CM1SCM_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in CM1_MYJ.variables:
                        db.append((i, fac*db_cm1[CM1SCM_time_ind[i],:], zzw[CM1SCM_time_ind[i],:], color))
    
                dc.append((CM1_MYJ_time_hr, zzw[0,:], fac*da_cm1.transpose(), clabel, np.array(CM1_MYJ.variables['zi_t'])*facz)) 

            elif data2plot[id] == 'CM1_MYNN_2.5':    # --- CM1_MYNN2.5

                clabel = 'CM1-MYNN2.5'
                color = 'darkkhaki'
                linestyle = 'dashdot'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif var == 'uu':
                    continue
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'vv'):
                    continue
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    var_z = 'zu'
                    fac = 1.
                elif var == 'ww':
                    continue
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'tt':
                    var_r = 'tsq'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'qq':
                    var_r = 'qsq'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'wu_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e3

                facz = 1.e-3 # convert to [km]

                zzw = facz * CM1_MYNN25.variables[var_z][:,:]
                if var_s in CM1_MYNN25.variables:
                    da_int = CM1_MYNN25.variables[var_r][:,:]
                    db_int = CM1_MYNN25.variables[var_s][:,:]
                else:
                    da_int = CM1_MYNN25.variables[var_r][:,:]

                da_cm1 = rollavg_pandas(da_int, num)  # centered time average
                if var_s in CM1_MYNN25.variables:
                    db_cm1 = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):

                    da.append((i, fac*da_cm1[CM1_time_ind[i],:], zzw[CM1_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in CM1_MYNN25.variables:
                        db.append((i, fac*db_cm1[CM1_time_ind[i],:], zzw[CM1_time_ind[i],:], color))
    
                dc.append((CM1_time_hr, zzw[0,:], fac*da_cm1.transpose(), clabel, np.array(CM1_MYNN25.variables['zi_t'])*facz)) 

            elif data2plot[id] == 'CM1_MYNN_3.0':    # --- CM1_MYNN3.0

                clabel = 'CM1-MYNN3.0'
                color = 'darkkhaki'
                linestyle = 'dotted'

                if (var == 'u'):
                    var_r = 'u'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'v'):
                    var_r = 'v'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 't'):
                    var_r = 't'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'q'):
                    var_r = 'q'
                    var_s = 'None'
                    var_z = 'zu'
                    fac = 1.e3
                elif var == 'uu':
                    continue
                    var_r = 'uu_r'
                    var_s = 'uu_s'
                    var_z = 'zu'
                    fac = 1.
                elif (var == 'vv'):
                    continue
                    var_r = 'vv_r'
                    var_s = 'vv_s'
                    var_z = 'zu'
                    fac = 1.
                elif var == 'ww':
                    continue
                    var_r = 'ww_r'
                    var_s = 'ww_s'
                    var_z = 'zw'
                    fac = 1.
                elif (var == 'tke'):
                    var_r = 'tke_s'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'tt':
                    var_r = 'tsq'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'qq':
                    var_r = 'qsq'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e6
                elif (var == 'uw'):
                    var_r = 'wu_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wt':
                    var_r = 'wt_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.
                elif var == 'wq':
                    var_r = 'wq_s_ed'
                    var_s = 'None'
                    var_z = 'zw'
                    fac = 1.e3

                facz = 1.e-3 # convert to [km]

                zzw = facz * CM1_MYNN30.variables[var_z][:,:]
                if var_s in CM1_MYNN30.variables:
                    da_int = CM1_MYNN30.variables[var_r][:,:]
                    db_int = CM1_MYNN30.variables[var_s][:,:]
                else:
                    da_int = CM1_MYNN30.variables[var_r][:,:]

                da_cm1 = rollavg_pandas(da_int, num)  # centered time average
                if var_s in CM1_MYNN30.variables:
                    db_cm1 = rollavg_pandas(db_int, num)
    
                for i in range(len(time2plot)):

                    da.append((i, fac*da_cm1[CM1_time_ind[i],:], zzw[CM1_time_ind[i],:], color, clabel, linestyle))  # add data to list
                    if var_s in CM1_MYNN30.variables:
                        db.append((i, fac*db_cm1[CM1_time_ind[i],:], zzw[CM1_time_ind[i],:], color))
    
#               dc.append((CM1_time_hr, zzw[0,:], fac*da_cm1.transpose(), clabel, np.array(CM1_MYNN30.variables['zi_t'])*facz)) 
    
            elif data2plot[id] == 'OBS':    # --- Observations
    
                if var == 'u':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_u[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_u.transpose(), clabel))

                elif var == 'v':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_v[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_v.transpose(), clabel))
    
                elif var == 'uu':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_uu[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uu.transpose(), clabel))
    
                elif var == 'vv':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_vv[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_vv.transpose(), clabel))
    
                elif var == 'ww':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_ww[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_ww.transpose(), clabel))

                elif var == 'tke':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_tke[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_tke.transpose(), clabel))
    
                elif var == 'uw':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_uw[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

                elif var == 'wt':
    
                    clabel = 'C-130'
                    facz = 1.e-3  # convert [m] -> [km]
    
#                   for i in range(len(time2plot)):
#                       do.append((i,c130_wt, c130_alt*facz, clabel))

                    do.append((2,c130_wt, c130_alt*facz, clabel))

#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

                elif var == 'wq':
    
                    clabel = 'C-130'
                    facz = 1.e-3  # convert [m] -> [km]
    
#                   for i in range(len(time2plot)):
#                       do.append((i,c130_wq, c130_alt*facz, clabel))
                    do.append((2,c130_wq, c130_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

        # ---- if we're plotting SCM results, calculate an average LES result
        #   NOTE: used db-array to store just the LES results for this purpose

        if (SCM == 'True'):

            # ---- declare some variables

            nl = len(dl)
            nt = len(time2plot)
            nz = len(zwi)
            nc = int(nl/nt)

            dl_z = np.empty((nl,nz), dtype=float)
            dl_d = np.empty((nl,nz), dtype=float)

            dl_z_tmp = np.empty((nc,nz), dtype=float)
            dl_d_tmp = np.empty((nc,nz), dtype=float)

            dl_z_avg = np.empty((nt,nz), dtype=float)
            dl_d_avg = np.empty((nt,nz), dtype=float)
            dl_d_min = np.empty((nt,nz), dtype=float)
            dl_d_max = np.empty((nt,nz), dtype=float)

            # ---- grab profile data from within data structure

            for i in range(nl):
                n = dl[i]
                dl_d[i,:] = n[0]  # data
                dl_z[i,:] = n[1]  # heights

            # ---- fill temp variable with data from different
            #      LES codes, but at like-times, calculate stats
            #
            #      surely there's a faster/cleaner numpy way to do 
            #      this and not need to use temporary variables...

            for i in range(nt):

                for ic in range(nc):
                    dl_z_tmp[ic,:] = dl_z[i+ic*nt,:]
                    dl_d_tmp[ic,:] = dl_d[i+ic*nt,:]

                # ---- calculate statistics at this time

                dl_z_avg[i,:] = np.mean(dl_z_tmp, axis=0)
                dl_d_avg[i,:] = np.mean(dl_d_tmp, axis=0)
                dl_d_min[i,:] = np.min (dl_d_tmp, axis=0)
                dl_d_max[i,:] = np.max (dl_d_tmp, axis=0)


#               dl_z_avg[i,:] = np.percentile(dl_z_tmp, 50, axis=0)
#               dl_d_avg[i,:] = np.percentile(dl_d_tmp, 50, axis=0)
#               dl_d_min[i,:] = np.percentile(dl_d_tmp,  5, axis=0)
#               dl_d_max[i,:] = np.percentile(dl_d_tmp, 95, axis=0)

            color = (0,0,0,.6)
            for i in range(nt):
                db.append((i, dl_d_avg[i,:], dl_z_avg[i,:], 
                              dl_d_min[i,:], dl_d_max[i,:], 
                              color, 'LES-AVG'))

        # ---- setup axis ticks and titles for profile plots
    
        xmin       = np.empty(len(time2plot), dtype=object)
        xmax       = np.empty(len(time2plot), dtype=object)
        xfrq_major = np.empty(len(time2plot), dtype=object)
        xfrq_minor = np.empty(len(time2plot), dtype=object)
        x_title    = np.empty(len(time2plot), dtype=object)
    
        ymin       = np.empty(len(time2plot), dtype=object)
        ymax       = np.empty(len(time2plot), dtype=object)
        yfrq_major = np.empty(len(time2plot), dtype=object)
        yfrq_minor = np.empty(len(time2plot), dtype=object)
        y_title    = np.empty(len(time2plot), dtype=object)
        
        # ---- setup axis ticks and titles for the current variable
    
        if var == 'u':
    
            var_label = r"$\overline{u}$~~[m s$^{-1}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    if ('OBS' in data2plot):
                        xmin[i] = -1.0
                        xmax[i] = 9.0
                        xfrq_major[i] = 2
                        xfrq_minor[i] = 4
                    else:
                        xmin[i] = 0.0
                        xmax[i] = 2.2
                        xfrq_major[i] = 1
                        xfrq_minor[i] = 5
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.4
                    xmax[i] = 2.0
                    xfrq_major[i] = 1
                    xfrq_minor[i] = 5

        elif var == 'v':
    
            var_label = r"$\overline{v}$~~[m s$^{-1}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    if ('OBS' in data2plot):
                        xmin[i] = -1.0
                        xmax[i] = 4.00
                        xfrq_major[i] = 1.0
                        xfrq_minor[i] = 5
                    else:
                        xmin[i] = -0.1
                        xmax[i] = 0.62
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 4
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.04
                    xmax[i] = 0.6
                    xfrq_major[i] = 0.2
                    xfrq_minor[i] = 4

        elif var == 't':
    
            var_label = r"$\overline{\theta}$~~[K]"
    
            # ---- profile plots

            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    xmin[i] = 297.5
                    xmax[i] = 304.5
                    xfrq_major[i] = 2
                    xfrq_minor[i] = 4
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = 298.0
                    xmax[i] = 301.6
                    xfrq_major[i] = 1
                    xfrq_minor[i] = 5

        elif var == 'q':
    
            var_label = r"$\overline{q}$~~[g kg$^{-1}$]"
    
            # ---- profile plots
    
            if (SCM == 'True'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 12.0
                    xfrq_major[i] = 5
                    xfrq_minor[i] = 5
            else:
                if (figs == 'profiles') or (figs == 'combined'):
                    for i in range(len(time2plot)):
#                       xmin[i] = 0.0
                        xmin[i] = -1.0
                        xmax[i] = 11.0
                        xfrq_major[i] = 5
                        xfrq_minor[i] = 5
                elif (figs == 'profiles_surface'):
                    for i in range(len(time2plot)):
                        xmin[i] = 8.0
                        xmax[i] = 11.0
                        xfrq_major[i] = 1
                        xfrq_minor[i] = 5

        elif var == 'p':
    
            var_label = r"$\overline{p}$~~[Pa]"
    
            # ---- profile plots
    
            if (SCM == 'True'):
                for i in range(len(time2plot)):
                    xmin[i] = 7.5e4
                    xmax[i] = 10.2e4
                    xfrq_major[i] = 5
                    xfrq_minor[i] = 5
            else:
                if (figs == 'profiles') or (figs == 'combined'):
                    for i in range(len(time2plot)):
                        xmin[i] = 7.5e4
                        xmax[i] = 10.2e4
                        xfrq_major[i] = 1e4
                        xfrq_minor[i] = 5
                elif (figs == 'profiles_surface'):
                    for i in range(len(time2plot)):
                        xmin[i] = 7.5e4
                        xmax[i] = 10.2e4
                        xfrq_major[i] = 1e4
                        xfrq_minor[i] = 5
    
        elif var == 'uu':
    
            var_label = r"$\overline{u'^{\,2}}$~~[m$^{2}$ s$^{-2}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    if ('OBS' in data2plot):
                       xmin[i] =  0.0
                       xmax[i] =  5.0
                       xfrq_major[i] = 1
                       xfrq_minor[i] = 5
                    else:
                       if (SCM == 'True'):
                          xmin[i] =  0.0
                          xmax[i] =  2.8
                       else:
                          xmin[i] =  0.0
                          xmax[i] =  1.6
                       xfrq_major[i] = 1
                       xfrq_minor[i] = 5
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] =  0.0
                    xmax[i] =  1.5
                    xfrq_major[i] = 1
                    xfrq_minor[i] = 4
    
        elif var == 'vv':
    
            var_label = r"$\overline{v'^{\,2}}$~~[m$^{2}$ s$^{-2}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    if ('OBS' in data2plot):
                       xmin[i] =  0.0
                       xmax[i] =  5.0
                       xfrq_major[i] = 1
                       xfrq_minor[i] = 5
                    else:
                       if (SCM == 'True'):
                          xmin[i] =  0.0
                          xmax[i] =  2.8
                       else:
                          xmin[i] =  0.0
                          xmax[i] =  1.6
                       xfrq_major[i] = 1
                       xfrq_minor[i] = 5
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 2.0
                    xfrq_major[i] = 1.
                    xfrq_minor[i] = 5
            
        elif var == 'ww':
    
            var_label = r"$\overline{w'^{\,2}}$~~[m$^{2}$ s$^{-2}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 1.8
                    xfrq_major[i] = 1.
                    xfrq_minor[i] = 5
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 1.5
                    xfrq_major[i] = 1.
                    xfrq_minor[i] = 4

        elif var == 'tke':
    
            var_label = r"TKE~~[m$^2$ s$^{-2}$]"
    
            # ---- profile plots
    
            for i in range(len(time2plot)):
                if (SCM == 'True'):
                    xmin[i] = -0.2
                    xmax[i] =  3.4
                    xfrq_major[i] = 1.
                    xfrq_minor[i] = 5
                else:
                    if ('OBS' in data2plot):
                        xmin[i] = 0.0
                        xmax[i] = 5.0
                        xfrq_major[i] = 1.
                        xfrq_minor[i] = 5
                    else:
                        xmin[i] = 0.0
                        xmax[i] = 2.0
                        xfrq_major[i] = 1.
                        xfrq_minor[i] = 5

        elif var == 'tt':
    
            var_label = r"$\overline{\theta'^{\,2}}$~~[K$^{2}$]"
    
            # ---- profile plots
    
            if (SCM == 'True'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 0.9
                    xfrq_major[i] = 0.2
                    xfrq_minor[i] = 4
            else:
                if (figs == 'profiles') or (figs == 'combined'):
                    for i in range(len(time2plot)):
                        xmin[i] = 0.0
                        xmax[i] = 0.5
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 4
                elif (figs == 'profiles_surface'):
                    for i in range(len(time2plot)):
                        xmin[i] = 0.0
                        xmax[i] = 0.22
                        xfrq_major[i] = 0.1
                        xfrq_minor[i] = 5

        elif var == 'qq':
    
            var_label = r"$\overline{q'^{\,2}}$~~[(g kg$^{-1}$)$^2$]"
    
            # ---- profile plots
    
            if (SCM == 'True'):
                for i in range(len(time2plot)):
                    xmin[i] = 0.0
                    xmax[i] = 11.0
                    xfrq_major[i] = 5.
                    xfrq_minor[i] = 5
            else:
                if (figs == 'profiles') or (figs == 'combined'):
                    for i in range(len(time2plot)):
                        xmin[i] = 0.0
                        xmax[i] = 5.4
                        xfrq_major[i] = 1.
                        xfrq_minor[i] = 5
                elif (figs == 'profiles_surface'):
                    for i in range(len(time2plot)):
                        xmin[i] = 0.0
                        xmax[i] = 0.5
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 4
    
        elif var == 'uw':
    
            var_label = r"$\overline{u'w'}$~~[m$^{2}$ s$^{-2}$]"
    
            # ---- profile plots
    
            for i in range(len(time2plot)):
                if (SCM == 'True'):
                    xmin[i] = -0.09
                    xmax[i] = 0.01
                    xfrq_major[i] = 0.05
                    xfrq_minor[i] = 5
                else:
                    if ('OBS' in data2plot):
                        xmin[i] = -0.45
                        xmax[i] =  0.25 
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 4
                    else:
                        xmin[i] = -0.07
                        xmax[i] = 0.01
                        xfrq_major[i] = 0.05
                        xfrq_minor[i] = 5

        elif var == 'vw':
    
            var_label = r"$\overline{v'w'}$~~[m$^{2}$ s$^{-2}$]"
    
            # ---- profile plots
    
            for i in range(len(time2plot)):
                if (SCM == 'True'):
                    xmin[i] = -0.04
                    xmax[i] = 0.02
                    xfrq_major[i] = 0.04
                    xfrq_minor[i] = 4
                else:
                    if ('OBS' in data2plot):
                        xmin[i] = -0.45
                        xmax[i] =  0.25 
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 4
                    else:
                        xmin[i] = -0.035
                        xmax[i] =  0.025
                        xfrq_major[i] = 0.02
                        xfrq_minor[i] = 4
    
        elif var == 'wt':
    
            var_label = r"$\overline{w'\theta'}$~~[m K s$^{-1}$]"
    
            # ---- profile plots
    
            if (figs == 'profiles') or (figs == 'combined'):
                for i in range(len(time2plot)):
                    xmin[i] = -.08
                    xmax[i] = 0.12
                    xfrq_major[i] = 0.1
                    xfrq_minor[i] = 5
            elif (figs == 'profiles_surface'):
                for i in range(len(time2plot)):
                    xmin[i] = -.02
                    xmax[i] = 0.14
                    xfrq_major[i] = 0.1
                    xfrq_minor[i] = 5

        elif var == 'wq':
    
            var_label = r"$\overline{w'q'}$~~[m s$^{-1}$ g kg$^{-1}$]"
    
            # ---- profile plots
    
            if (SCM == 'True'):
                for i in range(len(time2plot)):
                    xmin[i] = -.06
                    xmax[i] = 0.26
                    xfrq_major[i] = 0.1
                    xfrq_minor[i] = 5
            else:
                if (figs == 'profiles') or (figs == 'combined'):
                    for i in range(len(time2plot)):
                        xmin[i] = -.02
                        xmax[i] = 0.26
                        xfrq_major[i] = 0.1
                        xfrq_minor[i] = 5
                elif (figs == 'profiles_surface'):
                    for i in range(len(time2plot)):
                        xmin[i] = -.02
                        xmax[i] = 0.2
                        xfrq_major[i] = 0.2
                        xfrq_minor[i] = 5

        # ---- y-axis is the same for all profile plots
    
        if z_grid == 0:
            y_title[0] = r'$z$~~[km]'
            if (figs == 'profiles') or (figs == 'combined'):
                if (SCM == 'True'):
                    for i in range(len(time2plot)):
                        ymin[i] = 0.
                        ymax[i] = 2.6
                        yfrq_major[i] = 1
                        yfrq_minor[i] = 5
                else:
                    for i in range(len(time2plot)):
                        ymin[i] = 0.
                        ymax[i] = 2.4
                        yfrq_major[i] = 1
                        yfrq_minor[i] = 5

            elif (figs == 'profiles_surface'):
                if (var == 'u') or (var == 'v') or (var == 't') or (var == 'q'):
                    for i in range(len(time2plot)):
                        ymin[i] = 0.005
                        ymax[i] = 0.2
                else:
                    for i in range(len(time2plot)):
                        ymin[i] = 0.
                        ymax[i] = 0.2
                        yfrq_major[i] = 0.1
                        yfrq_minor[i] = 5
        else:
            y_title[0] = r'$z / z_i$'
            for i in range(len(time2plot)):
                ymin[i] = 0.
                ymax[i] = 1.4
                yfrq_major[i] = 0.2
                yfrq_minor[i] = 4
            
        y_title[1:-2] = ' '
        y_title[-1] = y_title[0]
            
        # ---- configure desired ticks/titles for the contour plots
    
        cont_xmin       = np.empty(1, dtype=object)
        cont_xmax       = np.empty(1, dtype=object)
        cont_xfrq_major = np.empty(1, dtype=object)
        cont_xfrq_minor = np.empty(1, dtype=object)
        cont_x_title    = np.empty(1, dtype=object)
    
        cont_ymin       = np.empty(1, dtype=object)
        cont_ymax       = np.empty(1, dtype=object)
        cont_yfrq_major = np.empty(1, dtype=object)
        cont_yfrq_minor = np.empty(1, dtype=object)
        cont_y_title    = np.empty(1, dtype=object)

        # ---- contour plots
        # ---- x- and y-axes are the same for all variables
    
        cont_xmin = 8.
        cont_xmax = 18.0
        cont_xfrq_major = 1
        cont_xfrq_minor = 4
        cont_x_title = "Time [hr LT]"
    
        if z_grid == 0:
            cont_y_title = r"$z$~~\huge{[km]}"
        else:
            cont_y_title = r"$z / z_i$"
    
        if z_grid == 0:
            if (SCM == 'True'):
                cont_ymin = 0.
                cont_ymax = 2.6
                cont_yfrq_major = 1.0
                cont_yfrq_minor = 5
            else:
                cont_ymin = 0.
                cont_ymax = 2.4
                cont_yfrq_major = 1.0
                cont_yfrq_minor = 5
        else:
            cont_ymin = 0.
            cont_ymax = 1.4
            cont_yfrq_major = 0.2
            cont_yfrq_minor = 4

        # ---- find variable max/min for contours
    
        amin = +999999.
        amax = -999999.
        vmin = amin
        vmax = amax
    
        if ('OBS' in data2plot):   # currently skipping OBS when setting contour intervals
            xx = len(dc) - 1
#       elif ('SCM' == 'True'): 
#           xx = 1
        else:
            xx = len(dc)

        for i in range(xx):
            n = dc[i]
            x_min_ind = np.argmin(np.abs(n[0] - cont_xmin))
            x_max_ind = np.argmin(np.abs(n[0] - cont_xmax))
            y_min_ind = np.argmin(np.abs(n[1] - cont_ymin))
            y_max_ind = np.argmin(np.abs(n[1] - cont_ymax))
            amin = np.min( n[2][y_min_ind:y_max_ind, x_min_ind:x_max_ind] )
            amax = np.max( n[2][y_min_ind:y_max_ind, x_min_ind:x_max_ind] )
            if amin < vmin:
                vmin = amin
            if amax > vmax:
                vmax = amax
    
    #   cont_lev = ticker.MaxNLocator(nbins='auto').tick_values(vmin, vmax) # find nicely distributed levels between vmin/vmax
        cont_lev = ticker.MaxNLocator().tick_values(vmin, vmax) # find nicely distributed levels between vmin/vmax
            
        # ---- collect those settings for more general use
    
        cont_ticks_titles = {'xmin': cont_xmin, 'xmax': cont_xmax,
                             'xfrq_major': cont_xfrq_major, 'xfrq_minor': cont_xfrq_minor, 'x_title': cont_x_title,
                             'ymin': cont_ymin, 'ymax': cont_ymax,
                             'yfrq_major': cont_yfrq_major, 'yfrq_minor': cont_yfrq_minor, 'y_title': cont_y_title,
                             'levels': cont_lev}
    
        ticks_titles = {'xmin': xmin, 'xmax': xmax, 'xfrq_major': xfrq_major, 'xfrq_minor': xfrq_minor, 'x_title': x_title,
                        'ymin': ymin, 'ymax': ymax, 'yfrq_major': yfrq_major, 'yfrq_minor': yfrq_minor, 'y_title': y_title}
    
        # ---- build plot

        if (figs == 'combined'):
    
            axc = [None] * len(dc)
            axp = [None] * len(time2plot)
    
            fig = plt.figure(figsize=(12, 12))
    
            gc = plt.GridSpec(len(dc), 1)
            gc.update(left=0.07, right=0.93, top=0.92, bottom=0.38, hspace=0.2)
    
            for i in range(len(dc)):
                axc[i] = fig.add_subplot(gc[i, 0:])  # contouor plots span all x
    
            gp = plt.GridSpec(1, len(time2plot))
            gp.update(left=0.07, right=0.93, top=0.30, bottom=0.08, wspace=0.15)
    
            for it in range(len(time2plot)):
                axp[it] = fig.add_subplot(gp[0, it])           # configure lower panels to produce one line plot per 'it'
        
            # ---- create the plots 
         
            plot_contour_1var_Nx1(dc, cont_ticks_titles)       # create contour plots
            plot_profile_2var_1x3(da, db, do, ticks_titles)    # create line plots
        
            # ---- lay a few items over top
        
            for ic in range(len(dc)):
                for it in range(len(time2plot)):
                    axc[ic].axvline(x=time2plot[it], color='black', linestyle='dashed', dashes=[6, 6], linewidth=1)
        
        elif (figs == 'profiles') or (figs == 'profiles_surface'):
    
            axp = [None] * len(time2plot)
    
            fig = plt.figure(figsize=(12, 4))
    
            gp = plt.GridSpec(1, len(time2plot))
            if (figs == 'profiles'):
                gp.update(left=0.06, right=0.94, top=0.95, bottom=0.21, wspace=0.12)
            else:
                gp.update(left=0.08, right=0.92, top=0.95, bottom=0.21, wspace=0.12)
    
            for it in range(len(time2plot)):
                axp[it] = fig.add_subplot(gp[0, it])           # configure lower panels to produce one line plot per 'it'
        
            # ---- create the plots 
            
            plot_profile_2var_1x3(da, db, do, ticks_titles)    # create line plots
        
        elif (figs == 'contours'):
    
            axc = [None] * len(dc)
    
            fig = plt.figure(figsize=(12, 12))
    
            gc = plt.GridSpec(len(dc), 1)
            gc.update(left=0.07, right=0.93, top=0.92, bottom=0.08, hspace=0.2)
    
            for i in range(len(dc)):
                axc[i] = fig.add_subplot(gc[i, 0:])  # contouor plots span all x
    
            # ---- create the plots 
         
            plot_contour_1var_Nx1(dc, cont_ticks_titles)       # create contour plots
        
            # ---- lay a few items over top
        
            for ic in range(len(dc)):
                for it in range(len(time2plot)):
                    axc[ic].axvline(x=time2plot[it], color='black', linestyle='dashed', dashes=[6, 6], linewidth=1)
        
        # ---- export file

        if (single_file == 0):
            if (SCM is 'True'):
                if (figs == 'profiles'):
                    if (output_file_type == 0):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/pdf/met_prof+obs.scm."+var+".pdf")
                        else:
                            plt.savefig("../plots/pdf/met_prof.scm."+var+".pdf")
                    elif (output_file_type == 1):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/png/met_prof+obs.scm."+var+".png", dpi=600, bbox_inches='tight')
                        else:
                            plt.savefig("../plots/png/met_prof.scm."+var+".png", dpi=600, bbox_inches='tight')
                if (figs == 'contours'):
                    if (output_file_type == 0):
                        plt.savefig("../plots/pdf/met_hov.scm."+var+".pdf")
                    elif (output_file_type == 1):
                        plt.savefig("../plots/png/met_hov.scm."+var+".png", dpi=600, bbox_inches='tight')
                if (figs == 'combined'):
                    if (output_file_type == 0):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/pdf/met_hov+prof+obs.scm."+var+".pdf")
                        else:
                            plt.savefig("../plots/pdf/met_hov+prof.scm."+var+".pdf")
                    elif (output_file_type == 1):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/png/met_hov+prof+obs.scm."+var+".png", dpi=600, bbox_inches='tight')
                        else:
                            plt.savefig("../plots/png/met_hov+prof.scm."+var+".png", dpi=600, bbox_inches='tight')
            elif (SCM is 'False'):
                if (figs == 'profiles'):
                    if (output_file_type == 0):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/pdf/met_prof+obs."+var+".pdf")
                        else:
                            plt.savefig("../plots/pdf/met_prof."+var+".pdf")
                    elif (output_file_type == 1):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/png/met_prof+obs."+var+".png", dpi=600, bbox_inches='tight')
                        else:
                            plt.savefig("../plots/png/met_prof."+var+".png", dpi=600, bbox_inches='tight')
                if (figs == 'profiles_surface'):
                    if (output_file_type == 0):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/pdf/met_prof_surf+obs."+var+".pdf")
                        else:
                            plt.savefig("../plots/pdf/met_prof_surf."+var+".pdf")
                    elif (output_file_type == 1):
                        plt.savefig("../plots/png/met_prof_surf."+var+".png", dpi=600, bbox_inches='tight')
                if (figs == 'contours'):
                    if (output_file_type == 0):
                        plt.savefig("../plots/pdf/met_hov."+var+".pdf")
                    elif (output_file_type == 1):
                        plt.savefig("../plots/png/met_hov."+var+".png", dpi=600, bbox_inches='tight')
                if (figs == 'combined'):
                    if (output_file_type == 0):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/pdf/met_hov+prof+obs."+var+".pdf")
                        else:
                            plt.savefig("../plots/pdf/met_hov+prof."+var+".pdf")
                    elif (output_file_type == 1):
                        if ('OBS' in data2plot):
                            plt.savefig("../plots/png/met_hov+prof+obs."+var+".png", dpi=600, bbox_inches='tight')
                        else:
                            plt.savefig("../plots/png/met_hov+prof."+var+".png", dpi=600, bbox_inches='tight')
        else:
            pdf.savefig( fig )
        plt.close( fig )

if (single_file == 1):
    pdf.close()
