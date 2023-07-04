#!/usr/bin/env python3

# TODO add a mode that gives you very bingo-friendly racks only

import time
import random
import os
from collections import namedtuple

from scrabble_words import north_american_words
from word_frequencies import word_frequencies_300k

Puzzle = namedtuple('Puzzle', 'rack board_word solution')
GuessResult = namedtuple('GuessResult', 'correct eight_placement incorrect_remark')

# print(north_american_words[0])
# print(north_american_words[-1])
# print(word_frequencies_300k['it'])

def main(scrabble_words, frequency_list):
    scrabble_words_set = set(scrabble_words)
    scrabble_words_by_frequency = [  # TODO inline unused variable?
        word for word in frequency_list
        if word in scrabble_words_set
    ]
    bingos_by_frequency = [
        word for word in scrabble_words_by_frequency
        if len(word) in [7, 8]
    ]

    common_bingos = bingos_by_frequency[:5000]

    i = 1
    os.system('clear')
    while True:
        puzzle = make_puzzle(choose_solution(common_bingos), scrabble_words)
        print(i)
        print('Board:', puzzle.board_word.upper())
        print('Rack:', puzzle.rack.upper(), shuffles(puzzle.rack))
        guess = input('? ')

        while guess.startswith('.'):
            show_rack_subset(puzzle.rack, guess[1:])
            guess = input('? ')

        result = check_guess(guess, puzzle, scrabble_words)
        if result.correct:
            print('Correct!', result.eight_placement or '') # Bug Z5

            if guess != puzzle.solution:
                print('Another solution was', puzzle.solution.upper(), 'Z4')
        else:
            print('## Incorrect:', result.incorrect_remark)
            print('Answer was', puzzle.solution.upper(), 'Z4')

        print()
        input('Press enter to continue')
        os.system('clear')
        i += 1

    # Z4 = TODO Show placement if it's an eight

    # Bug Z5:
    # Board: BES
    # Rack: EEEORSV
    # ? oversees
    # Correct! OVER(S)EE
    # Another solution was OVERSEE Z4
    #
    # The intended answer was the seven, but I guessed the eight, and so check_eight_guess erroneously replaced S with (S)
    # Maybe don't fix this -- maybe this problem is solved by doing the GUI version

    # Another bug:
    # 1
    # Board: REI
    # Rack: ACEEHRS Z6
    # ? searcher
    # Correct! (R)ESEARCH
    # Another solution was RESEARCH Z4

def show_rack_subset(rack, exclude):
    rack = list(rack)
    for letter in exclude:
        try:
            rack.remove(letter)
        except ValueError:
            return
    print(''.join(sorted(rack)).upper())

def shuffles(rack):
    return 'Z6'
    # result = []
    # rack = list(rack)
    # for _ in range(5):
    #     random.shuffle(rack)
    #     result.append(''.join(rack).upper())
    # return ' '.join(result)


def check_guess(guess, puzzle, scrabble_words):
    # TODO Maybe check that all the tiles are available first
    # Maybe don't fix this -- maybe this problem is solved by doing the GUI version
    if not guess:
        return GuessResult(False, None, 'empty guess')
    if guess not in scrabble_words:
        return GuessResult(False, None, 'not in dictionary')

    if len(guess) == 7:
        if sorted(guess) == list(puzzle.rack):
            return GuessResult(True, None, None)
        else:
            return GuessResult(False, None, 'Z1')
    elif len(guess) == 8:
        return check_eight_guess(guess, puzzle)
    else:
        return GuessResult(False, None, 'guess length must be 7 or 8')

def check_eight_guess(guess, puzzle):
    # Dictionary check already done in check_guess(), so no need to do it here
    for letter in sorted(set(puzzle.board_word)):
        if sorted(guess) == sorted(puzzle.rack + letter):
            placement = (
                puzzle.solution
                    .replace(letter, f'({letter})', 1)
                    .upper()
            )
            return GuessResult(True, placement, None)
    return GuessResult(False, None, 'Z3')

def choose_solution(common_bingos):

    if random.random() < 0.5:
        common_bingos = [
            w for w in common_bingos
            if (
                False
                or w.endswith('er')  # or 'ier'
                or w.endswith('est')  # or 'iest'
                or w.endswith('es')  # or 'ies'
                or w.endswith('ed')  # etc
                or w.endswith('ers')
                or w.endswith('ing')
                or w.endswith('ings')
                or w.startswith('re')
                or w.startswith('de')
            )
        ]

    # common_bingos = [
    #     w for w in common_bingos
    #     if w.endswith('iest')
    # ]

    sevens = [w for w in common_bingos if len(w) == 7]
    eights = [w for w in common_bingos if len(w) == 8]
    # if True:
    if random.choice([True, False]):
        return random.choice(sevens)
    else:
        return random.choice(eights)

def make_puzzle(solution, scrabble_words):
    if len(solution) == 7:
        rack = ''.join(sorted(solution))
        board_word = random.choice([w for w in scrabble_words if len(w) == 3])
        return Puzzle(rack, board_word, solution)
    elif len(solution) == 8:
        return make_eight_puzzle(solution, scrabble_words)

def make_eight_puzzle(solution, scrabble_words):
    def get_board_word(letter):
        # TODO Is this necessary? Check if there's a three-letter word for
        # every letter of the alphabet, etc (Hmm, maybe that's not sufficient
        # though: Maybe there aren't that many for some letters, so you'd start
        # seeing the same words over and over, and that'd be a giveaway. Maybe
        # four-letter words works better or something like that
        words = []
        n = 3
        while not words:
            words = [word for word in scrabble_words if len(word) == n and letter in word]
            n += 1
        return random.choice(words)

    assert len(solution) == 8

    rack = list(solution)
    random.shuffle(rack)
    intersection_letter = rack.pop()
    board_word = get_board_word(intersection_letter)
    # board_word = random.choice([
    #     w for w in scrabble_words
    #     if intersection_letter in w
    # ])

    return Puzzle(''.join(sorted(rack)), board_word, solution)

main(north_american_words, word_frequencies_300k)
