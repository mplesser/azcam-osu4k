# azcamconsole config file for OSU4k

import datetime
import os
import threading

from azcam_ds9.ds9display import Ds9Display

import azcam
import azcam.console
import azcam.shortcuts_console

# ****************************************************************
# files and folders
# ****************************************************************
azcam.db.systemname = "OSU4k"
azcam.db.systemfolder = f"{os.path.dirname(__file__)}"
azcam.utils.add_searchfolder(azcam.db.systemfolder, 0)  # top level only
azcam.utils.add_searchfolder(os.path.join(azcam.db.systemfolder, "common"), 1)
azcam.db.datafolder = os.path.join("/data", azcam.db.systemname)
parfile = f"{azcam.db.datafolder}/parameters_{azcam.db.systemname}.ini"

# ****************************************************************
# add folders to search path
# ****************************************************************
azcam.utils.add_searchfolder(azcam.db.systemfolder, 0)

# ****************************************************************
# start logging
# ****************************************************************
tt = datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_%H%M%S")
azcam.db.logger.logfile = os.path.join(azcam.db.datafolder, "logs", f"console_{tt}.log")
azcam.db.logger.start_logging()
azcam.log(f"Configuring console for {azcam.db.systemname}")

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()
dthread = threading.Thread(target=display.initialize, args=[])
dthread.start()  # thread just for speed

# ****************************************************************
# console tools
# ****************************************************************
azcam.console_tools.load()

# ****************************************************************
# try to connect to azcam
# ****************************************************************
server = azcam.get_tools("server")
connected = server.connect()  # default host and port
if connected:
    azcam.log("Connected to azcamserver")
else:
    azcam.log("Not connected to azcamserver")

# ****************************************************************
# read par file
# ****************************************************************
pardict = azcam.db.params.read_parfile(parfile)
azcam.db.params.update_pars(0, "azcamconsole")

# ****************************************************************
# clean namespace
# # ****************************************************************
