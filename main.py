import os
import shutil
from InquirerPy import inquirer
from PokeWrapper import PokeWrapper
import Utils
from termcolor import colored

# TODO: Get basic information searching working
# TODO: Format information well
# TODO: Make it pretty with Colorama at first
# TODO: Make it pretty AND interactive with some TUI framework
# TODO: Once you've got basic information searching working, set up links between them
# TODO: Make links clickable

def main():
    PokeWrapper.LoadCaches()
    Utils.ClearScreen()
    welcome = f"{colored('Welcome to ', color='white', attrs=['bold'])}{colored('Poké', 'red', attrs=['bold'])}{colored('Term!', 'white', attrs=['bold'])}"
    prompt = "What to search for?"
    options = [
        'Pokemon',
        # 'Ability',
        # 'Type',
        'Move',
        # 'Berry',
        # 'Location',
        # 'Item',
        # 'Version',
        'Clear Cache',
        'Quit'
    ]
    choice = ''

    while True:
        print(welcome)
        try:
            choice = inquirer.select(
                message=prompt,
                choices=options
            ).execute()

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

        if choice == 'Quit' or choice == '':
            QuitGracefully()

        elif choice == 'Clear Cache':
            if os.path.exists('./cache'):
                shutil.rmtree('./cache')
            Utils.ClearScreen()

        else:
            try:
                PokeWrapper.HandleSearch(choice)
                Utils.ClearScreen()
            except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the info screen
                QuitGracefully()

def QuitGracefully():
    Utils.ClearScreen()
    PokeWrapper.SaveCaches()
    quit(0)

if __name__ == '__main__':
    main()
