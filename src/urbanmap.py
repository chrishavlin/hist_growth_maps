""" 
ubanmap.py
a module for the visualization of the Historical Urban Population Growth Data dataset.

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
# import required modules
from mpl_toolkits.basemap import Basemap,shiftgrid
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

def load_cities(data_dir,city_file): 
    """ loads population, lat/lon and time arrays for historical 
        city data. """ 

    print 'Loading database: ' + city_file[:]
#   load city files
    flnm=data_dir+city_file
    fle = open(flnm, 'r') # open the file for reading
    csv_ob=csv.reader(fle,skipinitialspace=True)  
    
#   count number of lines
    indx=0
    #for line in fle:
    for row in csv_ob:
        indx=indx+1
    indx = indx-1
    fle.seek(0) # return to start of file
    
#   get header line 
    header = fle.next()
    header = header.rstrip()
    header = header.split(',')
    
#   build the Time array
    nt = len(header)
    Time_string=header[6:nt]
    nt = len(Time_string)
    Time = np.zeros((nt,1))
    
#   convert BC/AD to years before present 
    for it in range(0,nt):
        ct = Time_string[it]
        ct = ct.split('_')
	Time[it]=bc_ad_ce_to_ybp(ct[1],ct[0])
    
#   build population matrix and lat/lon arrays
#   each row is a city, each column is the known population at 
#   the Time array
    PopuL=np.zeros((indx,nt))
    city_lon=np.zeros((indx,1))
    city_lat=np.zeros((indx,1))
    indx=0
    for row in csv_ob:
#       read in current line
        line = row
        line = [item.replace('\xa0',' ') for item in line]
	     # deal with a couple of troublesome spaces in the database

#       pull out lat/lon    
        city_lat[indx] = float(line[3])
        city_lon[indx] = float(line[4])

#       pull out population	
	pop = line[6:nt]
    
#       loop over times, store population in PopuL matrix
        for it in range(0,nt,1):
              try:
                  PopuL[indx,it]=float(pop[it]) 
              except:
                  PopuL[indx,it]=0.0
    
        indx=indx+1
   
    fle.close()
    
    return (Time,PopuL,city_lat,city_lon)

def bc_ad_ce_to_ybp(yr,bc_ad_ce): 
    """ converts BC, AD, BCE or CE to years before present (ypb) """
    ref_yr=1950 # present defined as 1950
    if bc_ad_ce=='BC' or bc_ad_ce=='BCE':
        yr_before_present=ref_yr+float(yr)
    elif bc_ad_ce=='AD' or bc_ad_ce=='CE':
        yr_before_present=ref_yr-float(yr)

    return yr_before_present

def ybp_to_ce(yr): 
    """ converts years before present (ypb) to BCE or CE"""
    ref_yr=1950
    yr_ce = yr - ref_yr
    if yr_ce > 0: # then BCE
       year_ce=[str(yr_ce) + ',BCE']
    else: #then CE
       year_ce=[str(abs(yr_ce)) + ',CE']

    return year_ce

def base_plot(lon_start=180): 
    """ input:
        lon_start    westernmost longitude for map orientation   
                     center of map will be lon_start+180
    """
    
#   define lat/lon grid to draw
    lat_grid=np.arange(-60.,90.,30.)
    lon_grid=np.arange(lon_start,lon_start+360.,60.)

#   select projection type 
    project_type='robin'
   
#   flag for plotting topographic background   
    use_bg_topo=True

#   read in topo data (on a regular lat/lon grid) if 
#   we're using the background topo plot
    if use_bg_topo:
        map_path='../../../python_basemap_examples/'
        etopo=np.loadtxt(map_path+'etopo20data.gz')
        lons=np.loadtxt(map_path+'etopo20lons.gz')
        lats=np.loadtxt(map_path+'etopo20lats.gz')
        
    #   starting longitude needs to be on the lon grid 
    #   exactly, find closest value:
        lon0=lons[(np.abs(lons-lon_start)).argmin()]
        
    #   shift topo data to desired start location
        etopo,lons=shiftgrid(lon0,etopo,lons,start=True)
    #    confusing note: lon0 in shiftgrid is left-most value (or right-most)
    #                    while lon0 in Basemap is the center of the map!

    else:
        lon0=lon_start
        
#   calculate center longitude based on lon_start 
    center_lon=lon0+180.0

#   create basemap projection
    m = Basemap(projection=project_type,lon_0=center_lon)
    
    if use_bg_topo:
    #   make filled contour plot of topographic data.
        x, y = m(*np.meshgrid(lons, lats))
        cs = m.contourf(x,y,etopo,45,cmap=plt.cm.terrain)
    #        other good colormaps: coolwarm,seismic,hot
    
#   draw coastlines.
    m.drawcoastlines()
    
#   draw parallels and meridians.
#   labels=[L,R,T,B], if == 1 will label when it intersects that boundary
    m.drawparallels(lat_grid,labels=[1,0,0,0])
    m.drawmeridians(lon_grid,labels=[0,0,0,1])
    return m

def get_lon_lat_at_t(year_range,city_lon,city_lat,Time,PopuL):
    """ pulls out urban centers within time range and plots them on 
        the base topo map """

#   select lat/lon for cities with nonzero population in time_range
    ncit=len(PopuL[:,0]) # number of cities
    lons=np.copy(city_lon)
    lats=np.copy(city_lat)

#   convert year_range to years before present
    year_range=year_range.replace(" ", "")
    years=year_range.split(',')
    time_range=[0,0]
    time_range[0]=bc_ad_ce_to_ybp(years[0],years[1])
    time_range[1]=bc_ad_ce_to_ybp(years[2],years[3])

#   find lat and lon of cities with recorded populations in database
    for icit in range(0,ncit):
        pop=PopuL[icit,:] # current population
        pop_t=Time[pop>0] # times with nonzero pops  	
        pop_t=pop_t[pop_t<=time_range[0]] # pops within time range
        pop_t=pop_t[pop_t>=time_range[1]]

	if pop_t.size == 0: # flag for removal 
	   lons[icit]=999. 
	   lats[icit]=999.

#   remove zero pop cities for time range
    lons=lons[lons!=999]
    lats=lats[lats!=999]
    return lons,lats,time_range

def city_plot(lons,lats,m,plot_type,time_range,Time):

    if lons.size != 0: 
       if plot_type=='animation':
#         set current color based on where in time we are
          center_age=(time_range[0]+time_range[1])/2 
          minT = min(min(Time))
          maxT = max(max(Time))
          rat=(center_age-minT)/(maxT-minT)
          clr=(1-rat,0,rat)
#         set opacity based on time as well
          minalf=0.4
          alf= (1.-minalf) * rat + minalf
       else:
#         fixed color and opacity 
          clr=(1,0,0)
	  alf = 1.

#      put those points on the map
       x_1,y_1 = m(lons,lats)
       city_points=m.scatter(x_1,y_1,100,marker='o',color=clr,alpha=alf,edgecolors='k')

       titename=get_title(time_range,plot_type)
       plt.title(titename)

       if plot_type=='singleframe':
          print 'Plotting complete, close figure to end program'
    else: 
       titename=get_title(time_range,plot_type)
       plt.title(titename)
       city_points=False

    return city_points

def get_title(time_range,plot_type):
    """ generates title depending on plot_type """
    if plot_type=='animation':
       center_age=(time_range[0]+time_range[1])/2 
       dev =abs(time_range[1]-time_range[0])/2
       
       yr=ybp_to_ce(int(center_age))
       titename= yr[0] + '+/-' + str(int(dev)) + ' yrs'
    else:
       yr=ybp_to_ce(int(time_range[0]))[0].split(',')
       yr2 = ybp_to_ce(int(time_range[1]))[0].split(',')
       titename=yr[0] + ' ' + yr[1] + ' to ' + yr2[0] + ' ' + yr2[1]

    return titename

def urban_animate_py_driver(data_dir,city_file,n_time_steps,frm_spc,show_or_save,fpsout):
    """ pythonic animation driver """

    def setup_urban_animate(nt):
        """sets the time range to animate, picks animation windows at each point"""
        Time1= int(min(min(Time))) # min time bpy
        Time0= int(max(max(Time))) # max time bpy
        AnimatedTimeRange=np.linspace(Time0,Time1,nt)#range(Time0,Time1,step) 
        step = abs(AnimatedTimeRange[1]-AnimatedTimeRange[0])
        yr_window=int(step)
	return AnimatedTimeRange,yr_window

    def urban_animate_init():
        """ animation initialization function """
        m.scatter([],[])

    def urban_animate_py(i):
        """ the animated function """
#       select current step
        yr_current=int(AnimatedTimeRange[i])
#       generate proper string-input for year span
        yr_start= ybp_to_ce(yr_current+yr_window/2)
        yr_end= ybp_to_ce(yr_current-yr_window/2)
        yr_span=yr_start[0] + ',' + yr_end[0]
#       plot current step
        lons,lats,time_range=get_lon_lat_at_t(yr_span,city_lon,city_lat,Time,PopuL)
        city_plot(lons,lats,m,'animation',time_range,Time)

#   read the data    
    Time,PopuL,city_lat,city_lon=load_cities(data_dir,city_file) 

#   calculate time range 
    AnimatedTimeRange,yr_window=setup_urban_animate(n_time_steps)

#   the base topo map    
    plt.figure(facecolor=(1,1,1),figsize=(8,4.5))
    m=base_plot()

#   annotate with references
    add_annotations()

#   time to animate it!
    print 'Generation animation'
    anim = animation.FuncAnimation(plt.gcf(), urban_animate_py,init_func=urban_animate_init(), 
                                   frames=n_time_steps,interval=frm_spc,repeat=False)

#   save or show the animation				   
    if show_or_save=='save':
       print 'Saving animation'
       anim.save('plot_animation.mp4', fps=fpsout),
    else: 
       print 'Animation playback: close window to continue'
       plt.show()
    print 'Animation complete!'


def add_annotations():
    str_ref='Historical Urban Population Growth Data: Reba et al., 2016, http://urban.yale.edu/data'
    plt.annotate(str_ref, xy=(-0.1, 1.15), xycoords='axes fraction')
    str_ref='Visualization: C. Havlin, https://chrishavlin.wordpress.com/blog/'
    plt.annotate(str_ref, xy=(-0.1, -0.15), xycoords='axes fraction')

if __name__ == '__main__':
    """ default case plots the full time span of chandler """

#   select time range
    start_end_yr='5000,BCE,2016,CE'

#   select data set
    data_dir='../data_refs/'
    city_file='chandlerV2.csv'
    
#   get the city information    
    Time,PopuL,city_lat,city_lon=load_cities(data_dir,city_file) 

#   get lon/lat of cities in time span    
    lons,lats,time_range=get_lon_lat_at_t(start_end_yr,city_lon,city_lat,Time,PopuL)

#   create base plot and map object
    plt.figure(facecolor=(1,1,1))
    m = base_plot() 

#   add annotations    
    add_annotations()

#   add a city info
    current_cities = city_plot(lons,lats,m,'singleframe',time_range,Time)
    
#   display the plot    
    plt.show()
