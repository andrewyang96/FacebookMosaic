import os
from config import BASEPATH

print "os.path.exists(config.py)", os.path.exists("config.py")
print "* check", os.path.join(BASEPATH, "*.jpg")
