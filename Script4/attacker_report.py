#!/usr/bin/env python3
#Duncan Priestley Fri Mar 24 08:04:17 EDT 2023s
#for this script to work you need to install the following packages using the commands
#listed below:
#python3 -m pip install python-geoip-python3
#python3 -m pip install python-geoip-geolite

#import statements
#ip to country
from geoip import geolite2
#regex used for various checks
import re
#os (used to clear screen)
import os
#date and time
import datetime
#reads  file and check lines for any failed authentication attempts
#function return a set of dictionaries
def read_file(filename):
	file = open(filename, 'r')
	file_lines = file.readlines()
	#where the dictionary entries will be held
	failed_authens = []
	for line in file_lines:
		check1 = 'Failed password for root from' in line
		check2 = re.search("PAM +[0-9] more authentication failures",line)
		check3 = 'Failed password' in line
		if check1:
			#get the ip
			ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
			#check if the ip exists within the dictionaries within the list
			entry_exists, entry = check_for_ip(failed_authens, ip.group())
			#if it isn't make a new dictionary entry with the ip and country
			if entry_exists == False:
				failed_authens.append(create_entry(ip.group(), 1))
			#else increment the attempt count by one
			else:
				update_count(entry, 1)
		elif check2 != None:
			#get the ip
			ip = re.search('rhost=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
			#check if the ip exists within the dictionaries within the list
			entry_exists, entry = check_for_ip(failed_authens, ip)
			count = int(check2.group().split(' ')[1])
			#if it isn't make a new entry with ip and country
			if entry_exists == False:
				#consider putting the append into the method
				failed_authens.append(create_entry(ip.group().split('=')[1], count))
			#else increment by the count mentioned in the PAM message
			# do so by using the check2 variable and split
			else:
				update_count(entry, count)
		elif check3:
			#get the ip
			ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
			#check if the ip exists within the dictionaries within the list
			entry_exists, entry = check_for_ip(failed_authens, ip.group())
			#if it isn't make a new dictionary entry with the ip and country
			if entry_exists == False:
				failed_authens.append(create_entry(ip.group(), 1))
			#else increment the attempt count by one
			else:
				update_count(entry, 1)
	sortList(failed_authens)
	return failed_authens

#helper method to read file to check if the ip exists within the current dictionary list
def check_for_ip(list, ip):
	#first case list is empty
	if len(list) < 1:
		return False, 'none'
	else:
		for di in list:
			#second case ip address exists within list dictionary entries
			if di['ip'] == ip:
				return True, di
		#third case ip address does not exist within list dictionary entries
		return False, 'none'

#helper function for read_file
#if going through check 1 the count is 1
#else count is equal to the count in the PAM message
#returns a dictionary item to be place within the authentication failure list
def create_entry(ip, count):
	#just need to get the geolite2 results and make it into a basic dictionary
	#setup geoip
	match = geolite2.lookup(ip)
	#match returns as string finding country
	country = 'ph'
	if match is not None:
		country = match.country
	item = {
	'ip': ip,
	'count': count,
	'country': country,
	'is_attack': False

	}
	return item
#method to check if an IP is considered to be attacking
def update_count(dictionary, count):
	dictionary['count'] += count
	if dictionary['count'] >= 10 and dictionary['is_attack'] == False:
		dictionary['is_attack'] = True

#function to sort the list that is returned
def sortList(li):
	#property being sorted by
	prop = lambda a : a['count']
	#actual sorting
	li.sort(reverse=False,key=prop)

def print_attacker_info(failed_authens):
	#create the date object
	d = datetime.datetime.now()
	#print out the attacker report
	print('Attacker Report - ' + d.strftime('%B') + ' ' + d.strftime('%d') + ', ' + d.strftime('%Y')+'\n')
	print('Count:\tIP Adress:\tCountry:')
	for item in failed_authens:
		if item['is_attack'] == True:
			print( str(item['count'])+ '\t' + item['ip']+'\t'+item['country'])
def main():
	os.system('clear')
	filename = './syslog.log'
	failed_authens = read_file(filename)
	print_attacker_info(failed_authens)

if __name__ == "__main__":
        main()

#plan for reading the file:
#targets to look for for failed logins are:
#	"failed password for root from [ip]"
#	"PAM # more authentication failures; (gen info) rhost=[ip]"

#plan for checking for an attack:
#it counts as an attack if there are more than 10 attempts
#	if I where to do this for a job I would alsobe counting time inbetween attempts
#	as many of the things that could be called attacks havie groupings of about
# 	2 seconds between each login attemps

#storage plan:
#will store all of the raw information within a dictionary
#	this dictionary will contain the ip and the number of attacks
#	it may also potentially store the date
#if a dictionary entry is deemed to be an attack it will be stored in a seperate list
#that will contain the entry and its corresponding country
#	Consider storing this information in a file instead to create a permanent log
#self note(syntax help):
#dictionaries:
#	dictionary_name = {
#	"item_name[1]": value,
#	"item_name[2]": value,...
#	}
#	or
#	dictionary_name = dict(item_name[1] = value, item_name[2] = value, ...)
#	dictionary_name['item_name[1]']
#theoretical regex to find ip
#	 "[ ]+[0-9]*[0-9][.]+[0-9]*[0-9][.]+[0-9]*[0-9][.]+[0-9]*[0-9]"
#	There has got to be a better way of doing this
#	better way: "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1-3}"
#Theoretical regex for hadnling the PAM messages
#	"PAM +[0-9] more authentication failures;" -to check for the PAM message
#	"rhost=\d{1,3\.\d{1,3}\.\d{1,3}\.\d{1,3}" - getting the ip

#requirements:
#	script contains shebang 
#	Script has executable permissions 
#	Script is commented with my name and the date 
#	Script is titled 'attacker_report.py' 
#	Script clears the terminal when it runs(need os)
#	Report shows 10+ failed attempts(as an attack)
#	shows headers, count, ipaddress, and country
#	report shows current date
#	Count is sorted in ascending order
#	Regex is used to find ip address
#	Report identifies IP address and country of origin
#	Report is organized and readable
#	script is commented
#	script is written in a pythonic style(gonna try doing this without subprocess)
#	scripts runs without errors
#	scripts works as intended
