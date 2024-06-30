"""
Python process start file
"""

import subprocess

OPTIONS = ""
CMD = f"ipython --profile azcamconsole -i -m azcam_osu4k.console -- {OPTIONS}"

p = subprocess.Popen(
    CMD,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
