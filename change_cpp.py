import os
from colorama import Fore, Style

WANTED_WIDTH = 100
DISPLAY_WIDTH = min(WANTED_WIDTH, os.get_terminal_size().columns - 2)
print("┏" + "".center(DISPLAY_WIDTH, "━") + "┓")
print(f"┃{Fore.RED}" + "CMakeLists to C++17 Utils".center(DISPLAY_WIDTH, " ") + f"{Style.RESET_ALL}┃")
print(f"┃{Style.BRIGHT+ Fore.BLACK}" + "Meltwin - 2023".center(DISPLAY_WIDTH, " ") + f"{Style.RESET_ALL}┃")
print("┗" + "".center(DISPLAY_WIDTH, "━") + "┛")
print()

REPLACE_FILTER = {
    "-std=c++11":"-std=c++17",
    "COMPILER_SUPPORTS_CXX11": "COMPILER_SUPPORTS_CXX17",
    "CMAKE_CXX_STANDARD 11": "CMAKE_CXX_STANDARD 17",
    "CMAKE_CXX_STANDARD 14": "CMAKE_CXX_STANDARD 17"
}

def fix_cmakelist(cmakelist_path: str) -> None:
    print(f"{Fore.YELLOW}▷ {Fore.RESET}Found {Fore.RED}{cmakelist_path}{Fore.RESET}", end=" ")
    with open(cmakelist_path, "r") as handle:
        data = handle.read()

    # Replacing
    changed = False
    for key, value in REPLACE_FILTER.items():
        if data.find(key) != -1:
            data = data.replace(key, value)
            changed = True

    if changed:
        with open(cmakelist_path, "w") as handle:
            handle.write(data)
    print(f"{Fore.GREEN}Fixed !" if changed else f"{Fore.BLUE}Nothing to change")

def walk_dir(dir: str, depth = 0) -> None:
    if depth >=2:
        return
    for d in os.listdir(dir):
        cmakelist_path = f"{dir}/{d}/CMakeLists.txt"
        if not os.path.isfile(cmakelist_path):
            walk_dir(f"{dir}/{d}", depth+1)
        else :
            fix_cmakelist(cmakelist_path)

if __name__ == "__main__":
    # Get all the CMakeLists.txt
    walk_dir("./src")
