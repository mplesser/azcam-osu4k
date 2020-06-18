import os

# absolute path
folder = "\\azcam\\azcam-tool"

# relative path
# folder = os.path.normpath((os.path.dirname(__file__)))

exe = f"{folder}\\azcamtool\\builds\\azcamtool.exe"
s = "start %s -s localhost -p 2402" % exe
os.system(s)
