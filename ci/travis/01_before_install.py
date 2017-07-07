import sys
import os

with open("/etc/apt/sources.list", "a") as fin:
	fin.write("deb https://dl.bintray.com/solvingj/public-deb unstable main")


 
