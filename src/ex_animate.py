""" 
ex_animate.py

animates urban population growth at user specified intervals

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

# select data set
data_dir='../data_refs/'
city_file='chandlerV2.csv'

# data sets in Reba et al:
#    city_file='chandlerV2.csv'
#    city_file='modelskiAncientV2.csv'
#    city_file='modelskiModernV2.csv'
    
n_time_steps=50 # number of time steps to break up time range into
output='show' # 'save' to just save a .mp4 file, 'show' to show the animation without saving
framespace=250 # frame spacing in playback [ms]
fps_out=2 # frames per second if saving the animation

# now animate it!
um.urban_animate_py_driver(data_dir,city_file,n_time_steps,framespace,output,fps_out)


