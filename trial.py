# libraries needed for abs graph visualization
import pytplot
import numpy as np
from pytplot import tplot
from astropy.time import Time
import scipy.io.idl

# Single function that takes 'file_path' as an argument
def visual(file_path):

    # Opening the abs script 30file (binary to readable text)
    sav_data = scipy.io.idl.readsav(file_path)
    sav_data = scipy.io.idl.writesav()
    print(sav_data)
    a = sav_data["fomstr"]  # opens "megakey"

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


# File of Interest:
# 2022/abs_selections_2022-09-06-00-46-59.sav

