import platform
from Settings.settings import User, App
from colorama import init, Style, Fore


__all__ = ['intro'] 

def intro():
    match platform.system():
        case "Linux":
            introLinux() 
        case "Darwin":
            introOs() 
        case "Windows", _:
            introWindows()  # default

def introLinux():
    RESET = "\033[0m"
    BRIGHT = "\033[1m"
    ITALIC = "\033[3m"
    BLUE = "\033[34m"

    print(f"{BRIGHT}{BLUE}{App.name}{RESET}")
    print(f"- by {ITALIC}{User.name} {User.surname}{RESET} -\n")

def introOs():
    introLinux()

def introWindows():
    init(autoreset=True)
    print(Style.BRIGHT + Fore.BLUE + f"{App.name}")
    print(f"- by {User.name} {User.surname} -\n")
