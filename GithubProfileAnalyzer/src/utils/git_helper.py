import subprocess
import shutil

def get_git_config(key):
    """
    Retrieves a value from git config.
    """
    if not shutil.which("git"):
        return None
        
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def get_user_info():
    """
    Returns a dictionary with user info from git config.
    """
    info = {
        "name": get_git_config("user.name") or "",
        "email": get_git_config("user.email") or "",
        "username": get_git_config("github.user") or get_git_config("user.username") or ""
    }
    return info

def get_git_token():
    """
    Attempts to retrieve the GitHub token using 'git credential fill'.
    Assumes protocol=https and host=github.com.
    """
    if not shutil.which("git"):
        return None

    INPUT = "protocol=https\nhost=github.com\n"
    
    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input=INPUT,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # Parse output line by line
            for line in result.stdout.splitlines():
                if line.startswith("password="):
                    return line.split("=", 1)[1]
    except Exception:
        pass
        
    return None
