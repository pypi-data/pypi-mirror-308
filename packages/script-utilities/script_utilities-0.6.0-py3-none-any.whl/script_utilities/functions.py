import httpx as hx
import os
import tqdm as td

from . import constants as cs

cwd = os.getcwd()

def download(link: str, path: str, progress = True, description = None) -> None:
    """Downloads data from a given link at path."""
    
    if description is not None:
        print(f"Downloading {description}...")
    
    with hx.Client(http2 = True) as client:
        with client.stream("get", link) as response:
            with open(path, "wb") as file:
                total = int(response.headers.get("Content-Length", 0))
                with td.tqdm(total = total, \
                             unit_scale = True, \
                             unit_divisor = 2**10, \
                             unit = "B", \
                             disable = not progress) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                        progress.update(response.num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

def question(string: str) -> bool:
    """Asks the user a Y/N question and returns the accompagnied truth value."""
    
    while True:
        choice = input(f"{string} (Y/N): ").lower()
        
        if choice in cs.answers_true:
            return True
        elif choice in cs.answers_false:
            return False
        else:
            print("This is not an option. Please try again.")

def print_menu(strings: list[str]) -> None:
    """Prints a menu for a given list of strings."""
    
    for x, string in enumerate(strings):
        print(f"{chr(x + 65)}. {string}")

def select_option(options: list, question: str) -> object:
    """Lets the user select an option based on the given question."""
    
    while True:
        choice = input(f"{question} (Enter the corresponding option): ")
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif (index := ord(choice.upper()) - 65) in range(len(options)):
            return options[index]
        else:
            print("This is not an option. Please try again.")

def options_question(options: list, question = "What needs to be selected?",
                     display: list[str] = None) -> object:
    """Lets the user select an option based on the given question and strings."""
    
    if not display:
        display = options
    
    print_menu(display)
    return select_option(options, question)

def drive_selection() -> str:
    """Lets the user select a drive for a directory."""
    
    # Select drive for Windows only
    if os.name == "nt":
        # Collect available drives
        drives = []
        for letter in [chr(x) for x in range(ord("A"), ord("A") + 26)]:
            if os.path.exists(f"{letter}:"):
                drives.append(letter)
        
        # Print all drives
        for letter in drives:
            print(f"{letter}. Drive {letter}:")
        
        # Select a drive
        while True:
            drive = input("Which drive should be selected? (Enter the corresponding option): ").upper()
            
            if drive in drives:
                return f"{drive}:"
            else:
                print("This is not an option. Please try again.")
    else:
        return os.path.splitdrive(cwd)[0]

def clear_screen() -> None:
    """Clears the screen for Windows and Unix-based systems."""
    
    os.system("cls" if os.name == "nt" else "clear")
