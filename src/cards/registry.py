from .trainers.potion import POTION
from .trainers.professors_research import PROFESSORS_RESEARCH
# ... import all cards

ALL_CARDS = {
    "Potion": POTION,
    "Professor's Research": PROFESSORS_RESEARCH
    # ... all cards
}

def get_card(name: str):
    return ALL_CARDS.get(name)