import os
import sys

import azcam
import azcam.server
import azcam.shortcuts
from azcam.cmdserver import CommandServer
from azcam.system import System
from azcam.tools.instrument import Instrument
from azcam.tools.telescope import Telescope
from azcam.tools.archon.controller_archon import ControllerArchon
from azcam.tools.archon.exposure_archon import ExposureArchon
from azcam.tools.archon.tempcon_archon import TempConArchon
from azcam.tools.ds9display import Ds9Display
from azcam.tools.webserver.fastapi_server import WebServer
from azcam.tools.webtools.status.status import Status

from azcam_osu4k.detector_sta0500_osu4k import detector_sta0500_1amp

# ****************************************************************
# parse command line arguments
# ****************************************************************
try:
    i = sys.argv.index("-datafolder")
    datafolder = sys.argv[i + 1]
except ValueError:
    datafolder = None
try:
    i = sys.argv.index("-lab")
    lab = 1
except ValueError:
    lab = 0

# ****************************************************************
# define folders for system
# ****************************************************************
azcam.db.systemname = "OSU4k"

azcam.db.systemfolder = os.path.dirname(__file__)
azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)

if datafolder is None:
    droot = os.environ.get("AZCAM_DATAROOT")
    if droot is None:
        droot = "/data"
    azcam.db.datafolder = os.path.join(droot, azcam.db.systemname)
else:
    azcam.db.datafolder = datafolder
azcam.db.datafolder = azcam.utils.fix_path(azcam.db.datafolder)

parfile = os.path.join(
    azcam.db.datafolder, "parameters", f"parameters_server_{azcam.db.systemname}.ini"
)

azcam.db.verbosity = 2  # useful for controller status

# ****************************************************************
# enable logging
# ****************************************************************
logfile = os.path.join(azcam.db.datafolder, "logs", "server.log")
azcam.db.logger.start_logging(logfile=logfile)
azcam.log(f"Configuring {azcam.db.systemname}")

azcam.log(f"Configuring server for OSU4k")

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
controller.timing_file = os.path.join(azcam.db.datafolder, "archon_code", "OSU4k_1amp.acf")
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
# exposure
# ****************************************************************
filetype = "FITS"
exposure = ExposureArchon()
exposure.filetype = exposure.filetypes[filetype]
exposure.image.filetype = exposure.filetypes[filetype]
exposure.display_image = 1
exposure.folder = azcam.db.datafolder

# ****************************************************************
# header
# ****************************************************************
template = os.path.join(azcam.db.datafolder, "templates", "fits_template_OSU4k.txt")
system = System("OSU4k", template)
system.set_keyword("DEWAR", "OSU4k", "Dewar name")

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
azcam.db.parameters.read_parfile(parfile)
azcam.db.parameters.update_pars(0, "azcamserver")

# ****************************************************************
# define and start command server
# ****************************************************************
cmdserver = CommandServer()
cmdserver.port = 2402
azcam.log(f"Starting command server listening on port {cmdserver.port}")
# cmdserver.welcome_message = "Welcome - azcam-itl server"
cmdserver.start()

# ****************************************************************
# web server
# ****************************************************************
webserver = WebServer()
webserver.port = 2403  # common port for all configurations
webserver.index = os.path.join(azcam.db.systemfolder, "index_osu4k.html")
webserver.start()
webstatus = Status()
webstatus.initialize()

# ****************************************************************
# GUIs
# ****************************************************************
if 1:
    import azcam_osu4k.start_azcamtool

# ****************************************************************
# finish
# ****************************************************************
azcam.log("Configuration complete")
