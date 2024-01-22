#!/usr/bin/env python3
#Duncan Priestley Fri Mar 3 08:16:27 EST 2023s

#imports
import os
import subprocess


#function that exists because of how often i have to do this
def clean_subprocess_stdout(message):
	return message[2: len(message)-3]

#functions to create and remove a symbolic link
def create_symbolic_link():
	#prompt user for name
	clear_screen()
	name = input("Enter file name: ").strip()
	#logic to get file location
	clear_screen()
	file_location = find_file(name)
	#checks if the file exists
	if file_location != '1':
		#prompts user if they want to make a copy of said file
		check = input("create a symbolic link to " + file_location +"(Y/y)? ")
		if check.lower() == 'y':
			#logic for creating the sym link
			os.symlink(file_location, get_user_home()+'/'+name)
			input("Symbolic Link Created!\npress enter to continue:")
	else:
		print('file of name '+name+" does not exist")

#use os.unlink
def remove_symbolic_link():
	clear_screen()
	#prompt user for name
	name = input("Enter link name: ").strip()
	#logic to get link location
	clear_screen()
	link = find_link(name)
	#check if the link exists
	if link != '1' and link != '2':
		#prompt user if they  want  to remove the link
		check = input("remove the symbolic link at " + link +"(Y/y)? ")
		if check.lower() == 'y':
			#remove the link
			os.unlink(link)
			input("Symbolic Link removed!\npress enter to continue:")
	elif len == '1':
		print('a file by the '+name+' name does not exist within this directory')
	else:
		print('this file does not exist as a link')


#helper function: gets the users home directory
def get_user_home():
	#get the current users home directory
	local_home_cmd = str(subprocess.run(['bash', '-c', 'cd; pwd'], stdout=subprocess.PIPE).stdout)
	local_home = clean_subprocess_stdout(local_home_cmd)
	return local_home

#helper function that finds looks through your file system to find the file
#to create a sym link from/check that it exists
#I absolutly made this harder for myself
def find_file(name):
	#move to users home directory
	#get a recursive view of all of users files
	recurse_ls = subprocess.run(['bash', '-c', 'cd; pwd | ls -R'], stdout=subprocess.PIPE)
	#split up the output by directory
	directories = str(recurse_ls.stdout).split('\\n\\n')
	local_home = get_user_home()
	#start the look for the correct name
	#locations not found output is '1' for ease of checking(emulates an exit code 1)
	location = '1'
	i = 0
	#reads through each directory and then through each file in that directory
	while i < len(directories):
		files = str(directories[i]).split('\\n')
		for file in files:
			if file == name:
				return local_home + files[0][1:len(files[0])-1]+"/"+file
		i += 1

	return location

def find_link(name):
	#if result is b'' then it could not be found
	local_home = get_user_home()
	cmd = 'cd; ls -l '+ local_home +' | grep ' +name
	link_location_cmd = subprocess.run(['bash','-c', cmd], stdout=subprocess.PIPE)
	link_location = str(link_location_cmd.stdout)
	if(link_location == 'b\'\''):
		return '1'
	else:
		#now check if the file found is a link
		link_location = clean_subprocess_stdout(link_location)
		if(link_location[0] == 'l'):
			return local_home +'/'+name
		else:
			return '2'

#returns  an array of file name
def find_link_files():
	link_files = subprocess.run(['bash', '-c', "cd; ls -l | egrep l[rwx-][rwx-]"], stdout=subprocess.PIPE)
	link_files = clean_subprocess_stdout(str(link_files.stdout))
	link_files_array = link_files.split("\\n")
	#of each index the 9th item is the file name and the 11th is the absolute path
	return link_files_array

#there is some weird formatting that happens with this but I just kind of have to live with it right now
def display_symbolic_links():
	clear_screen()
	#get all links
	links = find_link_files()
	#get number of links
	link_count = '0'
	if links[0] != '':
		link_count = str(len(links))
	#display information
	print('Symbolic Link Report:\n\n')
	print('number of links is ' + link_count + ".\n")
	print('Link name:\t\tTarget Path:')
	for link in links:
		split_link = link.split(' ')
		print(split_link[9]+'\t\t\t'+split_link[11])
	print('')
	end_input = input('To return to the Main Menu, press ENTER. Or Select R/r to remove a link: ')
	#only checking if user is looking to remove a link else I can just let the function end
	if end_input.lower() == 'r':
		remove_symbolic_link()

#runs screen clear command and creates the main message
def clear_screen():
	os.system('clear')

def exit_protocol():
	print('exit protocol')

def main():
	while True:
		#initial message
		clear_screen()
		print("\t\t SHORTCUT CREATOR\n")
		print("Enter Selection:\n")
		print("\t1 - Create a shortcut in your home directory.")
		print("\t2 - Remove a shortut from you home direcory.")
		print("\t3 - Run shortcut report.\n")
		#get input to commit to actions
		u_input = input("Please enter  a  number (1-3) or (Q/q) to quit the program: ")
		if u_input.lower() == '1':
			create_symbolic_link()
		elif u_input.lower() == '2':
			remove_symbolic_link()
		elif u_input.lower() == '3':
			display_symbolic_links()
		elif u_input.lower() == 'q':
			break
		else:
			print('Not an available option please try again')
	#exit loop
	clear_screen()
	#exit message
	print("Have a good day!!!")
if __name__ == "__main__":
	main()

#running plan
#going to run this code out of the current users home directory so that symlinks can only be made from the 
#individuals current files system

