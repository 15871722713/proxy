#conding:utf-8

from checkproxy import main
from getproxy import totalproxy
import time

while 1:
	print '*'*30+'Start time:',time.asctime( time.localtime(time.time()) ),'*'*30
	totalproxy()
	time.sleep(10)
	main()
	print '*'*45+'Sleep 300s'+'*'*45
	time.sleep(300)