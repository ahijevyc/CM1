# ---- set base directory for all data

path_base = "/Users/patton/research/les/reinvest/sas/anl/data"
#path_base = "/glade/p/mmm/nmmm0058/data/sas"

# ---- define some functions

from IPython.display import display_html
def restartkernel() :
    display_html("<script>Jupyter.notebook.kernel.restart()</script>",raw=True)

def extract_ict2(parameter2extract, ict_path_file):
    # --------------
    # Read the  file
    # --------------
    f_ict        = open(ict_path_file, "r")
    ict_contents = f_ict.readlines()
    f_ict.close()
    # ---------------------------------------------------------------
    # Find the header: 
    # for ict format, line index of header is given in the first line
    # ---------------------------------------------------------------
    header_line_ind = -1+int(ict_contents[0].split(',')[0])
    FileHeaderKeyword = ict_contents[header_line_ind]
    FileHeaderKeyword = FileHeaderKeyword.replace(' ,', ',').replace(', ', ',')
    for i in range(len(ict_contents)):
        # if (ict_contents[i].find(FileHeaderKeyword) != -1): 
        ict_contents_squeeze = ict_contents[i].replace(' ,', ',').replace(', ', ',')
        # print(ict_contents_squeeze)
        if (ict_contents_squeeze.find(FileHeaderKeyword) != -1): 
            ict_header = ict_contents_squeeze
            ict_header_lineind = i
            break
    ict_contents = ict_contents[ict_header_lineind+1:]    # Chop off header
    ict_header = ict_header.split(',')                    # Chop header into pieces
    parameter_index = ict_header.index(parameter2extract) # Get the col index for the parameter
    # -------------------------
    # Now extract the parameter
    # -------------------------
    parameter_temp = ict_contents
    for i in range(len(ict_contents)): parameter_temp[i] = float(ict_contents[i].split(',')[parameter_index])
    return parameter_temp
    del parameter_temp
    del ict_contents


def extract_ict2_basedate(ict_path_file):
    # --------------
    # Read the  file
    # --------------
    f_ict        = open(ict_path_file, "r")
    ict_contents = f_ict.readlines()
    f_ict.close()
    # ------------------
    # Find the base date 
    # ------------------
    basedate_lineind = 6
    basedate = ict_contents[basedate_lineind]
    basedate = basedate.replace(' ,', ',').replace(', ', ',')
    basedate_out = basedate.split(',')[0] + '-' + basedate.split(',')[1] + '-' + basedate.split(',')[2]
    return basedate_out
    del basedate_out, basedate
    del ict_contents


def hourly_stats(hour_bounds, raw_hour_of_day, raw_param, raw_percentile):
    stat_out = []
    for n in range(-1+len(hour_bounds)):
        raw_param_temp = raw_param.copy()
        raw_param_temp = np.where((raw_hour_of_day>=hour_bounds[n]) & (raw_hour_of_day<hour_bounds[n+1]), raw_param_temp, np.nan)
        stat_out.append(np.nanpercentile(raw_param_temp, raw_percentile))
    return stat_out

def vertical_stats(height_bounds, raw_height, raw_param, raw_percentile):
    stat_out = []
    for n in range(-1+len(height_bounds)):
        raw_param_temp = raw_param.copy()
        raw_param_temp = np.where((raw_height>=height_bounds[n]) & (raw_height<height_bounds[n+1]), raw_param_temp, np.nan)
        stat_out.append(np.nanpercentile(raw_param_temp, raw_percentile))
    return stat_out
    del stat_out, raw_param_temp

def rollavg_pandas(a,n):
    # function to calculate running average
    # See: https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-numpy-scipy
    return pd.DataFrame(a).rolling(n, center=True, min_periods=1).mean().to_numpy()

def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier

def round_dn(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)

def down_sample(x, f=7):
    # pad to a multiple of f, so we can reshape
    # use nan for padding, so we needn't worry about denominator in
    # last chunk
    xp = np.r_[x, nan + np.zeros((-len(x) % f,))]
    # reshape, so each chunk gets its own row, and then take mean
    return np.nanmean(xp.reshape(-1, f), axis=-1)

def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape, dtype=data.dtype)
    out[mask] = np.concatenate(data)
    return out
