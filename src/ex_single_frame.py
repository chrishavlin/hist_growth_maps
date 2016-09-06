""" 
ex_single_frame.py

plots a single frame with urban centers within a specified time span (time_span)

Copyright (C) 2016  Chris Havlin, <https://chrishavlin.wordpress.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
The database is NOT distributed with the code here. Download it then set location of 
data base with data_dir variable. 

Data source:

  Reba, Meredith, Femke Reitsma, and Karen C. Seto. "Spatializing 6,000 
        years of global urbanization from 3700 BC to AD 2000." 
        Scientific data 3 (2016).

  <http://urban.yale.edu/data> "Historical Urban Population Growth Data"
"""

import urbanmap as um
import matplotlib.pyplot as plt

# select time range
time_span='500,BCE,50,CE'
       # comma separated string noting desired time span. The age descriptor can 
       # be BC, BCE, AD or CE.

# select data set
data_dir='../data_refs/'
city_file='modelskiAncientV2.csv'

# data sets in Reba et al:
#    city_file='chandlerV2.csv'
#    city_file='modelskiAncientV2.csv'
#    city_file='modelskiModernV2.csv'
    
# import data set 
(Time,PopuL,city_lat,city_lon)=um.load_cities(data_dir,city_file) 

# get lon/lat of cities in time span    
lons,lats,time_range=um.get_lon_lat_at_t(time_span,city_lon,city_lat,Time,PopuL)

# plot it
plt.figure(facecolor=(1,1,1))
m = um.base_plot() # create base plot and map object
um.add_annotations() # adds references
um.city_plot(lons,lats,m,'singleframe',time_range,Time) # plot points
plt.show() # and display the plot

# use plt.savefig to save instead of display
