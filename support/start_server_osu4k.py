"""
Python process start file
"""

import subprocess

OPTIONS = "-system osu4k"
# OPTIONS = "-testdewar"
CMD = f"ipython --profile azcamserver -i -m azcam_osu4k.server -- {OPTIONS}"

p = subprocess.Popen(
    CMD,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
