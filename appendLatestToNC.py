
#
# author Sarah Heim
# date create: May 2015
#
# Description: Read new log files and append to existing NetCDFs
# Input: location of log files and location of NCs(both in sass.py)
# Output: existing netCDFs
#
# Plans:


import time, os, datetime, pandas
import sass
# day can change before day's file exists!!!!!

def dt(str):
    return datetime.datetime.strptime(str, sass.dateformat)

def datefilename(dt):
    # time.strftime("%Y-%m/data-%Y%m%d.dat", tup)
    name = dt.strftime("%Y-%m/data-%Y%m%d.dat")
    return os.path.join(sass.logsdir, name)

## LRtup = sass.readLastRecorded()
## LRdt = datetime.datetime.fromtimestamp(time.mktime(LRtup))
def appendToNCs(logfile):
    #Make log, for testing!!!!!!!
    looplimit = 30
    log = open(logfile, 'a+')
    #log.write('STARTING Script: '+time.strftime(sass.dateformat, time.gmtime()))
    start = time.time()
    LRstr = sass.readLastRecorded()
    if (LRstr):
        LRdt = dt(LRstr)
        # print "Last Recorded  date:", LRdt.timetuple()[0:3]
        #log.write("\tLast Recorded  date: " + str(LRdt.timetuple()[0:3])+"\n")
        # print "Today's server date:", time.gmtime()[0:3]
        #log.write("\tCurrent server date: " + str(time.gmtime())+"\n")
        if LRdt.timetuple()[0:3] < time.gmtime()[0:3]:
            # print "initial file:", time.time()-start, datefilename(LRdt)
            #log.write('\nDIF day, catching up: ')
            #log.write("\n\tinitial file: " + str(time.time()-start)+" "+ datefilename(LRdt))
            sass.log2nc(datefilename(LRdt))
            loopCount = 0
            while LRdt.timetuple()[0:3] < time.gmtime()[0:3]:
                nextDayFile = datefilename(LRdt + datetime.timedelta(days=1)) #increment day
                # print "looping:", time.time()-start, nextDayFile
                #log.write("\n\tlooping: " + str(time.time()-start) +" "+  nextDayFile)
                sass.log2nc(nextDayFile)
                LRdt = dt(sass.readLastRecorded())
                #New Day/Today may not exist just yet!!!
                # exit or stuck in loop until file is created
                if nextDayFile == datefilename(datetime.datetime.utcnow()): 
                    #log.write('\n\tReached today, STOPPING')
                    return time.time()-start 
                loopCount += 1
                if loopCount > looplimit:
                    #log.write('\n\tReached loop limit, STOPPING: '+str(datetime.datetime.utcnow()))
                    return time.time()-start
 
        else:
            # Same Day
            # if file exists, read today's Last Line Server datetime (LLSdt)
            if os.path.isfile(datefilename(LRdt)):
                #USE Pandas. Last line could be a bad/ignored line
                # for line in open(datefilename(LRdt), 'r'):
                #     last=line
                # LLSstr = last.split(',')[0]
                pre = sass.readLastRecorded()
                # print "Last Rec'd datetime:", pre
                #log.write("\tLast Rec'd datetime: " + pre+"\n")
                sass.log2nc(datefilename(LRdt))
                post = sass.readLastRecorded()
                # print "post       datetime:", post
#                 if (pre==post):
#                     log.write("\tNO UPDATE")
#                 else:
#                     log.write("\tNew: " + post)
         
        #        if LLSdt != LRdt:
        #            print "add new data from TODAY"
        #            sass.log2nc(datefilename(LRdt))
        #        else:
        #            print "nc files are up to date"
            #else:
                # print "today's file doesn't exist yet", datefilename(LRdt)
                #log.write("\ntoday's file doesn't exist yet: " + datefilename(LRdt)+"\n")
    else:
        log.write("\nERROR: Latest Recorded file does NOT exist! \n") 
#    print "DONE APPENDING", time.time()-start
#    log.write("\tDONE! " + str(time.time()-start)+"\n")
    log.close()
    return time.time()-start

logfileLoc = '/data/InSitu/SASS/code/log2nc/appendLog.txt'
rt = appendToNCs(logfileLoc)
print "called", rt
