import importlib
import pkgutil
from pathlib import Path

ALL_CARDS = {}

def _load_cards_from_package(package_name: str):
    """Import all modules in a package and collect UPPERCASE card constants."""
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for attr_name in dir(module):
            if attr_name.isupper():  # e.g. BULBASAUR, POTION
                card = getattr(module, attr_name)
                if hasattr(card, "name"):  # sanity check
                    ALL_CARDS[card.name] = card

# Load all subpackages
_load_cards_from_package("src.cards.pokemon")
_load_cards_from_package("src.cards.trainers")

def get_card(name: str):
    return ALL_CARDS.get(name)