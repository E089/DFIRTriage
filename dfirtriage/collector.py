import os
import json
import socket
import datetime

# Import our custom function from utils.py
from .utils import run_command

# Define constants
# This finds the directory the script is in, so we can find the JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_LIST_PATH = os.path.join(BASE_DIR, "artifact_list.json")
OUTPUT_DIR_NAME = "triage_output"

def setup_output_directory():
    """
    Creates a unique, timestamped output directory for this collection.
    Example: triage_output/erica-laptop_20251106_010030/
    """
    try:
        # 1. Get hostname
        hostname = socket.gethostname()
        
        # 2. Get timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 3. Create unique folder name
        unique_folder_name = f"{hostname}_{timestamp}"
        
        # 4. Create the full path
        output_path = os.path.join(os.getcwd(), OUTPUT_DIR_NAME, unique_folder_name)
        
        # 5. Create the directory (and its parents, if needed)
        os.makedirs(output_path, exist_ok=True)
        
        print(f"[+] Output directory created at: {output_path}")
        return output_path

    except Exception as e:
        print(f"[!] CRITICAL ERROR: Could not create output directory.")
        print(f"[!] {e}")
        return None

def main():
    """
    Main function to orchestrate the artifact collection.
    """
    print("--- Starting DFIRTriage Collector ---")
    
    # 1. Set up the output folder
    output_dir = setup_output_directory()
    if not output_dir:
        return # Stop if we couldn't create the folder
        
    # 2. Load the artifact list
    try:
        with open(ARTIFACT_LIST_PATH, 'r') as f:
            artifacts = json.load(f)
    except Exception as e:
        print(f"[!] CRITICAL ERROR: Could not read {ARTIFACT_LIST_PATH}")
        print(f"[!] {e}")
        return

    print(f"[+] Successfully loaded {len(artifacts)} artifacts from JSON.")

    # 3. Main Collection Loop
    for artifact in artifacts:
        name = artifact.get("name", "unknown_artifact")
        command = artifact.get("command")
        
        print(f"    [*] Collecting: {name}...")
        
        if not command:
            print(f"        [!] Skipping {name}: No command specified.")
            continue
            
        # 4. Run the command using our util function
        stdout, stderr = run_command(command)
        
        # 5. Define the output file path
        output_filepath = os.path.join(output_dir, f"{name}.txt")
        
        # 6. Write the results to the file
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                if stderr:
                    # If the command failed, log the error
                    f.write(f"--- ERROR COLLECTING {name} ---\n")
                    f.write(f"COMMAND: {command}\n")
                    f.write(f"ERROR: {stderr}\n")
                else:
                    # If it succeeded, write the output
                    f.write(stdout)
            
            print(f"        [+] Saved to {name}.txt")
            
        except Exception as e:
            print(f"        [!] FAILED to write output for {name}: {e}")

    print("--- Collection Complete! ---")
    print(f"All artifacts saved in: {output_dir}")


if __name__ == "__main__":
    # This makes the script runnable
    main()