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
        # We use shell=True to correctly handle shell features
        # like wildcards (*), pipes (|), and environment variables.
        # This is VITAL for commands like 'cat /home/*/.*history'
        result = subprocess.run(
            cmd_string,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # Don't let a command hang for more than 30s
        )

        # Check if the command itself ran but reported an error
        # (e.g., 'cat /file/that/does/not/exist')
        if result.returncode != 0:
            return None, result.stderr.strip()

        # Success!
        return result.stdout.strip(), None

    except subprocess.TimeoutExpired:
        return None, f"Error: Command '{cmd_string}' timed out after 30 seconds."
    
    except Exception as e:
        # Handle other Python-level errors (e.g., command not found)
        return None, f"Error executing command: {e}"