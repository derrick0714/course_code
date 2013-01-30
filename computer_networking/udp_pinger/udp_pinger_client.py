#We will need the following module to generate random lost packets import random

from socket import *
import time
import sys
import signal

class pingConfig:
	client_ip 		= ''
	client_port 	= 13000;
	dest_ip			= '127.0.0.1'
	dest_port 		= 12000
	dest_host_name 	= ''
	timeout 		= 1
	times 			= 100
	send_times		= 0
	recv_times		= 0
	data_size		= 32

ping_config = pingConfig()

def is_ip( s ):
	try:
		inet_aton(s)
		return True
	except error:
		return False 

def show_result():
	print '\r\n--- %s(%s) ping statistics ---'%(ping_config.dest_host_name, ping_config.dest_ip)
	print '%d packets transmitted, %d packets received, %d%% packet loss'%(ping_config.send_times, ping_config.recv_times, int(100 - float(ping_config.recv_times)/float(ping_config.send_times)*100))

def signal_handler(signal, frame):
	show_result()
	sys.exit(0)


def main( dest_name ):
	#global ping_config;
	if is_ip( dest_name ) :
		ping_config.dest_ip 		= dest_name
		ping_config.dest_host_name 	= dest_name	
	else :
		ping_config.dest_ip 		= gethostbyname(dest_name);
		ping_config.dest_host_name	= dest_name	


	signal.signal(signal.SIGINT, signal_handler)

	#create a UDP socket
	client_socket = socket(AF_INET, SOCK_DGRAM) #assign IP address and port number to socket
	client_socket.bind(( ping_config.client_ip , ping_config.client_port))
	client_socket.settimeout(ping_config.timeout);

	print "PING %s(%s)"%(ping_config.dest_host_name, ping_config.dest_ip)
	for i in xrange(0,ping_config.times):
		time_now = int(time.time() * 1000)
		msg = 'ping %d %d'%(i,time_now)
		client_socket.sendto(msg, (ping_config.dest_ip, ping_config.dest_port))
		ping_config.send_times+=1
		try:
			data,addr = client_socket.recvfrom(1024)
		except timeout:
			print 'Request timeout for icmp_seq %d'%(i)

		else:
			ping_config.recv_times+=1
			cmd, seq_num, time_send = data.split(' ')
			time_now = int(time.time() * 1000)
			print "replay from %s: Time=%dms icmp_seq %d"%(ping_config.dest_ip,time_now-int(time_send),int(seq_num))
			time.sleep( 1 )
	show_result()

if __name__ == '__main__':
    import sys
    def usage():
        print
        print 'Usage: {0} <dest_ip>'.format(sys.argv[0])
        print

    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    main( sys.argv[1] ) 