import os
 
CONFIGURATION =  os.environ['CONFIGURATION']

os.system('md build')
os.system('cd build && cmake -G "' + os.environ["CMAKE_GENERATOR_NAME"] + '" ../src')
os.system('cmake --build . --config ' + CONFIGURATION)