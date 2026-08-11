from .trainers.potion import POTION
from .trainers.professors_research import PROFESSORS_RESEARCH
from .pokemon.pikachu import PIKACHU
from .pokemon.bulbasaur import BULBASAUR
from .pokemon.charmander import CHARMANDER
from .pokemon.squirtle import SQUIRTLE

ALL_CARDS = {
    "Potion": POTION,
    "Professor's Research": PROFESSORS_RESEARCH,
    "Pikachu": PIKACHU,
    "Bulbasaur": BULBASAUR,
    "Charmander": CHARMANDER,
    "Squirtle": SQUIRTLE
}

def get_card(name: str):
    return ALL_CARDS.get(name)