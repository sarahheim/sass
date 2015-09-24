
# Author Sarah Heim
# Date create: Sept 2015

import os, time, pandas
import numpy as np
from netCDF4 import Dataset
import sass

start = time.time()

filename = os.path.join(sass.logsdir, '2015-07', 'data-20150701.dat')
print filename
print os.path.isfile(filename)

sassLog = sass.readSASS(filename)
print type(sassLog)
print sassLog.shape

#b - bad, q - questionable
def defaultRangeTest(x, bMin=None, qMin=None, qMax=None, bMax=None):
    if (bMin and bMin >= x) or (bMax and bMax <= x):
        return 4
    elif (qMin and qMin >= x) or (qMax and qMax <= x):
        return 3
    else:
        return 1
    
def pressureRangeTest(x):
    if x < 2 or x > 4:
        return 4
    elif x < 2.3 or x > 3:
        return 3
    else:
        return 1
def salinityRangeTest(x):
    if x > 33:
        return 4
    elif x > 32.9:
        return 3
    else:
        return 1

###FLAG FOR LEVEL OF QC/TESTING!?!?!???###############
### Look for outliers (over 2 st dev)?!???######
##### - allLogsToNCs.py check values against others in the day
##### - post processing against all other values in the year/file

#print sassLog[:3]
#print 'MIN', sassLog.min()
#print 'MEAN', sassLog.mean()
#print 'MAX', sassLog.max()
print 'sst', type(sassLog['sst'][0])
print 'salinity', type(sassLog['salinity'][0])
print 'chl', type(sassLog['chlorophyll'][0])
print 'con', type(sassLog['conductivity'][0])
#sassLog['sst_flag'] = sassLog['sst'].map(lambda x:3 if x > 20 else 1)

#sassLog['sal_flag'] = sassLog['salinity'].map(lambda x:3 if x > 32.9 else 1)
#sassLog['sal_flag'] = sassLog['salinity'].map(lambda x:4 if x > 33)

#sassLog['sal_flag'] = sassLog['salinity'].map(lambda x: test(x))
sassLog['pres_flag'] = sassLog['pressure'].map(lambda x: pressureRangeTest(x))
sassLog['pres_flag2'] = sassLog['pressure'].map(lambda x: defaultRangeTest(x, None, 2, 4, 20))
print sassLog[0:1200:45].to_csv()

print "DONE! Appended a single log file", time.time()-start
