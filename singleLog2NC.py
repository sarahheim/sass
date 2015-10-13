
#SET python header line
# Author Sarah Heim
# Date create: May 2015
#
# Description: Test various NetCDF options to see affect on NC size.

import os, time, pandas
import numpy as np
from netCDF4 import Dataset
import sass

start = time.time()
#logsdir = r'/data/InSitu/SASS/data/'
#ncpath = '/home/scheim/SASS-netcdf/test/'
ncpath = '/data/InSitu/SASS/tmp/'

#CREATE NETCDF4 FILE STRUCTURE
def createNCshell(ncfile, ip):
    kwargs = {"zlib": True}
    # Create Dimensions
    time_dim = ncfile.createDimension('time', None) # unlimited axis (can be appended to).

    # Should units be CF, V spelt out???
    time_var = ncfile.createVariable('time', np.int32, ('time'), **kwargs) # int64? Gives error
#     time_var.setncattr({'standard_name':'time', 'long_name': 'time', 'units':'seconds since 1970-01-01 00:00:00 UTC'})
    time_var.standard_name = 'time'
    time_var.units = 'seconds since 1970-01-01 00:00:00 UTC'
    time_var.long_name = 'time'
    #time_var.calendar = 'gregorian' #use??
    sst = ncfile.createVariable('sst', 'f4', ('time'), **kwargs)
    sst.standard_name = 'sea_water_temperature'
    sst.long_name= 'sea water temperature'
    sst.units = 'celsius'
    con = ncfile.createVariable('conductivity', 'f4', ('time'), **kwargs)
    con.standard_name = 'sea_water_electrical_conductivity'
    con.long_name= 'sea water electrical conductivity'
    con.units = 'S/m'
    pres = ncfile.createVariable('pressure', 'f4', ('time'), **kwargs)
    pres.standard_name = 'sea_water_pressure'
    pres.long_name= 'sea water pressure'
    pres.units = 'dbar'
    a1= ncfile.createVariable('aux1', 'f4', ('time'), **kwargs)
    a1.long_name= 'Auxiliary 1' # Use Standard name for 1,3,4???
    a1.units = 'V'
    a3 = ncfile.createVariable('aux3', 'f4', ('time'), **kwargs)
    a3.long_name= 'Auxiliary 3'
    a3.units = 'V'
    chl = ncfile.createVariable('chlorophyll', 'f4', ('time'), **kwargs)
    chl.standard_name = 'mass_concentration_of_chlorophyll_a_in_sea_water'
    chl.long_name= 'chlorophyll'
    chl.units = 'V' #which CF name??? Wrong Units???
    a4 = ncfile.createVariable('aux4', 'f4', ('time'), **kwargs)
    a4.long_name= 'Auxiliary 4'
    a4.units = 'V'
    sal = ncfile.createVariable('salinity', 'f4', ('time'), **kwargs)
    sal.standard_name = 'sea_water_salinity'
    sal.long_name= 'sea water salinity'
    sal.units = 'PSU'
    sig = ncfile.createVariable('sigmat', 'f4', ('time'), **kwargs)
    sig.standard_name = 'sea_water_density'
    sig.long_name= 'sea water density'
    sig.units = 'kg/m^3'
    dV = ncfile.createVariable('diagnosticVoltage', 'f4', ('time'), **kwargs)
    dV.long_name= 'diagnostic voltage' #NO standard name???
    dV.units = 'V'
    cDr = ncfile.createVariable('currentDraw', 'f4', ('time'), **kwargs)
    cDr.long_name= 'current draw' #NO standard name???
    cDr.units = 'mA'

    ncfile.Metadata_Conventions = 'Unidata Dataset Discovery v1.0'
    ncfile.Conventions = 'CF-1.6'
    ncfile.summary = 'Automated shore station with a suite of sensors that are attached to piers'

    return ncfile

#mnpath = os.path.join(sass.logsdir, mn)
filename = os.path.join(sass.logsdir, '2015-07', 'data-20150701.dat')
#print sass.ncpath
sass.ncpath = ncpath
print sass.ncpath
print filename
sass.log2nc(filename)
print "DONE! Appended a single log file", time.time()-start

#Append a few files
#sass.log2nc(os.path.join(sass.logsdir, '2015-07', 'data-20150702.dat'))
#sass.log2nc(os.path.join(sass.logsdir, '2015-07', 'data-20150703.dat'))
#sass.log2nc(os.path.join(sass.logsdir, '2015-07', 'data-20150704.dat'))
#print "DONE! Appended a few log files", time.time()-start

