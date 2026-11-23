import os, subprocess
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


def convert_to_standalone_exe(script_path):
    """
    Converts a Python script into a standalone .exe file.
    Includes custom classes and modules automatically via PyInstaller's analysis.
    """
    if not os.path.exists(script_path):
        return
    
    script_path = "'"+script_path+"'"

    # Construct the PyInstaller command
    # --onefile: Create a single executable
    # --noconfirm: Replace existing output directories without asking
    # --clean: Clean PyInstaller cache before building

    import time


    command = [
        "pyinstaller",
        "--onefile",
        "--noconfirm",
        "--clean",
        script_path
    ]

    try:
        # Execute the command
        subprocess.check_call("pip install pyinstaller", shell=True)
        subprocess.check_call(" ".join(command), shell=True)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    