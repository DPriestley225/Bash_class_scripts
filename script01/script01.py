#!/usr/bin/env python3

#imports here
import os
import subprocess

#function to get default gate
#this was a weird way to do it
def find_default_gate():
	gate = ' '
	#get the ip route output
	command = subprocess.run(['ip', 'route'], stdout=subprocess.PIPE)
	#turn output into a list
	filtered = str(command.stdout).split('\\n')
	#get the line with default gateway
	for line in filtered:
		if 'default' in line:
			#gets the actual ip
			line_filtered = line.split(' ')
			i = 0
			for item in line_filtered:
				if 'default' in item and 'via' in line_filtered[i+1]:
					return line_filtered[i+2]
				i = i+1
	#means that the gateway could not be found
	return 0
# *2 takes an input of the target ip address
# Test by storing the ping resultsin a file or array
# then check the final results line and in the loss rate is 0% then it was successful
# else the test failed
def test_connection(ip_address, name):
	os.system('clear')
	#incase there is no gateway
	if ip_address == 0:
		print('Default Gateway Could not be found')
	#initial message here
	print('testing connection to ' + name+'...')
	#test run and results storage here
	command =  subprocess.run(['ping', '-c 4', ip_address], stdout=subprocess.PIPE)
	filtered = str(command.stdout).split('\\n')
	results_line = filtered[len(filtered)-3]
	filtered_results = str(results_line.split(',')[2]).split(' ')
	#display results
	os.system('clear')
	if '0%' == filtered_results[1]:
		print('Connection to '+ name + ': SUCCESS\n')
	else:
		print('Connection to ' + name + ': FAILED\n')

# *1 or the main is here
def main():
	#initial variables
	still_going = True
	user_input = ''
	gateway_ip = ''
	remote_ip = '129.21.3.17'
	#run class to get and set device gateway ip here
	gateway_ip = find_default_gate()
	#initiation text here
	#loop here
	while(still_going == True):
		#loop text here
		print('\t********************************')
		print('\t*** Ping Test Troubleshooter ***')
		print('\t********************************\n')
		print('Enter Selection:\n')
		print('\t1 - Test connectivity to your gateway.')
		print('\t2 - Test for remote connectivity.')
		print('\t3 - Test for DNS resolution.')
		print('\t4 - Display gateway IP Address\n.')
		#loop input prompt and response here
		user_input = input('Please enter a number (1-4) or \"Q/q\" to quit program.\t')
		#if statements and calls here
		#if input is 1 then test gateway
		if '1' in user_input:
			test_connection(gateway_ip, 'default gateway')
		#elif input is 2 then test remote connectivity
		elif '2' in user_input:
			test_connection(remote_ip, 'remote ip')
		#elif input is 3 then test google dns resolution
		elif '3' in user_input:
			test_connection('8.8.8.8', 'google\'s dns')
		#elif input is 4 display devices gateway IP
		elif '4' in user_input:
			os.system('clear')
			print('Your Default Gateway is '+gateway_ip+'\n')
		#elif input is q or Q break and display exit message
		elif 'q' in str.lower(user_input):
			os.system('clear')
			print('Goodbye')
			break
		#else tell them that the input is incorrect
		else:
			#clear terminal
			os.system('clear')
			print('incorrect input try again\n')
main()
#NOTES:
#Goal:
#	create a script that tests connectivity to google to multiple sources
#	these sources are: google dns, remote ip, gateway
#	you should also be able to check your own IP address
#	should loop your options to input these commands until the user uses a quit statement

#How to:
# 	have 3 primary classes
#	   *1 is main and will run the primary loop
#	   *2 will ping a target that depends on what the user wants to check
#	   *3 will be an exit program(not neccessary)
#	if time allows:
#	   have a class to find your gateway which will run before the loop
#	   sub function for *2 to check results(unneccessary)

#imports:
#	inetfaces
#	os
#	subprocesses
