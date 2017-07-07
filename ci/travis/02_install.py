import os
with open("/etc/apt/sources.list") as fin:
	print fin.read()
os.system("apt-get install -y fakeroot go-bin-deb changelog")