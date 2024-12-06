import subprocess
import os
import sys

def main():

    print("running DockEva: ")

    command = ['./DockEva']

    for i in range(len(sys.argv)-1):
        print(sys.argv[i+1])
        command.append(sys.argv[i+1])

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    print("The script path is: ", script_path)
    subprocess.run(['make'])

    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    main()


