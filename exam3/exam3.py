from scapy.all import *

packets = rdpcap('TeddyBallgame.pcap')

count = 0
total = 0
goodput = 0
address = '192.168.200.2'
for i in packets:
	if i.haslayer('IP') and i.haslayer('ICMP'):
		if i[IP].dst == address and i[ICMP].type == 8:
			total += int(i[IP].len) + 14
			goodput += int(i[IP].len) - 28
		elif i[IP].src == '192.168.100.2' and i[ICMP].type == 8:
			count += 1

print('Echo Requests recieved from ' +address+ ' = '+str(count))
print('Echo Request bytes sent to ' +address + ' = '+str(total))
print('Echo Request data sent to ' + address  + ' = ' + str(goodput))

