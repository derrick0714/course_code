from socket import *

import os
import sys
import struct
import time
import select
import binascii  
 
ICMP_ECHO_REQUEST = 8
sendtime = 0;

def checksum(str):
 
	csum = 0
	countTo = (len(str) / 2) * 2
	count = 0

	while count < countTo:
		thisVal = ord(str[count+1]) * 256 + ord(str[count])

		csum = csum + thisVal

 		csum = csum & 0xffffffffL #

 		count = count + 2

 		if countTo < len(str):
 			csum = csum + ord(str[len(str) - 1])
		csum = csum & 0xffffffffL #

		csum = (csum >> 16) + (csum & 0xffff)
		csum = csum + (csum >> 16)
		answer = ~csum

		answer = answer & 0xffff
	 
	 	answer = answer >> 8 | (answer << 8 & 0xff00)
	 
	return answer



class HeaderInformation(dict):
    """ Simple storage received IP and ICMP header informations """
    def __init__(self, names, struct_format, data):
        unpacked_data = struct.unpack(struct_format, data)
        dict.__init__(self, dict(zip(names, unpacked_data)))
 
 
def receiveOnePing(mySocket, ID, timeout, destAddr):
	global sendtime
	timeLeft = timeout
	while 1:
		startedSelect = time.time()
		
		whatReady = select.select([mySocket], [], [], timeLeft)
		
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out.\n"
		
		
		recPacket, addr = mySocket.recvfrom(1024)
		timeReceived = time.time()

		#Fill in start
		# Fetch the ICMP header from the IP packet
		icmp_header = HeaderInformation(names=["type", "code", "checksum",
			"packet_id", "seq_number"
			],
			struct_format="BBHHH",
			data=recPacket[20:28]
			)
		
		if icmp_header["packet_id"] == ID: # Our packet
			ip_header = HeaderInformation(
				names=[ "version", "type", "length",
						"id", "flags", "ttl", "protocol",
						"checksum", "src_ip", "dest_ip"
						],
				struct_format="BBHHHBBHII",
				data=recPacket[:20]
				)
			packet_size = len(recPacket) - 28
			ip = inet_ntoa(struct.pack("I", ip_header["src_ip"]))
			
			delay = (timeReceived-sendtime)*1000.0
			
			print '%d bytes from %s: icmp_seq=%d ttl=%d time=%.2f ms'%(packet_size,addr,icmp_header['seq_number'],ip_header['ttl'],delay)
			print 'ip_hearder:   %s'%(ip_header)
			print 'icmp_header:  %s'%(icmp_header)

			return ''

		# Fill in end
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out.\n"
 
 
def sendOnePing(mySocket, destAddr, ID):
	global sendtime
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	myChecksum = 0
	# Make a dummy header with a 0 checksum.
	# struct -- Interpret strings as packed binary data
	
	header = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(header + data)
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		myChecksum = htons(myChecksum) & 0xffff
	 	#Convert 16-bit integers from host to network  byte order.
	else:
	 	myChecksum = htons(myChecksum)
	header = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	try:
	
		mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
		sendtime=time.time()
	except:
		#print "Unexpected error:", sys.exc_info()[0]
		#raise
		#mySocket.close()
		exit(1)
	#Both LISTS and TUPLES consist of a number of objects
	#which can be referenced by their position number within the object.

 
def doOnePing(destAddr, timeout):

	icmp = getprotobyname("icmp")
 	#SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw

 	# Fill in start
	# Create Socket here
 	try: # One could use UDP here, but it's obscure
 		mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
 	except error, (errno, msg):
 		if errno == 1 :
			etype, evalue, etb = sys.exc_info()
			evalue = etype(
			"%s - Note that ICMP messages can only be send from processes running as root." % evalue)
			raise etype, evalue, etb
		raise # raise the original error
 	

 	# Fill in end

 	myID = os.getpid() & 0xFFFF  #Return the current process i
 	sendOnePing(mySocket, destAddr, myID)
 	delay = receiveOnePing(mySocket, myID, timeout, destAddr)

 	mySocket.close()

 	return delay
 
 
def ping(host, timeout=1):
	#timeout=1 means: If one second goes by without a reply from the server,
	#the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print "Pinging %s(%s) using Python:"%(host,dest)
	#Send ping requests to a server separated by approximately one second
	while 1 :
		delay = doOnePing(dest, timeout)
		print delay
		time.sleep(1)# one second
		return delay
 

ping("127.0.0.1")
ping("www.google.com")
ping("www.yahoo.jp")
ping("www.ox.ac.uk")
ping("www.uq.edu.au")