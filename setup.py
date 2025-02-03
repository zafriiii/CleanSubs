import sys
import os
from cx_Freeze import setup, Executable

# Locate the python312.dll in your Python installation.
# This uses sys.exec_prefix to determine the installation directory.
python_dll = os.path.join(sys.exec_prefix, "python312.dll")

# Define the build_exe options, including the DLL.
build_exe_options = {
    "packages": ["os", "re", "tkinter", "tkinter.font"],
    "include_files": [python_dll]  # Include python312.dll
}

# Set the base for a GUI application so that no console window appears.
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "cleansubs.py",            # Your main script
        base=base,
        target_name="CleanSubs.exe",  # The desired name for the executable
        icon=None  # You can specify an icon file here if available.
    )
]

setup(
    name="CleanSubs",
    version="1.0.0",
    description="CleanSubs - A tool to scan subtitle files for profanity based on Malaysian regulations.",
    options={"build_exe": build_exe_options},
    executables=executables
)
