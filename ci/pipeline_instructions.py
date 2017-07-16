import os, argparse, shared_pipeline

# Usage Guidelines
# Please capture all environment variables used as local variables at the top
# Define a method for each CI step used using the method name 
# Example: def before_install():
# If two methods would be identical across CI providers, create the method normally
# Then, put the logic in shared_pipeline and call it as follows
# Example: 
#          ..from .travis.yml 
#          def before_script():
#            some_method_from_shared_pipeline()
#
#          def before_build():
#            some_method_from_shared_pipeline()
#
# Travis Docs: https://docs.travis-ci.com/user/customizing-the-build/#The-Build-Lifecycle
# Appveyor Docs: https://www.appveyor.com/docs/build-configuration/#build-pipeline

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
args.step_name()

def travis_before_install():
	os.system("add-apt-repository 'deb https://dl.bintray.com/solvingj/public-deb unstable main'")

def travis_install():
	os.system("apt-get update")
	os.system("apt-get install --allow-unauthenticated fakeroot go-bin-deb changelog jfrog-cli")

def travis_script():
	os.system("mkdir build && cd build")
	os.chdir("build")
	os.system("cmake ../src && cmake --build . --config ${CONFIGURATION}")
	os.chdir("..")
	
def travis_before_deploy():
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
 
def travis_deploy():
  deploy_cmd = (
    "jfrog bt upload" +
    " --user ${BINTRAY_USER}" +
    " --key ${BINTRAY_KEY}" +
    " --override" +
    " --publish" +
    " --deb" if PKG_TYPE == "DEB" else "")
    
  os.system(deploy_cmd)
	
def appveyor_before_build():
REPO_NAME = os.environ["APPVEYOR_PROJECT_NAME"]
ARCH = os.environ["ARCH"]
PKG_VERSION = os.environ["APPVEYOR_BUILD_VERSION"]
PKG_NAME = REPO_NAME + "-" + ARCH + "-" + PKG_VERSION
os.environ['MSI_NAME'] = PKG_NAME + ".msi"
os.environ['NUPKG_NAME'] =  PKG_NAME + ".nupkg"

gomsi_path = "C:\Program Files\go-msi"
wix_path = "C:\Program Files (x86)\WiX Toolset v3.11\bin"
os.environ["PATH"] +=  os.pathsep + gomsi_path + os.pathsep + wix_path

if ARCH == "x86":
  os.environ['CMAKE_GENERATOR_NAME'] = "Visual Studio 15 2017"
elif ARCH == "x64":
  os.environ['CMAKE_GENERATOR_NAME'] = "Visual Studio 15 2017 Win64"
 

def appveyor_build_script():
CONFIGURATION =  os.environ['CONFIGURATION']

os.system('md build')
os.system('cd build && cmake -G "' + os.environ["CMAKE_GENERATOR_NAME"] + '" ../src')
os.system('cmake --build . --config ' + CONFIGURATION)

def appveyor_after_build():
  PKG_VERSION = os.environ["APPVEYOR_BUILD_VERSION"]
  MSI_NAME = os.environ['MSI_NAME']
  NUPKG_NAME =  os.environ['NUPKG_NAME']

  msi_cmd = "go-msi make" + 
    " --path msi-creation-data.json" +
    " --version " + PKG_VERSION +
    " --msi build/msi/ " MSI_NAME

  os.system(msi_cmd)

  nupkg_cmd = "go-msi choco" + 
    " --path msi-creation-data.json" +
    " --version " + PKG_VERSION +
    " --input build/msi/ " MSI_NAME
    " --output " + NUPKG_NAME
    
  os.system(nupkg_cmd)
