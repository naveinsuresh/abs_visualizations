# libraries needed for abs graph visualization
import pytplot
import numpy as np
from pytplot import tplot
from scipy.io import readsav
from astropy.time import Time

# Single function that takes 'file_path' as an argument
def visual(file_path):

    # Opening the abs script 30file (binary to readable text)
    sav_data = readsav(file_path)
    print(sav_data)
    a = sav_data["fomstr"] # opens "megakey"

    start_times = a["START"][0] 
    stop_times = a["STOP"][0] 
    print(start_times)
    print(stop_times)
    timestamp_values = a["TIMESTAMPS"][0] 
    print(timestamp_values)
    fom_values = a["FOM"][0] 
    print(fom_values)
    seg_length = a["SEGLENGTHS"][0]
    print(seg_length)
    num_segs = a["NSEGS"]
    print(num_segs)