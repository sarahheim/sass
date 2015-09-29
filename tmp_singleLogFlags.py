
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

def rangeTest(sassLog, attr, bMin, bMax, test):
    prim = attr+'_flagPrimary'
    sec = attr+'_flagSecondary'
    if not prim in sassLog:
        zeros = np.zeros(len(sassLog[attr]), dtype=int)
        primFlag = pandas.DataFrame(zeros, index=sassLog.index, columns=[prim])
        secFlag  = pandas.DataFrame(zeros, index=sassLog.index, columns=[sec])
        sassLog = pandas.concat([sassLog, primFlag, secFlag], axis=1)
    for i, x in enumerate(sassLog[attr]):
        ### currently an int, assuming increment
        ### could append string!!! or bit code number
        sassLog.ix[i, sec] = test
        #Failed this test (outside of range)
        if (bMin and bMin >= x) or (bMax and bMax <= x):
            sassLog.ix[i, prim]= 4
        #Passed (within range), no previous test or passed previous tests
        elif (sassLog[prim][i] == 0) or (sassLog[sec][i] == 1) :
            sassLog.ix[i, prim] = 1
        #Passed (within range), but had previous issues - keep previous number
        else:
            sassLog.ix[i, prim] = sassLog[prim][i]
    return sassLog

def sensorRangeTest(x, bMin, bMax):
    if (bMin and bMin >= x) or (bMax and bMax <= x):
        return 4
    else:
        return 1

#b - bad, q - questionable
def climateRangeTest(x, bMin=None, qMin=None, qMax=None, bMax=None):
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
#print sassLog.dtypes #fixed: sst used to be string

#sassLog['pres_flag'] = sassLog['pressure'].map(lambda x: rangeTest(x, None, None, None, 20))
sassLog = rangeTest(sassLog, 'pressure', 2, 4, -9) #test
sassLog = rangeTest(sassLog, 'conductivity', None, 4.7, -9) #test
sassLog = rangeTest(sassLog, 'salinity', 32.88, None, -9) #test
sassLog = rangeTest(sassLog, 'sst', 16, 20, -9) #test

#print type(sassLog['pressure'])
print sassLog[0:1200:90].to_csv()

print "DONE! Appended a single log file", time.time()-start
