from random import randint
from .models import Player, Frame
from .constans import FRAMES, ALL_PINS


def roll1(pins, curr_fr, previuos_fr, old_fr, num_frs):
    if pins is None:
        pins = randint(0, ALL_PINS)
    # check
    curr_fr.roll1 = pins
    if pins == ALL_PINS:
        curr_fr.strike = True
    if old_fr and old_fr.score is None:
        old_fr.score = ALL_PINS + ALL_PINS + curr_fr.roll1
        old_fr.save()
    elif previuos_fr and previuos_fr.spare:
        previuos_fr.score = ALL_PINS + curr_fr.roll1
        previuos_fr.save()
    if num_frs != FRAMES and curr_fr.strike:
        Frame(player=curr_fr.player).save()
    return pins


def roll2(pins, curr_fr, previuos_fr, num_frs):
    available_pins = ALL_PINS - curr_fr.roll1
    if pins is None:
        pins = randint(0, available_pins)
    # check
    curr_fr.roll2 = pins
    if curr_fr.roll1 + curr_fr.roll2 == ALL_PINS:
        curr_fr.spare = True
    else:
        curr_fr.score = curr_fr.roll1 + curr_fr.roll2
    if num_frs != FRAMES:
        # create next frame for the same player
        Frame(player=curr_fr.player).save()
    if previuos_fr and previuos_fr.score is None:
        if previuos_fr.spare:
            previuos_fr.score = ALL_PINS + curr_fr.roll1
        elif previuos_fr.strike and (not curr_fr.strike):
            previuos_fr.score = ALL_PINS + curr_fr.roll1 +\
                                              curr_fr.roll2
            previuos_fr.save()
    return pins


def roll3(pins, curr_fr, previuos_fr):
    if curr_fr.roll2 == ALL_PINS or curr_fr.spare:
        available_pins = ALL_PINS
    else:
        available_pins = ALL_PINS - curr_fr.roll2
    if pins is None:
        pins = randint(0, available_pins)
    curr_fr.roll3 = pins
    curr_fr.score = curr_fr.roll1 + curr_fr.roll2 +\
        curr_fr.roll3
    if previuos_fr.score is None:
        previuos_fr.score = ALL_PINS + curr_fr.roll1 +\
            curr_fr.roll2
        previuos_fr.save()
    return pins


def create_player_and_frame():
    last_player = Player()
    last_player.save()
    frame = Frame(player=last_player)
    frame.save()
    return last_player, frame
