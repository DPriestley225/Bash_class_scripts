#!/usr/bin/env python3
#Duncan Priestley 2/17/2023
import subprocess
import sys

#domain suffix and hostname
def device_information():
	#running command
	hostname_command = 'hostname'
	hostname_output = run_linux_command(hostname_command)
	#spliting the parts of the hostname to take both the device hostname and domain suffix out
	hostname_output_split = hostname_output.split('.')
	#first index is the actual device hostname
	hostname = hostname_output_split[0]
	#domain suffix logic
	domain_name = ''
	i = 1
	#everthing after hostname is assumed to be the suffix
	while(i < len(hostname_output_split)):
		#on first case I do not want to add a period before it
		if i == 1:
			domain_name = hostname_output_split[i]
		else:
			domain_name = domain_name +'.'+ hostname_output_split[i]
		i += 1
	message = 'Device Information:\nHostname:\t\t'+ hostname + '\nDomain:s\t\t'+ domain_name+"\n"
	return message	

def network_information():
	default_gate_command = "ip route | grep default | awk '{print $3}'"
	DNS_command = "cat /etc/resolv.conf | grep nameserver"
	#$2 = ip $4 = mask
	ip_and_mask_command = "ifconfig | grep inet | head -1 | awk '{print $2, $4}'"
	#running commands
	default_gate = run_linux_command(default_gate_command)
	DNS_output = run_linux_command(DNS_command)
	ip_and_mask_output = run_linux_command(ip_and_mask_command)
	#splitting DNS_output and ip/mask output
	DNS_output_split = DNS_output.split('\\n')
	ip_and_mask_output_split = ip_and_mask_output.split(' ')
	#story output from split in variables
	DNS_primary = DNS_output_split[0].split(' ')[1]
	DNS_secondary = DNS_output_split[1].split(' ')[1]
	ip = ip_and_mask_output_split[0]
	mask = ip_and_mask_output_split[1]
	#create string
	message = "Network Information:\nIP Address:\t\t" + ip + "\nGateway:\t\t"+ default_gate  +"\nNetwork Mask:\t\t" + mask +"\nDNS1: \t\t\t"+DNS_primary+"\nDNS2: \t\t\t"+DNS_secondary+"\n"
	return message

#os information function
def os_information():
	#os name command
	os_name_command = "cat /etc/os-release | grep NAME | head -1"
	os_version_command = "cat /etc/os-release | grep VERSION_ID"
	#kernel version
	kernel_version_command = "hostnamectl | grep Kernel | awk '{print $3}'"
	#run commands
	os_name_output = run_linux_command(os_name_command)
	os_version_output = run_linux_command(os_version_command)
	kernel_version = run_linux_command(kernel_version_command)
	#filter output
	#getting the value
	os_name = os_name_output.split("=")[1]
	os_version = os_version_output.split("=")[1]
	#removing the parens
	os_name = os_name[1:len(os_name)-1]
	os_version = os_version[1:len(os_version)-1]
	
	message = "OS Information: \nOperating System: \t"+os_name+"\nOS Version:\t\t"+os_version+"\nKernel Version: \t"+ kernel_version+"\n"
	return message

def storage_info():
	# $2 = total $4 = available
	disk_space_command = "df -BG | grep root | awk '{print $2, $4}'"
	
	#run command
	disk_space_output = run_linux_command(disk_space_command)
	total_space = disk_space_output.split(" ")[0]
	available_space = disk_space_output.split(" ")[1]
	message = "Storage Information:\nHard Drive Copacity:\t"+total_space+"\nAvailable Space:\t"+available_space +"\n"
	return message

def processor_info():
	cpu_info_command = "lscpu | grep 'Model name'; lscpu | grep 'CPU(s):' | head -1 | awk '{print $2}'; lscpu | grep 'Core(s)' | awk '{print $4}'"
	cpu_info_output = run_linux_command(cpu_info_command)
	#filtering output
	split_info_cmd = cpu_info_output.split('\\n')
	#getting the model name
	model_name = ''
	for part in split_info_cmd[0].split(' '):
		if part in '' or part in "Model" or part in 'name:':
			continue			
		else:
			model_name = model_name + part+' '
	cpu_count = split_info_cmd[1]
	# total cores = cores per socekt times number of cpu's actually present
	core_count = str(int(split_info_cmd[2])*int(cpu_count))
	# create messages
	message = "Processor Information: \nModel Name:\t\t"+model_name+"\nNumber of Processors: \t" + cpu_count + "\nNumber of Cores:\t" + core_count+"\n"
	return message

def memory_info():
	#$2 = total, $4 = available
	ram_command = "free -h | grep Mem | awk '{print $2, $4}'"
	# run the command
	ram_cmd_output = run_linux_command(ram_command)
	ram_output_split = ram_cmd_output.split(' ')
	total = ram_output_split[0]
	available = ram_output_split[1]
	message = "Memory Information:\nTotal Ram:\t\t" +total+"\nAvailable Ram:\t\t"+available+"\n"
	return message

def run_linux_command(command):
	ps = subprocess.run(['bash', '-c', command], stdout=subprocess.PIPE)
	ps_string =str(ps.stdout)
	ps_string = ps_string[2:len(ps_string)-3]
	return ps_string

def main():
	#get messages
	device_information_message = device_information()
	network_informaion_message = network_information()
	os_information_message = os_information()
	storage_info_message = storage_info()
	processor_info_message = processor_info()
	memory_info_message = memory_info()
	#getting date
	date_command = "date"
	date = run_linux_command(date_command)
	#output file
	#source: https//:stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
	#needed some help figuring out how to do this one
	with open('output.txt', 'w') as sys.stdout:
		print('System Report ' + date+"\n")
		print(device_information_message)
		print(network_informaion_message)
		print(os_information_message)
		print(processor_info_message)
		print(memory_info_message)
if __name__ == "__main__":
        main()


#Plan:
#   Purpose:
#	This scripts purpose is to take notes of system information on all systems in a company.
#   Specifications:
#	must be directed to standard output and redirect to a file in users home directory
#	must show current date (date) 
#	must show devices hostname (hostname) 
#	must show domain suffic (hostname) 
#	must show device IPv4 (ifconfig) 
#	must show devices default gateway(take from prior script) 
#	must show devices netmask (ifcofig) 
#	must show devices primary and secondary DNS serverse (cat /etc/resolv.conf) 
#	must show device's os and os version (cat /etc/os-release) or (hostnamectl) 
#	must show devices kernel version (hostnamectl) 
#	must show the size of and space of the systems disk (df) 
#	must show devices CPU model and the number of CPUs and CPU cores (lscpu) 
#	must show devices total and available RAM (free -h | grep Mem | awk 'print $2,$3,$4') 
#   functions:
#	one function for os and kernal info
#	one function for all network information
#	one function for disk space
#	one function for CPU model number of cpus and number of cores
#	one function for ram
#	one function for writing up all information into a document and putting date at the top
#	Bonus function idea:
#	   add a function that will run all of these subsystem calls for me so i don't have
#	   to rewrite them a billion times 


