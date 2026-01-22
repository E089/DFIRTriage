import os
import json
import socket
import datetime
import shutil 

from .utils import run_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_LIST_PATH = os.path.join(BASE_DIR, "artifact_list.json")
OUTPUT_DIR_NAME = "triage_output"

def setup_output_directory():
    """
    Creates a unique, timestamped output directory for this collection.
    Example: triage_output/erica-laptop_20251107_110030/
    """
    try:
        hostname = socket.gethostname()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_folder_name = f"{hostname}_{timestamp}"
        
        base_output_path = os.path.join(os.getcwd(), OUTPUT_DIR_NAME)
        
        output_path = os.path.join(base_output_path, unique_folder_name)
        
        os.makedirs(output_path, exist_ok=True)
        
        print(f"[+] Output directory created at: {output_path}")
        
        return output_path, base_output_path, unique_folder_name

    except Exception as e:
        print(f"[!] CRITICAL ERROR: Could not create output directory.")
        print(f"[!] {e}")
        return None, None, None

def package_collection(output_dir, base_output_path, unique_folder_name):
    """
    Compresses the collected artifacts into a .tar.gz archive.
    """
    print(f"\n[*] Compressing artifacts...")
    try:
        archive_name = os.path.join(base_output_path, unique_folder_name)
        shutil.make_archive(
            base_name=archive_name,
            format='gztar',
            root_dir=output_dir
        )
        shutil.rmtree(output_dir)
        
        print(f"[+] Success! Collection compressed to: {archive_name}.tar.gz")
        print(f"[+] Removed raw data folder: {output_dir}")

    except Exception as e:
        print(f"[!] ERROR: Could not compress collection: {e}")

def main():
    """
    Main function to orchestrate the artifact collection.
    """
    print("--- Starting DFIRTriage Collector ---")
    
    output_dir, base_output_path, unique_folder_name = setup_output_directory()
    if not output_dir:
        return 
        
    try:
        with open(ARTIFACT_LIST_PATH, 'r') as f:
            artifacts = json.load(f)
    except Exception as e:
        print(f"[!] CRITICAL ERROR: Could not read {ARTIFACT_LIST_PATH}")
        print(f"[!] {e}")
        return

    print(f"[+] Successfully loaded {len(artifacts)} artifacts from JSON.")

    for artifact in artifacts:
        name = artifact.get("name", "unknown_artifact")
        command = artifact.get("command")
        
        print(f"    [*] Collecting: {name}...")
        
        if not command:
            print(f"        [!] Skipping {name}: No command specified.")
            continue
            
        stdout, stderr = run_command(command)
        output_filepath = os.path.join(output_dir, f"{name}.txt")
        
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                if stderr:
                    f.write(f"--- ERROR COLLECTING {name} ---\n")
                    f.write(f"COMMAND: {command}\n")
                    f.write(f"ERROR: {stderr}\n")
                else:
                    f.write(stdout)
            
            print(f"        [+] Saved to {name}.txt")
            
        except Exception as e:
            print(f"        [!] FAILED to write output for {name}: {e}")

    print("--- Collection Complete! ---")
    
    package_collection(output_dir, base_output_path, unique_folder_name)


if __name__ == "__main__":
    main()