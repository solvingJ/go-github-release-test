import os

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
