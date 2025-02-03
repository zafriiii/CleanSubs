import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "re", "tkinter", "tkinter.font"],
    "excludes": []
}

# Base should be set to "Win32GUI" to avoid showing a console window.
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "cleansubs.py",            # Your main script
        base=base,
        target_name="CleanSubs.exe",  # Updated parameter name
        icon=None  # Optionally add an icon file, e.g., "app.ico"
    )
]

setup(
    name="CleanSubs",
    version="1.0.0",
    description="CleanSubs - A tool to scan subtitle files for profanity based on Malaysian regulations.",
    options={"build_exe": build_exe_options},
    executables=executables
)
