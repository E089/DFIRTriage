import subprocess
import shlex

def run_command(cmd_string):
    """
    Executes a shell command and returns its standard output and standard error.

    Args:
        cmd_string (str): The command to execute (e.g., "ls -l /etc").

    Returns:
        tuple: (stdout, stderr)
               stdout (str): The standard output of the command, or None if an error occurred.
               stderr (str): The standard error of the command, or None if successful.
    """
    try:
    
        result = subprocess.run(
            cmd_string,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  
        )

        if result.returncode != 0:
            return None, result.stderr.strip()

        return result.stdout.strip(), None

    except subprocess.TimeoutExpired:
        return None, f"Error: Command '{cmd_string}' timed out after 30 seconds."
    
    except Exception as e:
        return None, f"Error executing command: {e}"