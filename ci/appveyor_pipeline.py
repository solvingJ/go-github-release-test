import os, argparse

# Please read pipeline_instructions.py before working on this file

CONFIGURATION =  os.environ['CONFIGURATION']
REPO_NAME = os.environ["APPVEYOR_PROJECT_NAME"]
ARCH = os.environ["ARCH"]
PKG_VERSION = os.environ["APPVEYOR_BUILD_VERSION"]
PKG_NAME = REPO_NAME + "-" + ARCH + "-" + PKG_VERSION

parser = argparse.ArgumentParser()
parser.add_argument("-step_name")
args = parser.parse_args()

def before_build():
  GO_MSI_PATH = "C:\Program Files\go-msi"
  WIX_PATH = "C:\Program Files (x86)\WiX Toolset v3.11\bin"

  if ARCH == "x86":
    os.environ["CMAKE_GENERATOR_NAME"] = "Visual Studio 15 2017"
  elif ARCH == "x64":
    os.environ["CMAKE_GENERATOR_NAME"] = "Visual Studio 15 2017 Win64"
    
  os.environ["PATH"] +=  os.pathsep + GO_MSI_PATH + os.pathsep + WIX_PATH
  os.environ["MSI_NAME"] = PKG_NAME + ".msi"
  os.environ["NUPKG_NAME"] =  PKG_NAME + ".nupkg"

def build_script():
  GENERATOR_NAME = os.environ["CMAKE_GENERATOR_NAME"]
  os.system("md build")
  os.chdir("build")
  os.system("cmake -G ${GENERATOR_NAME} ../src")
  os.system("cmake --build . --config " + CONFIGURATION)
  
def after_build():
  MSI_NAME = os.environ["MSI_NAME"]
  NUPKG_NAME =  os.environ["NUPKG_NAME"]

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
  
def deploy_script():
    deploy_cmd = (
    "jfrog bt upload" +
    " --user ${BINTRAY_USER}" +
    " --key ${BINTRAY_KEY}" +
    " --override" +
    " --publish")
    
  os.system(deploy_cmd)

  
# This actually executes the step, must be after all methods are defined.
exec(args.step_name + "()")