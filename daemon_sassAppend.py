
import sys, time, os, datetime
import daemon
import appendLatestToNC 

logfileLoc = '/data/InSitu/SASS/code/log2nc/appendLog.txt'

if __name__ == "__main__":
	with daemon.DaemonContext():
                # print os.getpid()
                # sys.stdout.write(os.getpid())
                f = open(logfileLoc, 'a+')
                f.write('\nSTARTING DAEMON('+str(os.getpid())+'): '+str(datetime.datetime.utcnow()))
                f.close()	
	        while True:
			# tmp_writeToTxt.randomTimeWriting()
			runtime = appendLatestToNC.appendToNCs(logfileLoc)
			if runtime < 30:
				time.sleep(40)
