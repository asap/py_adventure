import tcod as libtcod

from components.ai import ConfusedMonster
from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({
            'consumed': False,
            'message': Message(
                'You are already at full health',
                libtcod.yellow)
        })
    else:
        entity.fighter.heal(amount)
        results.append({
            'consumed': True,
            'message': Message(
                'Your wounds start to fade. You feel much better!',
                libtcod.green)
        })

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if (entity.fighter and
            entity != caster and
                libtcod.map_is_in_fov(fov_map, entity.x, entity.y)):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({
            'consumed': True,
            'target': target,
            'message': Message(
                "You read the scroll in your hand and a low rumble begins to "
                "shake the room. With a white flash and a crack of thunder, "
                "a bolt of lightning leaps from the page and strikes "
                f"{target.name},  dealing {damage} HP of damage. "
                "The scroll crumbles to ash as the light fades.",
                libtcod.yellow)})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({
            'consumed': False,
            'target': None,
            'message': Message(
                "No enemy close enough to strike. "
                "You'd be wasting the scroll.", libtcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            'consumed': False,
            'message': Message(
                "You don't see anyone worthy of a fireball yet.",
                libtcod.yellow)})

        return results

    results.append({
        'consumed': True,
        'message': Message(
            "The scroll in your hand begins to smoke and ignites with a "
            "red flash. The flames leap from the page and fill the room with "
            f"fire, burning everything within {radius} tiles."
            "The scroll crumbles to ash as the flames burn out.",
            libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({
                'message': Message(
                    f"The {entity.name} gets burned for {damage} HP.",
                    libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            'consumed': False,
            'message': Message(
                "You don't see anyone to cast confusion on.",
                libtcod.yellow)})

        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({
                'consumed': True,
                'message': Message(
                    "The odd symbols of the scroll begin to "
                    "swirl on the page. You hear the laughter of "
                    f" a disembodied voice as the {entity.name} begins "
                    "to stumble and slur as if they've had a few pints. "
                    "For some reason, the scroll in your hand is now a duck. "
                    "It quacks once before running off down the corridor.",
                    libtcod.light_green
                )})

            break

    else:
        results.append({
            'consumed': False,
            'message': Message(
                "You don't see anyone to cast confusion on.",
                libtcod.yellow)})

    return results
