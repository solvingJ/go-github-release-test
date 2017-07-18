import os, argparse

# Please read pipeline_instructions.py before working on this file
CONFIGURATION = os.environ["CONFIGURATION"] if "CONFIGURATION" in os.environ else "Release"
GIT_REPO_NAME = os.environ["APPVEYOR_PROJECT_NAME"]
ARCH = os.environ["ARCH"]
BT_REPO_MSI = os.environ["BINTRAY_REPO_MSI"]
BT_REPO_NUGET = os.environ["BINTRAY_REPO_NUGET"]
BT_REPO_CHOCO = os.environ["BINTRAY_REPO_CHOCO"]
BT_SUBJECT = os.environ["BINTRAY_SUBJECT"]
BT_USER = os.environ["BINTRAY_USER"]
BT_KEY = os.environ["BINTRAY_KEY"]
CHOCO_KEY = os.environ["CHOCO_KEY"]
PKG_VERSION = os.environ["APPVEYOR_BUILD_VERSION"]
PKG_NAME = GIT_REPO_NAME + "-" + ARCH + "-" + PKG_VERSION

parser = argparse.ArgumentParser()
parser.add_argument("-step_name")
args = parser.parse_args()

def before_build():
  os.system(r'setx PATH "C:\Program Files (x86)\WiX Toolset v3.11\bin;%PATH%;"')
  os.system("choco install go-msi")

def build_script():
  generator_name = '"' + os.environ["CMAKE_GENERATOR"] + '"'
  os.system("md build")
  os.chdir("build")
  os.system("cmake -G " + generator_name + " ../src")
  os.system("cmake --build . --config " + CONFIGURATION)
    
def after_build():
  os.system("RefreshEnv")
  print("Running package_msi()")
  package_msi()
  print("Running package_nupkg()")
  package_nupkg() 
  
def deploy_script():
  print("Running install_jfrog_cli()")
  install_jfrog_cli()
  print("Running config_jfrog_cli()")
  config_jfrog_cli()

  bt_path = create_pkg_path()
  
  msi_upload_suffix = PKG_NAME + ".msi" + " " +  create_pkg_location(BT_REPO_MSI) + " " + bt_path
  nupkg_upload_suffix = PKG_NAME + ".nupkg" + " " +  create_pkg_location(BT_REPO_NUGET) + " " + bt_path
  choco_upload_suffix = PKG_NAME + ".nupkg" + " " +  create_pkg_location(BT_REPO_CHOCO) + " " + bt_path
  
  upload_bintray(msi_upload_suffix)
  upload_bintray(nupkg_upload_suffix)
  upload_bintray(choco_upload_suffix)
  #upload_choco()
  
def create_pkg_path():
  return "pool" + "/" + PKG_NAME[0] + "/" + GIT_REPO_NAME + "/"

def create_pkg_location(bt_repo_name):
  return BT_SUBJECT + "/" + bt_repo_name + "/"  + GIT_REPO_NAME + "/" + PKG_VERSION
  
def package_msi():
  package_cmd=(
  "go-msi make" + 
  " --path msi-creation-data.json" +
  " --version " + PKG_VERSION +
  " --msi " +  PKG_NAME + ".msi")
  print("MSI command : " + package_cmd)
  os.system(package_cmd)
    
def package_nupkg():
  package_cmd=(
  "go-msi choco" + 
  " --path msi-creation-data.json" +
  " --version " + PKG_VERSION +
  " --input " + PKG_NAME + ".msi"
  " --out " + PKG_NAME + ".nupkg")
  print("NUPKG command : " + package_cmd)
  os.system(package_cmd)
  
def install_jfrog_cli():
  install_command=("curl -fsSk -o jfrog.exe -L https://api.bintray.com/content/jfrog/jfrog-cli-go/%24latest/jfrog-cli-windows-amd64/jfrog.exe?bt_package=jfrog-cli-windows-amd64")
  print("Installing jfrog client with command: " + install_command)
  os.system(install_command)
  
def config_jfrog_cli():
  configure_command=(
  "jfrog bt config --user " + BT_USER + 
  " --key " + BT_KEY + 
  " --licenses MIT")
  print("Configuring jfrog client for bintray uploads with command: " + configure_command)
  os.system(configure_command)
  
def upload_bintray(upload_cmd_suffix):
  upload_cmd_prefix = "jfrog bt upload --override --publish "
  print("Uploading file to Bintray with command: " + upload_cmd_prefix + upload_cmd_suffix)
  os.system(upload_cmd_prefix + upload_cmd_suffix)
  
def upload_choco():
  choco_upload_cmd = "choco push -k=" + CHOCO_KEY + " " + NUPKG_NAME
  print("Uploading file to Chocolatey with command: " + choco_upload_cmd)
  os.system(choco_upload_cmd)
  
  
# This actually executes the step, must be after all methods are defined.
exec(args.step_name + "()")