import os
import subprocess
from tqdm import tqdm
from colorama import init, Fore, Style
init(autoreset=True)
def list_all_directories(paths, output_file):
    directories = []
    try:
        total_dirs = 0
        for path in paths:
            for _, dirs, _ in os.walk(path):
                total_dirs += len(dirs)
        with tqdm(total=total_dirs, desc="Listing Directories", unit="dir", position=1, leave=True) as pbar, open(output_file, 'w', encoding='utf-8') as f:
            for path in paths:
                for root, dirs, _ in os.walk(path):
                    for directory in dirs:
                        dir_path = os.path.join(root, directory)
                        directories.append(dir_path)
                        tqdm.write(dir_path)
                        f.write(dir_path + '\n')
                        pbar.update(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    return directories
def load_directories_from_file(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            directories = f.read().splitlines()
        return directories
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []
def highlight_keyword(text, keyword):
    start_index = text.lower().find(keyword.lower())
    end_index = start_index + len(keyword)
    highlighted_text = (text[:start_index] + Fore.RED + Style.BRIGHT + text[start_index:end_index] + 
                        Style.RESET_ALL + text[end_index:])
    return highlighted_text
def search_and_open_directory(directories):
    while True:
        search_query = input("Enter the directory name to search for: ")
        matches = [dir_path for dir_path in directories if search_query.lower() in os.path.basename(dir_path).lower()]
        if matches:
            print("Found directories:")
            for match in matches:
                highlighted_match = highlight_keyword(match, search_query)
                print(highlighted_match)
            selected_dir = matches[0]
            print(f"Opening directory: {selected_dir}")
            if os.name == 'nt':
                os.startfile(selected_dir)
            elif os.name == 'posix':
                subprocess.run(['xdg-open', selected_dir])
            else:
                print("Unsupported OS")
        else:
            print("No directories found with the specified name.")
        search_again = input("Do you want to search for another directory? (yes/no): ").strip().lower()
        if search_again != 'yes':
            break
        clear_console()
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
if __name__ == "__main__":
    output_file = 'directory_list.txt'
    preload = input("Do you have directories saved as a text file? (yes/no): ").strip().lower()
    if preload == 'yes':
        input_file = input("Enter the path to the text file: ").strip()
        directories = load_directories_from_file(input_file)
    else:
        root_path = ['/']
        drives = ['C:\\', 'D:\\', 'E:\\']
        paths_to_scan = root_path + drives
        directories = list_all_directories(paths_to_scan, output_file)
    search_and_open_directory(directories)
    input("Press Enter to exit...")
