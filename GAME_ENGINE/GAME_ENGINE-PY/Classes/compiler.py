import subprocess
import os
import sys

def FORCE_DEL_FOLDER(f):
    if os.listdir().__contains__(f):
        import stat
        for f1 in os.listdir(f"./{f}"):
            for f2 in os.listdir(f"./{f}/{f1}"):
                try:
                    for f3 in os.listdir(f"./{f}/{f1}/{f2}"):
                        os.remove(f"./{f}/{f1}/{f2}/{f3}") 
                    try:
                        os.chmod(f"./{f}/{f1}/{f2}", stat.S_IWRITE)
                        os.rmdir(f"./{f}/{f1}/{f2}")
                    except NotADirectoryError:
                        pass
                except NotADirectoryError:
                    os.remove(f"./{f}/{f1}/{f2}")
            os.chmod(f"./{f}/{f1}", stat.S_IWRITE)
            os.rmdir(f"./{f}/{f1}")
        os.chmod(f"./{f}", stat.S_IWRITE)
        os.rmdir(f"./{f}")

def convert_to_standalone_exe(script_path):
    """
    Converts a Python script into a standalone .exe file.
    Includes custom classes and modules automatically via PyInstaller's analysis.
    """
    if not os.path.exists(script_path):
        print(f"Error: The file '{script_path}' was not found.")
        return

    print(f"--- Starting Build Process for: {script_path} ---")
    
    script_path = "'"+script_path+"'"

    # Construct the PyInstaller command
    # --onefile: Create a single executable
    # --noconfirm: Replace existing output directories without asking
    # --clean: Clean PyInstaller cache before building

    import time

    FORCE_DEL_FOLDER("build")

    command = [
        "pyinstaller",
        "--onefile",
        "--noconfirm",
        "--clean",
        script_path,
        "> /dev/null 2>&1"
    ]

    try:
        # Execute the command
        print("eeeee")
        subprocess.check_call("pip install pyinstaller", shell=True)
        subprocess.check_call(" ".join(command), shell=True)
        FORCE_DEL_FOLDER("build")
        print("BUILD SUCCESSFUL!")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the build: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    FORCE_DEL_FOLDER("build")
    

import sys
from modulefinder import ModuleFinder

def estimate_build_time(script_path):
    finder = ModuleFinder()
    finder.run_script(script_path)
    
    # Count unique modules found
    num_modules = len(finder.modules)
    
    # Rough heuristic: 0.5 seconds per module + 10s overhead 
    # (Adjust '0.5' based on your specific machine's performance)
    base_overhead = 10 
    predicted_seconds = (num_modules * 0.5) + base_overhead
    
    return num_modules, predicted_seconds
