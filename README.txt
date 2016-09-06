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

DESCRIPTION 

The python code here is module for plotting historical urbanization data sets. 
It was tailored to read in the freely availabe data set of Reba et al. (2016, 
full citation below). The data base is NOT distributed with the code here.

Data set source:

  Reba, Meredith, Femke Reitsma, and Karen C. Seto. "Spatializing 6,000 
        years of global urbanization from 3700 BC to AD 2000." 
        Scientific data 3 (2016).

  http://urban.yale.edu/data "Historical Urban Population Growth Data"     

The author (C. Havlin) of this python code has no affiliation with the database 
authors (Reba et al.). Furthermore, the author has not undertaken any significant 
benchmarking to check that the code accurately reads in or correctly plots the 
database points. So check carefully before using this code for presentations or 
publications. 

REQUIREMENTS

required python modules: matplotlib, mpl_toolkits (basemap), numpy, csv 
tested only in python 2.7

mpl_toolkits data: the plot uses topography data that comes with the mpl_toolkit. 
after installing the toolkit, the map_path variable in urbanmap.baseplot has to 
be set to the location of the mpl_toolkit sample folder containing etopo20data.gz,
etopo20lons.gz and etopo20lats.gz. Or, references to the topo data can be commented
(see step 2b of USAGE, below).

USAGE

1. download the data set of Reba et al. http://urban.yale.edu/data
   put the .csv files into historical_urban_growth_mapping/data_refs/
   or put them anywhere you like and modofiy the data_dir variable
   in the source code. 

2. modify source code in two locations

   2a. set data_dir in ex_single_frame.py, ex_animate.py and urbanmap.py
       following step 1. 

   2b. the background topographic map uses topographic data from 
       the basemap demos. The three files: etopo20data.gz, etopo20lats.gz,
       and etopo20lons.gz are found in basemap-1.0.7/examples/ when 
       you download the mpl-toolkits basemap. If you already have basemap 
       installed, download the source again from 

       http://matplotlib.org/basemap/users/download.html

       then copy those files somewhere convenient and set then map_path
       variable in urbanmap.py to the location of those files. 

       alternatively, set use_bg_topo=FALSE in urbanmap.py

       (open up urbanmap.py and do a search to find map_path and use_bg_topo)

3. cd to the src folder then from the command line:

      $ python FILENAME.py

What you choose for FILENAME.py will change behavior: 

      urbanmap.py  create a default plot of all urban locations for all 
                   times in the database

      ex_single_frame.py create a plot of urban locations for a
                   specified time range

      ex_animate.py creates an animation of urban locations through time
                    at specified interval


See https://chrishavlin.wordpress.com/blog/ for examples of output.
