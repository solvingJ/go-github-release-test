import os

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
 