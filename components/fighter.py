class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:

            results.append(
                {'message': f"{self.owner.name.capitalize()} attacks " +
                    f"{target.name} for {str(damage)} HP"})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append(
                {'message': f"{self.owner.name.capitalize()} laughs " +
                    f"at {target.name}'s ineffective attack."})

        return results
