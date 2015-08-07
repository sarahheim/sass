

#SET python header line
# Author Sarah Heim
# Date create: May 2015
#
# Description: Library: Various variable and functions used in:
# allLogsToNCs.py
# appendLatestToNC.py
#
# Plans:
#SETUP, GLOBAL VARIABLES
import os, time, pandas
import numpy as np
from netCDF4 import Dataset

logsdir = r'/data/InSitu/SASS/data/'
#ncpath = '/home/scheim/SASS-netcdf/test/'
ncpath = '/data/InSitu/SASS/netcdfs/'

dateformat = "%Y-%m-%dT%H:%M:%SZ"
fnformat = "%Y-%m/data-%Y%m%d.dat"

staMeta = {'UCSB': {'loc':'UCSB', 'lat': 34.4107, 'lon': -119.6874, 'loc_name':'Stearns Pier', 
                        'url': 'http://msi.ucsb.edu/', 'depth': '2', 
                        'inst': 'Marine Science Institute at University of California, Santa Barbara'}, 
       'UCI': {'loc':'UCI', 'lat': 33.6073, 'lon': -117.9289, 'loc_name':'Newport Pier', 
                        'url': 'http://uci.edu/', 'depth': '2',
                        'inst': 'University of California, Irvine'},
       'UCLA': {'loc':'UCLA', 'lat': 34.0086, 'lon': -118.4986 , 'loc_name':'Santa Monica Pier', 
                        'url': 'http://environment.ucla.edu/', 'depth': '2',
                        'inst': 'Institute of the Environment at the University of California, Los Angeles'},
       'UCSD': {'loc':'UCSD', 'lat': 32.867, 'lon': -117.257, 'loc_name':'Scripps Pier', 
                        'url': 'https://sccoos.org/', 'depth': '5',
                        'inst': 'Southern California Coastal Ocean Observing System (SCCOOS) at Scripps Institution of Oceanography (SIO)'}}

ips = {'166.148.81.45': staMeta['UCSB'],
       '166.241.139.252': staMeta['UCI'],
       '166.241.175.135': staMeta['UCLA'],
       '132.239.117.226': staMeta['UCSD'],
       '172.16.117.233': staMeta['UCSD']}

#header names to dat log files
columns = ['server_date', 'ip', 'sst', 'conductivity', 'pressure', 'aux1', 
                'aux3', 'chlorophyll', 'aux4', 'salinity', 'date', 'time', 
                'sigmat', 'diagnosticVoltage', 'currentDraw']

attrArr = ['sst', 'conductivity', 'pressure', 'aux1', 'aux3', 'chlorophyll', #NOT INCLUDING 'time'
           'chlorophyll', 'aux4', 'salinity', 'sigmat', 'diagnosticVoltage', 'currentDraw']

#####################################################################################################

#CREATE NETCDF4 FILE STRUCTURE
def createNCshell(ncfile, ip):
    kwargs = {"zlib": True, "fletcher32":True}
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


    ncfile.naming_authority = 'sccoos.org'
    ncfile.Metadata_Conventions = 'Unidata Dataset Discovery v1.0'
    ncfile.Conventions = 'CF-1.6'
    ncfile.metadata_link = 'www.sccoos.org.progress/data-products/automateed-shore-stations/'
    # Text
    ncfile.summary = 'Automated shore station with a suite of sensors that are attached to piers'+ \
    ' along the nearshore California coast. ' + \
    'These automated sensors measure temperature, salinity, chlorophyll, turbidity '+ \
    'and water level at frequent intervals in the nearshore coastal ocean. This data can provide '+ \
    'local and regional information on mixing and upwelling, land run-off, and algal blooms.'
    ncfile.keywords = 'EARTH SCIENCE, OCEANS, SALINITY/DENSITY, SALINITY,  OCEAN CHEMISTRY, CHLOROPHYLL,'+ \
        ' OCEAN TEMPERATURE, WATER TEMPERATURE, OCEAN PRESSURE, WATER PRESSURE'
    ncfile.keywords_vocabulary = 'Global Change Master Directory (GCMD) Earth Science Keywords'
    ncfile.standard_name_vocabulary = 'CF Standard Name Table (v28, 07 January 2015)'
    ncfile.history = 'Created: '+ time.ctime(time.time())
    ncfile.comment = 'The SIO Pier automated shore station operated by SCCOOS is mounted at a nominal'+ \
    ' depth of '+str(ips[ip]['depth'])+' meters MLLW. The instrument package includes a Seabird SBE 16plus SEACAT Conductivity, '+ \
    'Temperature, and Pressure recorder, and a Seapoint Chlorophyll Fluorometer with a 0-50 ug/L gain setting.'


    ncfile.institution = 'Scripps Institution of Oceanography, University of California San Diego'
    ncfile.date_created = time.ctime(time.time())
    ncfile.date_modified = time.ctime(time.time())
    ncfile.date_issued = time.ctime(time.time())
    ncfile.project = 'Automated Shore Stations'
    ncfile.acknowledgment = 'The Southern California Coastal Ocean Observing System (SCCOOS) is one of eleven regions that contribute to the national U.S. Integrated Ocean Observing System (IOOS).'

    ncfile.publisher_name = 'Southern California Coastal Ocean Observing System'
    ncfile.publisher_url = 'http://sccoos.org'
    ncfile.publisher_email = 'info@sccoos.org'

    ncfile.processing_level = 'QA/QC has not been performed'
    ncfile.license = 'Data is preliminary and should not be used by anyone.'
    ncfile.cdm_data_type = 'Station'

    ncfile.geospatial_lon_units = 'degrees_east'
    ncfile.geospatial_lat_units = 'degrees_north'
    ncfile.source = 'insitu observations'
    ncfile.time_coverage_units = 'seconds since 1970-01-01 00:00:00 UTC'

    # CHECK
    ncfile.time_coverage_resolution = '1'
    ncfile.geospatial_lat_resolution = '2.77E-4' #?
    ncfile.geospatial_lon_resolution = '2.77E-4' #?
    ncfile.geospatial_vertical_units = 'm' #???
    ncfile.geospatial_vertical_resolution = '1' #???
    ncfile.geospatial_vertical_positive = 'down' #???

    #-----------------SPECIFIC to stations------------------------
    ncfile.title = ips[ip]['loc']+' Automated Shore Station' 
    ncfile.geospatial_lat_min = ips[ip]['lat']  #for single point???
    ncfile.geospatial_lat_max = ips[ip]['lat']
    ncfile.geospatial_lon_min = ips[ip]['lon']
    ncfile.geospatial_lon_max = ips[ip]['lon']
    ncfile.contributor_name = ips[ip]['inst']+', NOAA, SCCOOS, IOOS'
    ncfile.contributor_role = 'station operation, station funding, data management'
    ncfile.creator_name = ips[ip]['inst']
    ncfile.creator_url = ips[ip]['url']
    ncfile.geospatial_vertical_min = ips[ip]['depth'] #???
    ncfile.geospatial_vertical_max = ips[ip]['depth'] #???

    return ncfile


def tupToISO(timeTup):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', timeTup);

#Only return Day, Hour, Min, Sec in ISO 8601 duration format
#Designed, testing NSDate int, may work with epoch (subsec???)
def ISOduration(minTimeS, maxTimeS):
    secDif = maxTimeS-minTimeS
    days = secDif/(3600*24)
    dayRem = secDif%(3600*24)
    hrs = dayRem/3600
    hrRem = dayRem%3600
    mins = hrRem/60
    secs = hrRem%60
    durStr = "P"+str(days)+"DT"+str(hrs)+"H"+str(mins)+"M"+str(secs)+"S"
#     print secDif, days, dayRem, hrs, hrRem, mins, secs, durStr
    return durStr        

def NCtimeMeta(ncfile, ip):
    #SPECIFIC to file
    #Calculate. ISO 8601 Time duration
    times = ncfile.variables['time'][:]
    minTimeS = min(times)
    maxTimeS = max(times)
    minTimeT = time.gmtime(minTimeS)
    maxTimeT = time.gmtime(maxTimeS)
    ncfile.time_coverage_start = tupToISO(minTimeT)
    ncfile.time_coverage_end = tupToISO(maxTimeT)   
    ncfile.time_coverage_duration = ISOduration(minTimeS, maxTimeS)
    ncfile.date_modified = time.ctime(time.time())

##############################################################################################
def readSASS(filename):
    sass = pandas.read_csv(filename, header=None, parse_dates=[['date', 'time']], names= columns, 
                           infer_datetime_format=True)
    #STRIP bad lines
    sass = sass[sass.ip != '0.0.0.0'] #Don't include this ip
    sass = sass.dropna(subset=sass.columns, how='any') #Remove ANY lines with NaN
    sass.sst = sass.sst.str.replace('#\s+', '') #Remove '#' in temp
    # Don't add any lines that already have been written
    sass['server_date_pandas'] = pandas.to_datetime(sass.server_date, format=dateformat, utc=None)
    LRpd = pandas.to_datetime(readLastRecorded(), utc=None)
    sass = sass[sass.server_date_pandas > LRpd]

    #make the instrument datetime the index
    sass.index = pandas.to_datetime(sass.pop('date_time'), format=' %d %b %Y  %H:%M:%S', utc=None)
    sass.index = sass.index.tz_localize('UTC')
    return sass

def dataToNC(yr, ip, subset):
    yr = str(yr)
    loc = ips[ip]['loc']
    sass_netfilename = os.path.join(ncpath, loc, loc+'_'+yr+'_raw_v5-zl-fl32T.nc')
#     print "dataToNC", sass_netfilename
    if not os.path.isfile(sass_netfilename):
        ncfile = Dataset(sass_netfilename, 'w', format='NETCDF4_CLASSIC')
        ncfile = createNCshell(ncfile, ip)
        # print "added init nc meta", loc+'_'+yr+'.nc'
        ncfile.variables['time'][:] = subset.index.astype('int64')// 10**9
        for attr in attrArr:
#             ncfile.variables['sst'][:] = subset['temperature'].values
            ncfile.variables[attr][:] = subset[attr].values

    else:
        ncfile = Dataset(sass_netfilename, 'a', format='NETCDF4_CLASSIC')
        timeLen = len(ncfile.variables['time'][:]) 
        # length should be the same for time & all attributes
        ncfile.variables['time'][timeLen:] = subset.index.astype('int64')// 10**9
        for attr in attrArr:
            #atLen = len(ncfile.variables[attr][:])
            ncfile.variables[attr][timeLen:] = subset[attr].values
    NCtimeMeta(ncfile, ip)
    ncfile.close()

def log2nc(logFN):
    if os.path.isfile(logFN):
        # print filename
        # startfile = time.time()
        sassLog = readSASS(logFN)

        #Its possible to have more one year's data to bleed into next file (i.e. 12/31/14 23:59:57 in 20150101.dat)
        groupedYr = sassLog.groupby(sassLog.index.year)
        for grpYr in groupedYr.indices:
            grouped = groupedYr.get_group(grpYr).groupby('ip')
            for grpIP in grouped.indices:
                group = grouped.get_group(grpIP)
                if grpIP in ips:
                    loc = ips[grpIP]['loc']
                    dataToNC(grpYr, grpIP, group)
                writeLastRecorded(sassLog[-1:].server_date.values[0])
        # print time.time() - startfile, sassLog.shape, logFN


def readLastRecorded():
    LRfn = os.path.join(ncpath, 'latestNCrec.txt')
    if os.path.isfile(LRfn):
        LRfile = open(LRfn, 'r')
        dateStr = LRfile.read()
        LRfile.close()
        # print dateStr
        # LRtup = time.strptime(dateStr, dateformat)
        # LRpd = pandas.to_datetime(dateStr, format=dateformat, utc=None)
        return dateStr
    #file hasn't been created yet
    else:
        return '0001-01-01T00:00:00Z' #tupToISO(time.gmtime(0))

def writeLastRecorded(dateStr):
    LRfile = open(os.path.join(ncpath, 'latestNCrec.txt'), 'w') #overwrite
    dateStr = LRfile.write(dateStr)
    LRfile.close()
