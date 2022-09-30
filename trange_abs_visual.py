# libraries needed for abs graph visualization
import pytplot
import os
import numpy as np
from pytplot import tplot
from scipy.io import readsav
from astropy.time import Time

# Single function that takes user's start time, stop time and folder of datasets as arguments
def time_visual(user_start, user_end, folder):

# Empty NumPy arrays outside of loop that are defined for later use
    mega_x_data = np.array([])
    mega_y_data = np.array([])
    nouvelle_x = np.array([])
    nouvelle_y = np.array([])

# large for loop which cycles through each file inside "folder"
    for file in os.listdir(folder):
        rock = os.path.join(folder, file)

        # Opening the abs script file (binary to readable text)
        sav_data = readsav(rock)
        a = sav_data["fomstr"]

        start_times = a["START"][0] 
        stop_times = a["STOP"][0] 
        timestamp_values = a["TIMESTAMPS"][0] 
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

        # Combines all the data across all files into two separate arrays, each for x and y
        mega_x_data = np.concatenate((mega_x_data, up_unix_x_data))
        mega_y_data = np.concatenate((mega_y_data, up_new_y_data))

    # Converts the user's start and stop values ot the "UTC" format
    change1 = (Time(user_start, scale='utc')).unix
    change2 = (Time(user_end, scale='utc')).unix

    # Narrows down to the required data needed based on start/stop time constraints
    for k in mega_x_data:
        if change1 <= k <= change2:
            nouvelle_x = np.append(nouvelle_x, k)
            value = np.where(mega_x_data == k)[0][0]
            nouvelle_y = np.append(nouvelle_y, mega_y_data[value])
            
    # Corrects small error by moving first element of y_data to the end of teh array
    nouvelle_y = np.roll(nouvelle_y, -1)

    # Creates a tplot variable for data
    pytplot.store_data('FOM', data={'x':nouvelle_x, 'y':nouvelle_y})
    time, data = pytplot.get_data('FOM')

    # Prints the x_data & y_data arrays
    print(time)
    print(data)

    # Displays the tplot graph:
    return tplot(["FOM"])

