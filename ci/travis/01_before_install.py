import sys
import os

os.system("add-apt-repository 'deb https://dl.bintray.com/solvingj/public-deb unstable main'")
with open("/etc/apt/sources.list") as fin:
	print fin.read()


 
