import subprocess
import os
import sys

def main():

	print("running DockEva: ")

	script_path = os.path.abspath(__file__)
	script_dir = os.path.dirname(script_path)
	print("The script path is: ", script_path)
	print("The dir path is: ", script_dir)

	if os.path.exists(os.path.join(script_dir, 'DockEva')) == False:
		subprocess.run('make', shell=True, cwd=script_dir)
	# subprocess.run(['cd', script_dir, '&&', 'make'], shell=True)

	program_path = os.path.join(script_dir, 'DockEva')

	print('The program path is: ', program_path)

	command = [program_path]

	for i in range(len(sys.argv)-1):
		print(sys.argv[i+1])
		command.append(sys.argv[i+1])

	# make_path = os.path.join(script_dir, 'Makefile')
	# print("Make file path is: ", make_path)
	# subprocess.run('make', '-f', make_path)

	result = subprocess.run(command, capture_output=True, text=True)
	print(result.stdout)

if __name__ == "__main__":
	main()


