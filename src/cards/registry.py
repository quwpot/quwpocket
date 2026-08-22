from .trainers.potion import POTION
from .trainers.professors_research import PROFESSORS_RESEARCH
from .pokemon.bulbasaur import BULBASAUR

ALL_CARDS = {
    "Potion": POTION,
    "Professor's Research": PROFESSORS_RESEARCH,
    "Bulbasaur": BULBASAUR
}

def get_card(name: str):
    return ALL_CARDS.get(name)