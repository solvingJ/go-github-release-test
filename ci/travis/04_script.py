import os

def REPO_NAME=os.environ['REPO_NAME']
def ARCH=os.environ['ARCH']
def PKG_VERSION=os.environ['PKG_VERSION']
def PKG_TYPE=os.environ['PKG_TYPE']
def BUILD_DIR=os.environ['TRAVIS_BUILD_DIR']
def PKG_NAME=REPO_NAME + "-" + ARCH + "-" + PKG_VERSION

if PKG_TYPE == "DEB" ]:
  def deb_cmd=(
    "go-bin-deb generate "
    "--file deb-creation-data.json "
    "--version " + PKG_VERSION
    "--arch " + ARCH
    "-o " + PKG_NAME + ".deb")
  os.system(deb_cmd)
elif PKG_TYPE == "RPM"
  def rpm_cmd=(
    "go-bin-rpm generate "
    "--file rpm-creation-data.json "
    "--version " + PKG_VERSION
    "--arch " + ARCH
    "-o " + PKG_NAME + ".rpm")
  os.system("docker run -v " + BUILD_DIR + "/:/mnt/travis solvingj/go-bin-rpm /bin/sh -c " + rpm_cmd)
 