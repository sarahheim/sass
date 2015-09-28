
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
        print 'true'
        #sassLog[prim] = pandas.Series(np.zeros(len(sassLog[attr]), dtype=sassLog.index))
        #sassLog[sec]  = pandas.Series(np.zeros(len(sassLog[attr]), dtype=sassLog.index))
        zeros = np.zeros(len(sassLog[attr]), dtype=int)
        primFlag = pandas.DataFrame(zeros, index=sassLog.index, columns=[prim])
        secFlag  = pandas.DataFrame(zeros, index=sassLog.index, columns=[sec])
        sassLog = pandas.concat([sassLog, primFlag, secFlag], axis=1)
    for i, x in enumerate(sassLog[attr]):
        ### currently an int, assuming increment
        ### could append string!!! or bit code number
        #sassLog[sec][i] = test
        #sassLog.iloc[i][sec] = test
        sassLog.ix[i, sec] = test
        #Failed this test (outside of range)
        if (bMin and bMin >= x) or (bMax and bMax <= x):
            #sassLog[prim][i]= 4
            sassLog.ix[i, prim]= 4
        #Passed (within range), no previous test or passed previous tests
        elif (sassLog[prim][i] == 0) or (sassLog[sec][i] == 1) :
            #sassLog[prim][i] = 1
            sassLog.ix[i, prim] = 1
        #Passed (within range), but had previous issues - keep previous number
        else:
            #sassLog[prim][i] = sassLog[prim][i]
            sassLog.ix[i, prim] = sassLog[prim][i]
    #print 'HERE', i, sassLog[prim][i], sassLog[sec][i]
    #print sassLog.iloc[i][attr]
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
print 'sst', type(sassLog['sst'][0]) #sst is str?!!!
print 'sal', type(sassLog['salinity'][0])
print 'chl', type(sassLog['chlorophyll'][0])
print 'con', type(sassLog['conductivity'][0])
print 'pre', type(sassLog['pressure'][0])

###qMin ==0 for sal, con, pres???
#sassLog['con_flag'] = sassLog['conductivity'].map(lambda x: rangeTest(x, None, None, None, 9))
#sassLog['pres_flag'] = sassLog['pressure'].map(lambda x: rangeTest(x, None, None, None, 20))
#sassLog['pres_test'] = sassLog['pressure'].map(lambda x, i: i)
sassLog = rangeTest(sassLog, 'pressure', 2, 4, -9) #test
#print type(sassLog['pressure'])
#flag = pandas.DataFrame(0, index = np.arange(len(sassLog['sst'])), columns=['test_flag'])
#flag = pandas.DataFrame(np.zeros(len(sassLog['sst']), dtype=int), index=sassLog.index, columns=['test_flag'])
#print flag[:3]
#sassLog = pandas.concat([sassLog, flag], axis=1)
#sassLog.append(flag)
#print sassLog[0:1200:200].to_csv()
print sassLog[0:1200:90].to_csv()

print "DONE! Appended a single log file", time.time()-start
