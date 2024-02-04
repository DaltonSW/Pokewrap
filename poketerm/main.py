import os

from sys import exit
from readchar import readkey, key as keys
from rich import box
from rich.table import Table

from poketerm.utils import testing
import poketerm.utils.updater as updater

from poketerm.console import console
from poketerm.config import Config
from poketerm.resources import move, ability, type, pokemon, species
from poketerm.resources import version, generation
from poketerm.resources import version_group, nature, egg_group
from poketerm.utils.visual import PrintData, ClearScreen

from poketerm.utils.searching import SearchManager
from poketerm.utils.caching import CacheManager

from poketerm.utils.caching import (
    verify_cache_dir,
    remove_cache_dir,
    save_cache,
    load_cache,
)


# region Main Util Functions
def SaveCaches():
    verify_cache_dir()
    valid_names = {}
    for resource_name in RESOURCES.keys():
        resource = RESOURCES[resource_name]
        valid_names[resource_name] = resource.VALID_NAMES
        resource.save_cache()

    save_cache("valid_names", valid_names)
    Config.SaveCache()


def ClearCaches(doQuit=False):
    remove_cache_dir()
    for resource in RESOURCES.values():
        resource.NAME_TO_DATA_CACHE.clear()
        resource.ID_TO_NAME_CACHE.clear()

    if doQuit:
        exit(0)


def HandleSearch(resource):
    query = input(f"{resource.ENDPOINT.title()} Name or ID: ").lower()
    if query == "":
        return

    with console.status(f"Querying for {resource.ENDPOINT.title()}..."):
        result = resource.HandleSearch(query)
    if result is not None:
        PrintData(result)
    return


def QuitGracefully():
    SaveCaches()
    console.clear()
    exit(0)


def HandleCacheTest():
    ClearCaches()
    testing.HandleCacheTest()
    SaveCaches()
    exit(0)


# endregion

BASE_URL = "https://pokeapi.co/api/v2/"
RESOURCES = {
    "Ability": ability.Ability,
    # 'Berry': Berry.Berry,
    "EggGroup": egg_group.EggGroup,
    "Generation": generation.Generation,
    # 'Item': Item.Item,
    # 'Location': Location.Location,
    "Move": move.Move,
    "Nature": nature.Nature,
    "Pokemon": pokemon.Pokemon,
    "Type": type.Type,
    "Version": version.Version,
    "Species": species.Species,
    "VersionGroup": version_group.VersionGroup,
}

SEARCH_OPTIONS = [
    "[A]bility",
    # "[B]erry",
    "[C]alculators",
    "[E]gg Groups",
    "[G]eneration",
    # "[I]tem",
    # "[L]ocation",
    "[M]ove",
    "[N]ature",
    "[P]okemon",
    "[T]ype",
]

ADMIN_OPTIONS = [
    # "[1] Options",
    "[2] Clear Cache",
    "[3] Clear Cache & Quit",
    "[0] Quit Without Saving",
]

SEARCH_DISPATCH = {
    "a": lambda: SearchManager.handle_search(ability.Ability.ENDPOINT),
    "e": lambda: SearchManager.handle_search(egg_group.EggGroup.ENDPOINT),
    "g": lambda: SearchManager.handle_search(generation.Generation.ENDPOINT),
    "m": lambda: SearchManager.handle_search(move.Move.ENDPOINT),
    "n": lambda: SearchManager.handle_search(nature.Nature.ENDPOINT),
    "p": lambda: SearchManager.handle_search(pokemon.Pokemon.ENDPOINT),
    "q": lambda: HandleCacheTest(),
    "t": lambda: SearchManager.handle_search(type.Type.ENDPOINT),
}

ADMIN_DISPATCH = {"2": ClearCaches, "3": lambda: ClearCaches(True), "0": QuitGracefully}


def main():
    CacheManager.load_caches()

    # if updater.CheckForUpdate():
    #     SaveCaches()
    #     exit(0)

    while True:
        try:
            ClearScreen(True)
            PrintWelcome()
            PrintChoices()
            key = readkey()
            if key == keys.ENTER:
                QuitGracefully()

            console.clear()

            if key in SEARCH_DISPATCH:
                SEARCH_DISPATCH[key]()
            elif key in ADMIN_DISPATCH:
                ADMIN_DISPATCH[key]()
            else:
                console.print("Not a valid key!")

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

    # TODO:
    #   Location
    #   Item
    #   Game/Version
    #   PokeBalls
    #   Catch Rate Calculator


def handle_dispatch(key):
    return


def PrintChoices():
    print()
    console.rule(
        "[bold white]Press a bracketed letter to search on that topic.", characters=" "
    )
    console.rule("[bold white]Press Enter to save caches and exit.", characters=" ")

    overallTable = Table(show_header=False, box=box.SIMPLE)

    searchTable, adminTable = Table(show_header=False, box=box.SIMPLE), Table(
        show_header=False, box=box.SIMPLE
    )

    for option in SEARCH_OPTIONS:
        searchTable.add_row(f"[bold]{option}[/]")

    for option in ADMIN_OPTIONS:
        adminTable.add_row(f"[bold]{option}[/]")

    overallTable.add_row(searchTable, adminTable)

    console.print(overallTable, justify="center")
    console.rule("[bold white]\[Enter] Save & Quit[/]", characters=" ")


def PrintWelcome():
    console.rule("[red]     #########    [/]", characters=" ")
    console.rule("[red]   #############  [/]", characters=" ")
    console.rule("[red]  ############### [/]", characters=" ")
    console.rule("[red] #####       #####[/]", characters=" ")
    console.rule("[white]        ###       [/]", characters=" ")
    console.rule("[white]        ###       [/]", characters=" ")
    console.rule("[white] #####       #####[/]", characters=" ")
    console.rule("[white]  ############### [/]", characters=" ")
    console.rule("[white]   #############  [/]", characters=" ")
    console.rule("[white]     #########    [/]", characters=" ")
    print()
    console.rule(f"[bold white]Welcome to [red]Poké[/]Term!", style="white")
    console.rule(f"Cache is stored at ~{os.sep}.poketerm", characters=" ")


if __name__ == "__main__":
    main()
