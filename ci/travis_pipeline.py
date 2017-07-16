import os, argparse, shared_pipeline

# Please read pipeline_instructions.py before working on this file

CONFIGURATION = os.environ['CONFIGURATION'] if "CONFIGURATION" in os.environ else "Release"
REPO_NAME = os.environ['REPO_NAME']
ARCH = os.environ['ARCH']
PKG_VERSION = os.environ['PKG_VERSION']
PKG_TYPE = os.environ['PKG_TYPE']
BUILD_DIR = os.environ['TRAVIS_BUILD_DIR']
PKG_NAME = REPO_NAME + "-" + ARCH + "-" + PKG_VERSION

parser = argparse.ArgumentParser()
parser.add_argument("-step_name")
args = parser.parse_args()

def before_install():
	os.system("add-apt-repository 'deb https://dl.bintray.com/solvingj/public-deb unstable main'")

def install():
	os.system("apt-get update")
	os.system("apt-get install --allow-unauthenticated fakeroot go-bin-deb changelog jfrog-cli")

def script():
	os.system("mkdir build && cd build")
	os.chdir("build")
	os.system("cmake ../src && cmake --build . --config ${CONFIGURATION}")

def after_success():
	os.system("curl -fL https://getcli.jfrog.io | sh")
	
	if PKG_TYPE == "DEB":
	  package_cmd=(
		"go-bin-deb generate" +
		" --file deb-creation-data.json" +
		" --version " + PKG_VERSION +
		" --arch " + ARCH +
		" -o " + PKG_NAME + ".deb")
	  os.system(package_cmd)
	elif PKG_TYPE == "RPM":
	  package_cmd=(
		"go-bin-rpm generate" +
		" --file rpm-creation-data.json" +
		" --version " + PKG_VERSION +
		" --arch " + ARCH +
		" -o " + PKG_NAME + ".rpm")
	  os.system("docker run -v " + BUILD_DIR + "/:/mnt/travis solvingj/go-bin-rpm /bin/sh -c " + package_cmd)
 
  deploy_cmd = (
    "jfrog bt upload" +
    " --user ${BINTRAY_USER}" +
    " --key ${BINTRAY_KEY}" +
    " --override" +
    " --publish" +
    " --deb" if PKG_TYPE == "DEB" else "")
    
  os.system(deploy_cmd)

# This actually executes the step, must be after all methods are defined.
exec(args.step_name + "()")