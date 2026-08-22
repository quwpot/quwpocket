def can_use_attack(pokemon: Pokemon, attack: Attack) -> bool:
    for req in attack.cost:

        if req.energy_type == "Colorless":
            total_cost = 0
            for type in attack.cost:
                total_cost += type.amount
            print(total_cost, pokemon.attached_energy)
            if total_cost > len(pokemon.attached_energy):
                print("not enough")
                return False

        elif pokemon.attached_energy.count(req.energy_type) < req.amount:
            print("energy amount doesnt suffice for attacking")
            return False
    return True