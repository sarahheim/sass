
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
    
###FLAG FOR LEVEL OF QC/TESTING!?!?!???###############
###PUT TESTS in META!!!##############
### Look for outliers (over 2 st dev)?!???######
##### - allLogsToNCs.py check values against others in the day
##### - post processing against all other values in the year/file
### Spike Test???

#print sassLog[:3]
#print 'MIN', sassLog.min()
#print 'MEAN', sassLog.mean()
#print 'MAX', sassLog.max()
print 'sst', type(sassLog['sst'][0]) #sst is str?!!!
print 'sal', type(sassLog['salinity'][0])
print 'chl', type(sassLog['chlorophyll'][0])
print 'con', type(sassLog['conductivity'][0])
print 'pre', type(sassLog['pressure'][0])

###qMin ==0 for sal, con, pres???
sassLog['con_flag'] = sassLog['conductivity'].map(lambda x: defaultRangeTest(x, None, None, None, 9))
sassLog['pres_flag'] = sassLog['pressure'].map(lambda x: defaultRangeTest(x, None, None, None, 20))
print sassLog[0:1200:90].to_csv()

print "DONE! Appended a single log file", time.time()-start
