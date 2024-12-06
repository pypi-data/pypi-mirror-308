import subprocess
import os
import sys
import platform

def main():

	print("running DockEva: ")

	script_path = os.path.abspath(__file__)
	script_dir = os.path.dirname(script_path)
	print("The script path is: ", script_path)
	print("The dir path is: ", script_dir)

	# check the platform of the system
	system = platform.system()
	print("Current system is: ", system)

	command = []
	if system == 'Linux' or system == 'MacOS':
		program_dir = os.path.join(script_dir, 'Linux/')
		program_path = os.path.join(program_dir, 'DockEva')
		print('The program path is: ', program_path)
		command.append(program_path)
		for i in range(len(sys.argv)-1):
			print(sys.argv[i+1])
			command.append(sys.argv[i+1])

	if system == 'Windows':
		program_dir = os.path.join(script_dir, 'Windows/')
		program_path = os.path.join(program_dir, 'DockEva')
		print('The program path is: ', program_path)
		command.append(program_path)
		for i in range(len(sys.argv)-1):
			print(sys.argv[i+1])
			command.append(sys.argv[i+1])

	result = subprocess.run(command, capture_output=True, text=True)
	print(result.stdout)

if __name__ == "__main__":
	main()


