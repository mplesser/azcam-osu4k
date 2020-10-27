import datetime
import os
import sys

from azcam_archon.controller_archon import ControllerArchon
from azcam_archon.exposure_archon import ExposureArchon
from azcam_archon.tempcon_archon import TempConArchon
from azcam_ds9.ds9display import Ds9Display
from azcam_osu4k.detector_sta0500_osu4k import detector_sta0500_1amp
from azcam_osu4k.osu4k_custom import OSU4k

import azcam
import azcam.server
import azcam.shortcuts
from azcam.cmdserver import CommandServer
from azcam.genpars import GenPars
from azcam.header import Header
from azcam.instruments.instrument import Instrument
from azcam.telescopes.telescope import Telescope

# ****************************************************************
# parse command line arguments
# ****************************************************************
try:
    i = sys.argv.index("-system")
    option = sys.argv[i + 1]
except ValueError:
    option = "menu"

# ****************************************************************
# define folders for system
# ****************************************************************
azcam.db.systemname = "OSU4k"
azcam.db.systemfolder = os.path.dirname(__file__)
azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)
azcam.db.datafolder = os.path.join("/data", azcam.db.systemname)
azcam.db.datafolder = azcam.utils.fix_path(azcam.db.datafolder)
azcam.db.verbosity = 2  # useful for controller status
azcam.db.parfile = os.path.join(
    azcam.db.datafolder, f"parameters_{azcam.db.systemname}.ini"
)

# ****************************************************************
# enable logging
# ****************************************************************
tt = datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_%H%M%S")
azcam.db.logfile = os.path.join(azcam.db.datafolder, "logs", f"server_{tt}.log")
azcam.utils.start_logging(azcam.db.logfile, "123")

azcam.log(f"Configuring for {option}")

# ****************************************************************
# define and start command server
# ****************************************************************
cmdserver = CommandServer()
cmdserver.port = 2402
azcam.log(f"Starting command server listening on port {cmdserver.port}")
# cmdserver.welcome_message = "Welcome - azcam-itl server"
cmdserver.start()

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()

# ****************************************************************
# controller
# ****************************************************************
controller = ControllerArchon()
controller.camserver.port = 4242
controller.camserver.host = "10.0.0.2"
controller.timing_file = os.path.join(
    azcam.db.systemfolder, "archon_code", "OSU4k_1amp.acf"
)
controller.reset_flag = 1  # 0 for soft reset, 1 to upload code

# ****************************************************************
# instrument
# ****************************************************************
instrument = Instrument()

# ****************************************************************
# temperature controller
# ****************************************************************
tempcon = TempConArchon()
controller.heater_board_installed = 1

# ****************************************************************
# dewar
# ****************************************************************
controller.header.set_keyword("DEWAR", "OSU4k", "Dewar name")

# ****************************************************************
# exposure
# ****************************************************************
filetype = "FITS"
exposure = ExposureArchon()
exposure.filetype = azcam.db.filetypes[filetype]
exposure.image.filetype = azcam.db.filetypes[filetype]
exposure.display_image = 1
exposure.image.remote_imageserver_flag = 0
exposure.filename.folder = azcam.db.datafolder

# ****************************************************************
# header
# ****************************************************************
template = os.path.join(azcam.db.datafolder, "templates", "FitsTemplate_OSU4k.txt")
sysheader = Header("OSU4k", template)
sysheader.set_header("system", 0)

# ****************************************************************
# detector
# ****************************************************************
exposure.set_detpars(detector_sta0500_1amp)
exposure.fileconverter.set_detector_config(detector_sta0500_1amp)

# WCS - plate scale
sc = 1.000  # ChangeMe
exposure.image.focalplane.wcs.scale1 = 1 * [sc]
exposure.image.focalplane.wcs.scale2 = 1 * [sc]

# ****************************************************************
# telescope
# ****************************************************************
telescope = Telescope()
telescope.enabled = 0

# ****************************************************************
# read par file
# ****************************************************************
azcam.db.genpars = GenPars(azcam.db.parfile, "azcamserver")
azcam.db.genpars.parfile_read()
azcam.utils.update_pars(0, azcam.db.genpars.parfile_dict["azcamserver"])
wd = azcam.db.genpars.get_par("azcamserver", "wd", "default")
azcam.utils.curdir(wd)


# ****************************************************************
# custom OSU4k commands
# ****************************************************************
osu4k = OSU4k()
azcam.db.cli_cmds["osu4k"] = osu4k

# ****************************************************************
# apps
# ****************************************************************

# ****************************************************************
# finish
# ****************************************************************
azcam.log("Configuration complete")
