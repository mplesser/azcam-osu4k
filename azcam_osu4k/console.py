# azcamconsole config file for OSU4k

import datetime
import os
import threading

from azcam_ds9.ds9display import Ds9Display

import azcam
import azcam.console
import azcam.shortcuts
from azcam import api, db
from azcam.genpars import GenPars

azcam.log("Loading azcam-OSU4k environment")

# ****************************************************************
# files and folders
# ****************************************************************
azcam.db.systemname = "OSU4k"
azcam.db.systemfolder = f"{os.path.dirname(__file__)}"
azcam.utils.add_searchfolder(azcam.db.systemfolder, 0)  # top level only
azcam.utils.add_searchfolder(os.path.join(azcam.db.systemfolder, "common"), 1)
azcam.db.datafolder = os.path.join("/data", azcam.db.systemname)
azcam.db.parfile = f"{azcam.db.datafolder}/parameters_{azcam.db.systemname}.ini"

# ****************************************************************
# start logging
# ****************************************************************
tt = datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_%H%M%S")
azcam.db.logfile = os.path.join(db.datafolder, "logs", f"console_{tt}.log")
azcam.utils.start_logging(db.logfile)
azcam.log(f"Configuring console for {azcam.db.systemname}")

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()
dthread = threading.Thread(target=display.initialize, args=[])
dthread.start()  # thread just for speed

# ****************************************************************
# try to connect to azcam
# ****************************************************************
connected = azcam.api.connect()  # default host and port
if connected:
    azcam.log("Connected to azcamserver")
else:
    azcam.log("Not connected to azcamserver")

# ****************************************************************
# read par file
# ****************************************************************
azcam.db.genpars = GenPars(azcam.db.parfile, "azcamconsole")
azcam.db.genpars.parfile_read()
azcam.utils.update_pars(0, azcam.db.genpars.parfile_dict["azcamconsole"])
wd = azcam.db.genpars.get_par("azcamconsole", "wd", "default")
azcam.utils.curdir(wd)

# ****************************************************************
# add scripts to sys.path for Run
# ****************************************************************
azcam.utils.add_searchfolder(os.path.join(azcam.db.systemfolder, "scripts"))

# ****************************************************************
# define names to imported into namespace when using cli
# # ****************************************************************
azcam.db.cli_cmds.update({"azcam": azcam, "db": db, "api": api})

# ****************************************************************
# clean namespace
# # ****************************************************************
del azcam.focalplane, azcam.displays, azcam.shortcuts
del azcam.header, azcam.image
