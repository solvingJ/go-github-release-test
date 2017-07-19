import os, argparse

# Please read pipeline_instructions.py before working on this file

CONFIGURATION = os.environ["CONFIGURATION"] if "CONFIGURATION" in os.environ else "Release"
GIT_REPO_NAME = os.environ["GIT_REPO_NAME"]
ARCH = os.environ["ARCH"]
BT_REPO_DEB = os.environ["BINTRAY_REPO_DEB"]
BT_REPO_RPM = os.environ["BINTRAY_REPO_RPM"]
BT_REPO_TARGZ = os.environ["BINTRAY_REPO_TARGZ"]
BT_REPO_CONAN = os.environ["BINTRAY_REPO_CONAN"]
BT_SUBJECT = os.environ["BINTRAY_SUBJECT"]
BT_USER = os.environ["BINTRAY_USER"]
BT_KEY = os.environ["BINTRAY_KEY"]
PKG_VERSION = os.environ["TRAVIS_JOB_NUMBER"]
PKG_PATH_DEB = "pool" + "/" + GIT_REPO_NAME[0] + "/" + GIT_REPO_NAME + "/"
PKG_PATH_RPM = GIT_REPO_NAME + "/" + ARCH + "/"
PKG_PATH_TARGZ = PKG_PATH_RPM
PKG_PATH_CONAN = PKG_PATH_RPM #Don't actually know about this yet
PKG_NAME = GIT_REPO_NAME + "-" + ARCH + "-" + PKG_VERSION
PKG_NAME_DEB = PKG_NAME + ".deb"
PKG_NAME_RPM = PKG_NAME + ".rpm"
PKG_NAME_TARGZ = PKG_NAME + ".targz"
PKG_NAME_CONAN = PKG_NAME + ".zip" #Don't actually know about this yet

parser = argparse.ArgumentParser()
parser.add_argument("-step_name")
args = parser.parse_args()

def before_install():
  os.system("add-apt-repository 'deb https://dl.bintray.com/solvingj/public-deb unstable main'")

def install():
  os.system("apt-get update")
  os.system("apt-get install --allow-unauthenticated fakeroot go-bin-deb changelog")

def script():
  os.system("mkdir build && cd build")
  os.chdir("build")
  os.system("cmake ../src && cmake --build . --config " + CONFIGURATION)

def after_success():
  package()
  deploy()

def package():
  package_deb()
  package_rpm()
  package_targz()
  package_conan()
  
def deploy():
  print("Running install_jfrog_cli()")
  install_jfrog_cli()
  print("Running config_jfrog_cli()")
  config_jfrog_cli()
  
  deb_option = "--deb=unstable/main/" + ARCH
  
  deb_upload_suffix = deb_option + " " + PKG_NAME_DEB + " " + create_pkg_location(BT_REPO_DEB) + " " + PKG_PATH_DEB
  # rpm_upload_suffix = PKG_NAME_RPM + " " +  create_pkg_location(BT_REPO_RPM) + " " + PKG_PATH_RPM
  rpm_upload_suffix = r'"(*.rpm)"' + " " +  create_pkg_location(BT_REPO_RPM) + " " + PKG_PATH_RPM
  targz_upload_suffix = PKG_NAME_TARGZ + " " +  create_pkg_location(BT_REPO_TARGZ) + " " + PKG_PATH_TARGZ
  conan_upload_suffix = PKG_NAME_CONAN + " " +  create_pkg_location(BT_REPO_CONAN) + " " + PKG_PATH_CONAN
  
  upload_bintray(deb_upload_suffix)
  upload_bintray(rpm_upload_suffix)
  #upload_bintray(targz_upload_suffix)
  #upload_bintray(conan_upload_suffix)
  
def create_pkg_location(bt_repo_name):
  return BT_SUBJECT + "/" + bt_repo_name + "/"  + GIT_REPO_NAME + "/" + PKG_VERSION
  
def package_deb():
  print("Packaging DEB")
  package_cmd=(
  "go-bin-deb generate" +
  " --file deb-creation-data.json" +
  " --version " + PKG_VERSION + 
  " --arch " + ARCH + 
  " -o " + PKG_NAME_DEB)
  print("DEB command : " + package_cmd)
  os.system(package_cmd)
    
def package_rpm():
  print("Packaging RPM")
  package_cmd=(
  "go-bin-rpm generate" +
  " --file rpm-creation-data.json" +
  " --version " + PKG_VERSION + 
  " --arch " + ARCH + 
  " -o " + PKG_NAME_RPM)
  
  print("RPM command : " + "docker run -v $PWD:/mnt/travis solvingj/go-bin-rpm /bin/sh -c \"" + package_cmd + "\"")
  os.system("docker run -v $PWD:/mnt/travis solvingj/go-bin-rpm /bin/sh -c \"" + package_cmd + "\"")
  
def package_targz():
  print("No instructions for conan packaging tar.gz")
  
def package_conan():
  print("No instructions for conan packaging yet")

def install_jfrog_cli():
  install_command=("curl -fL https://getcli.jfrog.io | sh")
  print("Installing jfrog client with command: " + install_command)
  os.system(install_command)
  
def config_jfrog_cli():
  configure_command=(
  "./jfrog bt config --user " + BT_USER + 
  " --key " + BT_KEY + 
  " --licenses MIT")
  print("Configuring jfrog client for bintray uploads with command: " + configure_command)
  os.system(configure_command)
  
def upload_bintray(upload_cmd_suffix):
  upload_cmd_prefix = "./jfrog bt upload --override=true --publish=true "
  print("Uploading files to Bintray with command: " + upload_cmd_prefix + upload_cmd_suffix)
  os.system(upload_cmd_prefix + upload_cmd_suffix)
    
# This actually executes the step, must be after all methods are defined.
exec(args.step_name + "()")