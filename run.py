import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    # Ensure we are in the project root
    project_root = Path(__file__).resolve().parent
    os.chdir(project_root)

    venv_dir = project_root / "my_env"
    
    # Determine executable paths based on OS
    if platform.system() == "Windows":
        python_executable = venv_dir / "Scripts" / "python.exe"
        pip_executable = venv_dir / "Scripts" / "pip.exe"
    else:
        python_executable = venv_dir / "bin" / "python"
        pip_executable = venv_dir / "bin" / "pip"

    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print(f"Virtual environment '{venv_dir.name}' not found. Creating it...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment.")
            sys.exit(1)
            
        print("Installing dependencies...")
        req_file = project_root / "music_analysis" / "requirements.txt"
        if req_file.exists():
            try:
                subprocess.check_call([str(pip_executable), "install", "-r", str(req_file)])
            except subprocess.CalledProcessError:
                print("Failed to install dependencies.")
                sys.exit(1)
        else:
            print(f"Warning: {req_file} not found.")

    # Run the pipeline
    print("Running Music Analysis Pipeline...")
    main_script = project_root / "music_analysis" / "main.py"
    
    if not main_script.exists():
        print(f"Error: {main_script} not found.")
        sys.exit(1)

    try:
        subprocess.check_call([str(python_executable), str(main_script)])
    except subprocess.CalledProcessError as e:
        print(f"Pipeline execution failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
