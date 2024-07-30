import requests
from colorama import Fore, Style, init
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

def check_username(index, username):
    url = f'https://rblx.trade/api/v2/users/search?query={username}&showTerminated=true&showNormal=true&offset=0&limit=2'
    headers = {
        'Accept': 'application/json',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            return index, username, 'invalid'
        else:
            return index, username, 'valid'
    except requests.RequestException as e:
        print(Fore.YELLOW + f"[{get_current_time()}] {Style.BRIGHT}⚠ Error checking {username}: {e}")
        return index, username, 'error'

def get_current_time():
    return datetime.now().strftime("[%H:%M:%S]")

def print_completion_message():
    print(Style.BRIGHT + Fore.MAGENTA + "\n" + "=" * 50)
    print(Fore.GREEN + Style.BRIGHT + "🎉 Checking Finished! 🎉")
    print(Fore.CYAN + Style.BRIGHT + "All usernames have been processed.")
    print(Style.BRIGHT + Fore.MAGENTA + "=" * 50 + "\n")

def process_chunk(usernames, valid_file):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_username, idx, username): idx for idx, username in enumerate(usernames)}
        
        for future in as_completed(futures):
            index, username, status = future.result()
            timestamp = get_current_time()
            if status == 'valid':
                print(Fore.GREEN + f'{timestamp} {Style.BRIGHT}✔ {username} - VALID')
                with open(valid_file, 'a') as file:
                    file.write(f'{username}\n')
            elif status == 'invalid':
                print(Fore.RED + f'{timestamp} {Style.BRIGHT}✘ {username} - INVALID')
            else:
                print(Fore.YELLOW + f'{timestamp} {Style.BRIGHT}⚠ {username} - ERROR DURING CHECK')

def main():
    input_file = 'users.txt'
    valid_file = 'valid.txt'

    # Ensure the valid file exists
    if not os.path.isfile(valid_file):
        open(valid_file, 'w').close()

    chunk_size = 15000
    with open(input_file, 'r') as file:
        chunk = []
        for line in file:
            chunk.append(line.strip())
            if len(chunk) >= chunk_size:
                process_chunk(chunk, valid_file)
                chunk = []

        if chunk:
            process_chunk(chunk, valid_file)
    
    print_completion_message()

    input(Fore.CYAN + Style.BRIGHT + "Press Enter to exit...")

if __name__ == "__main__":
    main()
