import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.card import Pokemon
from src.models.attack import Attack, AttackRequirement

def get_attacks() -> list[Attack]:

    """
Generate the Python code for all Attacks of a Pokemon through user inputs.
    """

    adding_attacks = True
    cost = []
    attacks = []

    while adding_attacks:


        if input("Add another attack? (y/n) ") == "y":
            name = input("Attack name: ")
            damage = int(input("Attack damage: "))
            print(f"Now we'll aquire the attack cost.")
        
            adding_cost = True
            while adding_cost:

                if input("Add another Energy type? (y/n) ") == "y":
                    typing = input("Energy type required: ")
                    amount = int(input("Amount required: "))

                    cost.append(AttackRequirement(typing, amount))

                else:
                    break

            attacks.append(Attack(name, damage, cost))
    
        else:
            return attacks

def generate_attack_code(attacks: list[Attack]) -> str:

    """
Generate Python code for attacks list.
    """

    attack_lines = []
    for i, attack in enumerate(attacks):
        cost_lines = []
        for req in attack.cost:
            cost_lines.append(f"                AttackRequirement(\"{req.energy_type}\", {req.amount})")
        cost_str = ",\n".join(cost_lines)
        
        attack_lines.append(f"""        Attack(
            name="{attack.name}",
            damage={attack.damage},
            cost=[
{cost_str}
            ]
        )""")
    
    return "[\n" + ",\n".join(attack_lines) + "\n    ]"

def generate_pokemon(name: str) -> string:

    """
Generate the complete Python file content for a Pokemon card.
    """

    max_hp = int(input("How many hp? "))
    typing = input("What type is it (Grass, ...)? ")
    stage = input("What stage is it (no capital letters)? ")
    retreat_cost = int(input("Retreat cost: "))

    weakness = input("Weakness: ")
    if weakness == "None":
        weakness = None

    evolves_from = input("Preevolution: ")

    is_ex = input("Card is ex? (y/n) ")
    if is_ex == "y":
        is_ex = True
    else:
        is_ex = False

    attacks = get_attacks()

    attacks_code = generate_attack_code(attacks)

    string = f"""from src.models.card import Pokemon\nfrom src.models.attack import Attack, AttackRequirement

{name.upper()} = Pokemon(
    name="{name}",
    card_type="pokemon",
    typing="{typing}",
    stage="{stage}",
    max_hp={max_hp},
    hp={max_hp},
    retreat_cost={retreat_cost},
    weakness="{weakness}",
    evolves_from={None if evolves_from == None else "{evolves_from}"},
    is_ex={is_ex},
    attacks={attacks_code}
)"""

    return string    

def create_pokemon_card():

    """
Create a Pokemon card file in the correct directory.
    """

    name = input("Name of the Pokemon: ")

    text = generate_pokemon(name)

    with open(f"src/cards/pokemon/{name.lower()}.py", "w") as f:
        f.write(text)

create_pokemon_card()