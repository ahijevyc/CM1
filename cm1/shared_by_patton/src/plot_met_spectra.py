#!/usr/bin/env python3

exec(open('import_packages.py').read())
exec(open('definitions.py').read())
exec(open('read_les_ncar.py').read())
exec(open('read_les_wrf.py').read())
exec(open('read_les_fe.py').read())
exec(open('read_les_cm1.py').read())
exec(open('read_les_dales.py').read())
exec(open('read_obs_lidar.py').read())

def plot_profile_2var_1x3 (da, config):

    # ---- function to plot three sets of vertical profiles of two variables each 
    #      (e.g. tot + sgs) laid out in a 1row x 3column three-panel arrangement 
    #
    #   NOTE: in order to enable modification to the figure following a call to this
    #         routine, the routine does not show or close the plot, or export a file.

    for j in range(len(hgt2plot)):
        for i in range(len(time2plot)):
            k = j*(len(time2plot))+i
            axp[k].tick_params(axis='both', which='both', direction='out', labelsize='medium', pad=3)
            axp[k].tick_params(axis='both', which='major', length=5.5, width=1)
            axp[k].tick_params(axis='both', which='minor', length=3., width=0.7)
            axp[k].tick_params(axis='x', which='both', top='True')
            axp[k].tick_params(axis='y', which='both', right='True')

#   marker_style = dict(color='black', linestyle='-', marker='o',
#                   markersize=3, linewidth=0.5)

    # --- add lines to each plot

    for id in range(len(data2plot)):
        for j in range(len(hgt2plot)):
            for i in range(len(time2plot)):
                k = id*(len(hgt2plot)*len(time2plot)) + j*(len(time2plot))+i
                n = da[k]
                axp[n[0]].plot(n[1], n[2], color=n[3], linestyle=n[5], linewidth=2, label=n[4]) # ---- resolved quantities

#   for n in do:
#       axp[n[0]].plot(n[1], n[2], fillstyle='none', label=n[3], **marker_style)         # ---- observations

    # ---- x-axis

    for j in range(len(hgt2plot)):
        for i in range(len(time2plot)):
            k = j*(len(time2plot))+i
            axp[k].set_xscale('log')
            axp[k].set_xlim([config['xmin'][i], config['xmax'][i]])
            axp[k].xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
            axp[k].xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))

    j = len(hgt2plot)-1
    for i in range(len(time2plot)):
        k = j*(len(time2plot))+i
        axp[k].set_xlabel(config['x_title'][i], fontsize='large', labelpad=6)

    for j in range(len(hgt2plot)-1):
        for i in range(len(time2plot)):
            k = j*(len(time2plot))+i
            axp[k].xaxis.set_ticklabels([])
            axp[k].xaxis.set_ticks_position('both')

    # ---- y-axis

#   if (var == 'uw') or (var == 'wt') or (var == 'wq'):
    if (var == 'uw'):
        for j in range(len(hgt2plot)):
            for i in range(len(time2plot)):
                k = j*(len(time2plot))+i
                axp[k].set_ylim([config['ymin'][i], config['ymax'][i]])
    else:
        for j in range(len(hgt2plot)):
            for i in range(len(time2plot)):
                k = j*(len(time2plot))+i
                axp[k].set_yscale('log')
                axp[k].set_ylim([config['ymin'][i], config['ymax'][i]])
                axp[k].yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
                axp[k].yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))


    i = 0
    for j in range(len(hgt2plot)):
        kl = j*(len(time2plot))+i
        kr = (j+1)*(len(time2plot))-1
        axp[kl].set_ylabel(config['y_title'][i], fontsize='large', labelpad=7)
        axp[kr].set_ylabel(config['y_title'][i], fontsize='large', labelpad=7)
        axp[kr].yaxis.set_label_position("right")
        axp[kr].yaxis.tick_right()
        axp[kr].yaxis.set_ticks_position('both')

    for j in range(len(hgt2plot)):
        for i in range(1,len(time2plot)-1):
            k = j*(len(time2plot))+i
            axp[k].yaxis.set_ticklabels([])
            axp[k].yaxis.set_ticks_position('both')

    # ---- add legend

    axp[-1].legend(loc='lower left',fontsize='small', frameon='True', borderpad=0.5,
                  framealpha=1.0,
                  borderaxespad=0.7, handlelength=2.8, handletextpad=0.6,
                  labelspacing=0.3, edgecolor='dimgray')

    # ---- lay a few items over top

    time_label_x = 0.64
    time_label_y = 0.95

    j = 0
    for i in range(len(time2plot)):
        k = j*(len(time2plot))+i
        axp[k].text(time_label_x, time_label_y, 
                     '{time:0>4.0f} LT'.format(time=time2plot[i]*100),
                     transform=axp[k].transAxes,
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize='medium', color='black')

    hgt_label_x = 0.08
    hgt_label_y = 0.15

    i = 0
    for j in range(len(hgt2plot)):
        k = j*(len(time2plot))+i
        axp[k].text(hgt_label_x, hgt_label_y, 
                     r'$z/z_i$ = {hgt:3.1f}'.format(hgt=hgt2plot[j]),
                     transform=axp[k].transAxes,
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize='medium', color='black')

    # ---- add line depicting -5/3 slope

#   if (var == 'uw') or (var == 'wt') or (var == 'wq'):
    if (var == 'uw'):
        pass
    else:

        slope = -5./3.
        x1 = 5.           # starting x-location
        x2 = x1 * 10.     # ending x-location
        xx = [x1, x2]

        for j in range(len(hgt2plot)):
            for i in range(len(time2plot)):
                k = j*(len(time2plot))+i
                y1 = config['ymax'][i] / 10.
                y_intercept = np.log10(y1) - slope*np.log10(x1)
                y2 = np.power(10.,(slope*np.log10(x2) + y_intercept))
                yy = [y1, y2]
                axp[k].plot(xx, yy, color='black', linestyle='dashed', linewidth=1) # ---- resolved quantities

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

#print(plt.rcParams.keys())

# ----- select if you'd like separate files per variable, or a single file

single_file = 0    # =0, individual files; =1, export all figs to single file
output_file_type = 1    # =0, PDF; =1, PNG (only works with: single_file=0)

if (single_file == 1):
    pdf = matplotlib.backends.backend_pdf.PdfPages("../plots/met_spectra.all.pdf")

# ----- select the output style

figs2plot = [ 'spectra' ]

# ----- select which data to plot

#data2plot = [ 'FE', 'WRF', 'DALES', 'NCAR', 'OBS']
#data2plot = [ 'FE', 'WRF', 'DALES', 'CM1', 'NCAR']

#data2plot = [ 'CM1', 'DALES', 'NCAR' ]
data2plot = [ 'CM1', 'NCAR' ]

# ----- set variables to plot

vars2plot = [ 'uu', 'vv', 'ww', 'tt', 'qq', 'uw', 'wt', 'wq']
#vars2plot = [ 'uu' ]

# ----- select the times to plot

time2plot = [ 10., 12., 14., 16. ]

# --- specify averaging duration (in 5-min chunks, i.e. 12 = 60 min avg)

num = 12  # number of data points in rolling average centered at time

# ----- select the normalized [z/zi] heights to plot

hgt2plot = [ 0.9, 0.5, 0.1 ]
#hgt2plot = [ 0.5, 0.1 ]
#hgt2plot = [ 0.5 ]

# ----- build time indices

WRFLES_time_ind = [None] * len(time2plot)
NCARLES_time_ind = [None] * len(time2plot)
FE_time_ind = [None] * len(time2plot)
CM1_time_ind = [None] * len(time2plot)
DALES_time_ind = [None] * len(time2plot)
LIDAR_time_ind = [None] * len(time2plot)

for it in range(len(time2plot)):
    WRFLES_time_ind[it] = np.argmin(np.abs(WRF_time_hr - time2plot[it]))
    NCARLES_time_ind[it] = np.argmin(np.abs(NCARLES_time_hr - time2plot[it]))
    FE_time_ind[it] = np.argmin(np.abs(FE['time'] - time2plot[it]))
    CM1_time_ind[it] = np.argmin(np.abs(CM1_time_hr - time2plot[it]))
    DALES_time_ind[it] = np.argmin(np.abs(DALES_time_hr - time2plot[it]))
    LIDAR_time_ind[it] = np.argmin(np.abs(LIDAR_time_hr - time2plot[it]))

# --- build z/zi grid into which data will be interpolated

z_grid = 0   # =0 -> km 
             # =1 -> z/zi
             # =2 -> data interpolated in to z/zi grid

nt,nk = np.shape(wrfchem_2dvar['zu_zi'])
zwi = np.empty([nk], dtype=object)

ztop = 1500.
zl = 3000
zwi = np.linspace(0,zl,nk) / ztop

# ---- find indices pointing to selected heights

hgt_ind = [None] * len(hgt2plot)
for k in range(len(hgt2plot)):
    hgt_ind[k] = np.argmin(np.abs(zwi - hgt2plot[k]))

# ---- loop over plot type

for figs in figs2plot:

    print(' working on: ',figs)

    for var in vars2plot:                      # loop over variable to plot

        print('     var: ',var)

        da = []
        do = []

        for id in range(len(data2plot)):       # loop over data types, i.e. LES, OBS

            if data2plot[id] == 'FE':        # ---- FastEddy

                clabel = 'FastEddy'
                color = 'mediumseagreen'
                linestyle = 'solid'
    

            elif data2plot[id] == 'WRF':     # ---- WRF

                clabel = 'WRF'
                color = 'blue'
                linestyle = 'solid'


            elif data2plot[id] == 'DALES':    # --- DALES

                clabel = 'DALES'
                color = 'crimson'
                linestyle = 'solid'

                if (var == 'uu'):
                    var_s = DALES_uu_s2d
                elif (var == 'vv'):
                    var_s = DALES_vv_s2d
                elif (var == 'ww'):
                    var_s = DALES_ww_s2d
                elif (var == 'tt'):
                    var_s = DALES_tt_s2d
                elif (var == 'qq'):
                    fac = 1.e6
                    var_s = fac*DALES_qq_s2d
                elif (var == 'uw'):
                    var_s = DALES_uw_s2d
                elif (var == 'wt'):
                    var_s = DALES_wt_s2d
                elif (var == 'wq'):
                    fac = 1.e3
                    var_s = fac*DALES_wq_s2d

                var_x = DALES_xk_a
                var_z = 'zu_zi'
                facx  = DALES_PBLH

                # ---- interpolate spectra to z/zi grid

                da_int = np.array( [[np.interp(zwi,DALES_2dvar[var_z][i],var_s[i,:,j]) 
                                   for j in range(DALES_ncx)] for i in range(DALES_nt)] )

#               da_int = np.array( [[var_s[i,:,j] for j in range(DALES_ncx)] for i in range(DALES_nt)] )

                # ---- loop over heights to plot

#               xk_cut = int(2./3.*DALES_ncx) 
                xk_cut = DALES_ncx 

                for j in range(len(hgt2plot)):

                    # ---- time average spectra at current z/zi height

                    da_dales = rollavg_pandas(da_int[:,:,hgt_ind[j]], num)  # centered time average at this height

                    # ---- collect data at this height for all desired times

                    for i in range(len(time2plot)):

                        var_a = [facx[DALES_time_ind[i]]*var_x[DALES_time_ind[i],j] for j in range(1,xk_cut)]
#                       var_b = [var_x[DALES_time_ind[i],j]*da_dales[DALES_time_ind[i],j] for j in range(1,xk_cut)]
                        var_b = da_dales[DALES_time_ind[i],1:xk_cut]
                       
                        k = j*(len(time2plot))+i
                        da.append((k, var_a, var_b, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'CM1':     # --- CM1
    
                clabel = 'CM1'
                color = 'magenta'
#               color = 'dodgerblue'
                linestyle = 'solid'

                if (var == 'uu'):
                    var_s = CM1_uu_s2d
                elif (var == 'vv'):
                    var_s = CM1_vv_s2d
                elif (var == 'ww'):
                    var_s = CM1_ww_s2d
                elif (var == 'tt'):
                    var_s = CM1_tt_s2d
                elif (var == 'qq'):
                    fac = 1.e6
                    var_s = fac*CM1_qq_s2d
                elif (var == 'uw'):
                    var_s = CM1_uw_s2d
                elif (var == 'wt'):
                    var_s = CM1_wt_s2d
                elif (var == 'wq'):
                    fac = 1.e3
                    var_s = fac*CM1_wq_s2d

                var_x = CM1_xk_a
                var_z = 'zu_zi'
                facx  = CM1_PBLH

                # ---- interpolate spectra to z/zi grid

                da_int = np.array( [[np.interp(zwi,CM1_2dvar[var_z][i],var_s[i,:,j]) 
                                   for j in range(CM1_ncx)] for i in range(CM1_nt)] )

#               da_int = np.array( [[var_s[i,:,j] for j in range(CM1_ncx)] for i in range(CM1_nt)] )

                # ---- loop over heights to plot

#               xk_cut = int(2./3.*CM1_ncx)
                xk_cut = CM1_ncx 

                for j in range(len(hgt2plot)):

                    # ---- time average spectra at current z/zi height

                    da_cm1 = rollavg_pandas(da_int[:,:,hgt_ind[j]], num)  # centered time average at this height

                    # ---- collect data at this height for all desired times

                    for i in range(len(time2plot)):

                        var_a = [facx[CM1_time_ind[i]]*var_x[CM1_time_ind[i],j] for j in range(1,xk_cut)]
#                       var_b = [var_x[CM1_time_ind[i],j]*da_cm1[CM1_time_ind[i],j] for j in range(1,xk_cut)]
                        var_b = da_cm1[CM1_time_ind[i],1:xk_cut]
                       
                        k = j*(len(time2plot))+i
                        da.append((k, var_a, var_b, color, clabel, linestyle))  # add data to list
    

            elif data2plot[id] == 'NCAR':    # --- NCARLES
    
                clabel = 'NCAR-LES'
                color = 'orange'
                linestyle = 'solid'
    
                if (var == 'uu'):
                    var_s = NCARLES_uu_s2d
                elif (var == 'vv'):
                    var_s = NCARLES_vv_s2d
                elif (var == 'ww'):
                    var_s = NCARLES_ww_s2d
                elif (var == 'tt'):
                    var_s = NCARLES_tt_s2d
                elif (var == 'qq'):
                    fac = 1.e6
                    var_s = fac*NCARLES_qq_s2d
                elif (var == 'uw'):
                    var_s = NCARLES_uw_s2d
                elif (var == 'wt'):
                    var_s = NCARLES_wt_s2d
                elif (var == 'wq'):
                    fac = 1.e3
                    var_s = fac*NCARLES_wq_s2d

                var_x = NCARLES_xk_a
                var_z = 'zu_zi'
                facx  = NCARLES_PBLH

                # ---- interpolate spectra to z/zi grid

                da_int = np.array( [[np.interp(zwi,NCARLES_2dvar[var_z][i],var_s[i,:,j]) 
                                   for j in range(NCARLES_ncx)] for i in range(NCARLES_nt)] )

#               da_int = np.array( [[var_s[i,:,j] for j in range(NCARLES_ncx)] for i in range(NCARLES_nt)] )

                # ---- loop over heights to plot

                xk_cut = int(2./3.*NCARLES_ncx)

                for j in range(len(hgt2plot)):

                    # ---- time average spectra at current z/zi height

                    da_ncar = rollavg_pandas(da_int[:,:,hgt_ind[j]], num)  # centered time average at this height

                    # ---- collect data at this height for all desired times

                    for i in range(len(time2plot)):

                        var_a = [facx[NCARLES_time_ind[i]]*var_x[NCARLES_time_ind[i],j] for j in range(1,xk_cut)]
#                       var_b = [var_x[NCARLES_time_ind[i],j]*da_ncar[NCARLES_time_ind[i],j] for j in range(1,xk_cut)]
                        var_b = da_ncar[NCARLES_time_ind[i],1:xk_cut]
                       
                        k = j*(len(time2plot))+i
                        da.append((k, var_a, var_b, color, clabel, linestyle))  # add data to list

            elif data2plot[id] == 'OBS':    # --- Observations
    
                if var == 'u':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_u[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_u.transpose(), clabel))
    
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
    
                elif var == 'uw':
    
                    clabel = 'WindCube'
                    facz = 1.e-3  # convert [m] -> [km]
    
                    for i in range(len(time2plot)):
                        do.append((i,lidar_uw[LIDAR_time_ind[i]], lidar_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

#               elif var == 'wt':
#   
#                   clabel = 'C-130'
#                   facz = 1.e-3  # convert [m] -> [km]
#   
#                   for i in range(len(time2plot)):
#                       do.append((i,c130_wt, c130_alt*facz, clabel))
#   
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

#               elif var == 'wq':
#   
#                   clabel = 'C-130'
#                   facz = 1.e-3  # convert [m] -> [km]
#   
#                   for i in range(len(time2plot)):
#                       do.append((i,c130_wq, c130_alt*facz, clabel))
    
#                   dc.append((LIDAR_time_hr, lidar_alt*facz, lidar_uw.transpose(), clabel))

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

        # ---- find variable max/min

        if ('OBS' in data2plot):   # currently skipping OBS to set contour intervals
            xx = len(da) - 1
        elif ('SCM' == 'True'):
            xx = 1
        else:
            xx = len(da)

       # ---- max/min for x-axis

        amin = +999999.
        amax = -999999.
        vamin = amin
        vamax = amax

        for i in range(xx):
            n = da[i]
            amin = np.min( n[1][:] )
            amax = np.max( n[1][:] )
            if amin < vamin:
                vamin = amin
            if amax > vamax:
                vamax = amax

        # ---- max/min for y-axis

        bmin = +999999.
        bmax = -999999.
        vbmin = bmin
        vbmax = bmax
        for i in range(xx):
            n = da[i]
            bmin = np.min( n[2][:] )
            bmax = np.max( n[2][:] )
            if bmin < vbmin:
                vbmin = bmin
            if bmax > vbmax:
                vbmax = bmax

        # ---- setup axis ticks and titles for the current variable
    
        if (var == 'uu'):
    
            y_title[0] = r"$E_u$~~[m$^{2}$ s$^{-2}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 5.e-7
                ymax[i] = 5.e-1

        elif (var == 'vv'):
    
            y_title[0] = r"$E_v$~~[m$^{2}$ s$^{-2}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 5.e-7
                ymax[i] = 5.e-1

        elif (var == 'ww'):
    
            y_title[0] = r"$E_w$~~[m$^{2}$ s$^{-2}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 5.e-7
                ymax[i] = 5.e-1

        elif (var == 'tt'):
    
            y_title[0] = r"$E_{\theta}$~~[K$^{2}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 1.e-8
                ymax[i] = 5.e-2

        elif (var == 'qq'):
    
            y_title[0] = r"$E_{q}$~~[(g kg$^{-1}$)$^2$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 5.e-8
                ymax[i] = 1.

        elif (var == 'uw'):
    
            y_title[0] = r"$Co_{uw}$~~[m$^{2}$ s$^{-2}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = -0.025
                ymax[i] =  0.02

        elif (var == 'wt'):
    
            y_title[0] = r"$Co_{w\theta}$~~[m K s$^{-1}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 1.e-8
                ymax[i] = 1.e-2

        elif (var == 'wq'):
    
            y_title[0] = r"$Co_{wq}$~~[m s$^{-1}$\,\, g kg$^{-1}$]"
    
            for i in range(len(time2plot)):
                ymin[i] = 5.e-8
                ymax[i] = 1.e-1

        # ---- x-axis is the same for all spectra plots
    
        for i in range(len(time2plot)):
            x_title[i] = r'$k_h \, z_i$'
            xmin[i] = 0.5
            xmax[i] = 500

        # ---- collect those settings for more general use
    
        ticks_titles = {'xmin': xmin, 'xmax': xmax, 'x_title': x_title,
                        'ymin': ymin, 'ymax': ymax, 'y_title': y_title}

        # ---- build plot

        axp = [None] * len(time2plot) * len(hgt2plot)

        fig = plt.figure(figsize=(12, 2.8*len(hgt2plot)))

        gp = plt.GridSpec(len(hgt2plot), len(time2plot))
        gp.update(left=0.09, right=0.91, top=0.97, bottom=0.09, wspace=0.18, hspace=0.18)

        for j in range(len(hgt2plot)):
            for i in range(len(time2plot)):
                k = j*(len(time2plot))+i
                axp[k] = fig.add_subplot(gp[j,i])           # configure one line plot per 'i'
    
        # ---- create the plots 
        
        plot_profile_2var_1x3(da, ticks_titles)    # create line plots
        
        # ---- export file

        if (single_file == 0):
            if (output_file_type == 0):
                plt.savefig("../plots/met_spectra."+var+".pdf")
            elif (output_file_type == 1):
                plt.savefig("../plots/png/met_spectra."+var+".png", dpi=2048, bbox_inches='tight')
        else:
            pdf.savefig( fig )
        plt.close( fig )

if (single_file == 1):
    pdf.close()
