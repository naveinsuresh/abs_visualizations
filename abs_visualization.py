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
    a = sav_data["fomstr"]

    start_times = a["START"][0] 
    stop_times = a["STOP"][0] 
    print(start_times)
    print(stop_times)
    timestamp_values = a["TIMESTAMPS"][0] 
    print(timestamp_values)
    fom_values = a["FOM"][0] 

    # Merges the the start_time and stop_values array into a single sorted array
    alpha = np.concatenate((start_times, stop_times))
    alpha.sort()

    # Creates a new 1 x 18 array which contains a series of "start and stop" timestamp_values
    beta = np.array([])
    for i in alpha:
        gamma = np.array([timestamp_values[i]])
        beta = np.append(beta, gamma)

    # Adds the required 10 second increment to EVERY OTHER timestamp_value 
    # Assigns timestamp_values to x_data variable
    beta[::2] += 10
    x_data = beta
  
    # Assigns fom_values to y_data
    y_data = fom_values

    # Performs the conversion from TAI to UNIX/UTC
    tai_format = 'gps' # use unix_tai or gps?

    t1 = Time('1958-01-01 00:00:00', scale='utc')
    ut_t2 = Time('1970-01-01 00:00:08', scale='utc') # unix_tai'
    g_t2 = Time('1980-01-06 00:00:19', scale='utc') # gps
    if tai_format == 'unix_tai':
        delta = t1 - ut_t2
    else:
        delta = t1 - g_t2

    # Creates a new array of converted unix values for the x_data
    unix_x_data = np.array([])
    for tata in x_data:
        converted = (Time(str(tata), scale='tai', format=tai_format)+delta).unix
        manga = np.array([converted])
        unix_x_data = np.append(unix_x_data, manga)

    # Previous unix_x_data is repeated 2x
    up_unix_x_data = np.repeat(unix_x_data, 2) # x-axis

    # Previous y_data array conntent is repeated 2x 
    new_y_data = np.repeat(y_data, 2) 
    
    # inserts zeros in specific places to create "bar" type display
    i = 0
    while i < len(new_y_data):
        new_y_data = np.insert(new_y_data, i, 0)
        i += 3
    
    i = 4
    while i < len(new_y_data):
        new_y_data = np.insert(new_y_data, i, 0)
        i += 4

    up_new_y_data = np.append(new_y_data, 0) # y-axis

    # Creates a tplot variable for data
    pytplot.store_data('FOM', data={'x':up_unix_x_data, 'y':up_new_y_data})
    time, data = pytplot.get_data('FOM')

    # prints the x_data & y_data arrays
    print(time)
    print(data)

    # Displays the tplot graph:
    return tplot(['FOM'])



# Steps to display data given a trange
# Write a for loop which takes loops through each file in the directory and concatenates the arrays presented together