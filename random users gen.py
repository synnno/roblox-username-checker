import random
import string
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_username(length, include_numbers):
    characters = string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_positive_integer(prompt_text):
    while True:
        try:
            value = int(Prompt.ask(prompt_text))
            if value <= 0:
                raise ValueError("The number must be a positive integer.")
            return value
        except ValueError as e:
            console.print(f"[bold red]Invalid input:[/bold red] {e}. Please enter a positive integer.")

def get_yes_no(prompt_text):
    while True:
        response = Prompt.ask(prompt_text).strip().lower()
        if response in ['yes', 'no']:
            return response == 'yes'
        console.print(f"[bold red]Invalid input:[/bold red] Please enter 'yes' or 'no'.")

def main():
    clear_console()
    console.print("[bold cyan]https://github.com/synnno[/bold cyan]")
    username_length = get_positive_integer("[bold magenta]Enter the number of letters for each username (max 20):[/bold magenta]")
    number_of_usernames = get_positive_integer("[bold magenta]Enter the number of usernames to generate:[/bold magenta]")
    include_numbers = get_yes_no("[bold magenta]Should the usernames contain numbers? (yes/no):[/bold magenta]")

    if username_length > 20:
        console.print("[bold red]Username length cannot exceed 20 characters. Setting length to 20.[/bold red]")
        username_length = 20

    usernames = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Generating usernames...", total=number_of_usernames)
        for _ in range(number_of_usernames):
            usernames.append(generate_random_username(username_length, include_numbers))
            progress.update(task, advance=1)

    output_file = 'random_usernames.txt'
    with open(output_file, 'w') as file:
        for username in usernames:
            file.write(f'{username}\n')

    console.print(f"\n[bold green]{number_of_usernames} usernames of {username_length} letters each have been generated and saved to '{output_file}'.[/bold green]")
    Prompt.ask("[bold yellow]Press Enter to exit...[/bold yellow]")

if __name__ == "__main__":
    main()
