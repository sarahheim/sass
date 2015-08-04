
#
# author Sarah Heim
# date create: May 2015
#
# Description: Read all log files and create NetCDFs
# Input: location of log files and location of where to put NCs(both in sass.py)
# Output: netCDFs
#
# Plans:

#import pandas
import time, os
import sass

start = time.time()
#Loop through ALL log files and put in NC files
mnArr = os.listdir(sass.logsdir)
mnArr.sort()
for mn in mnArr:
    mnpath = os.path.join(sass.logsdir, mn)
    if os.path.isdir(mnpath):
        # print "folder:", mn
        startfld = time.time()
        #Loop through all log files
        filesArr = os.listdir(mnpath)
        filesArr.sort()
        for fn in filesArr:
            filename = os.path.join(mnpath, fn)
            sass.log2nc(filename)
    print time.time() - startfld, mn
print "DONE", time.time()-start, time.strftime(sass.dateformat, time.gmtime())
