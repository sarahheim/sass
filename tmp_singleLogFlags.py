
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

def rangeTest(sassLog, attr, test, bMin=None, qMin=None, qMax=None, bMax=None):
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
        #Failed this test (outside of BAD range)
        if   (bMin and bMin >= x) or (bMax and bMax <= x):
            sassLog.ix[i, prim]= 4
        #Suspect this test (outside of SUSPECT range)
        elif (qMin and qMin >= x) or (qMax and qMax <= x):
            sassLog.ix[i, prim]= 3
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
#TEST TESTS
#sassLog = rangeTest(sassLog, 'pressure', -9, 2, 2.3, 3, 4) #test
#sassLog = rangeTest(sassLog, 'conductivity', -9, 0, None, None, 4.7) #test
#sassLog = rangeTest(sassLog, 'salinity', -9, None, 32.88, 33.3, None) #test
#sassLog = rangeTest(sassLog, 'sst', -9, 16, 18.3, 19, 20) #test

#QC TESTS: sensor range fail = 4, SoCal fail = 3 (suspect)
#sst tests: sensor range -5 to 35C, SoCal 8 to 30C
sassLog = rangeTest(sassLog, 'sst', 2, -5, 8, 30, 35)
#conductivity test: sensor range AND SoCal 0 to 9 s/m
sassLog = rangeTest(sassLog, 'conductivity', 2, 0, None, None, 9)
#salinity test: SoCal 30 to 34.5 psu
sassLog = rangeTest(sassLog, 'salinity', 2, None, 30, 34.5, None)
#pressure test: sensor range 0 to 20 dbar, SoCal 1 to 6 dbar
sassLog = rangeTest(sassLog, 'pressure', 2, 0, 1, 6, 20) 

#print type(sassLog['pressure'])
print sassLog[0:1200:90].to_csv()

print "DONE! Appended a single log file", time.time()-start
