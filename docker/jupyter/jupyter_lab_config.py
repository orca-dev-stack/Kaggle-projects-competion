import subprocess
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    os.chdir(PROJECT_ROOT)
    cmd = ["docker", "compose", "up", "jupyter"]
    print("Launching Osprey Jupyter workspace...")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
