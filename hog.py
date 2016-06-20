"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    y = num_rolls
    score = 0
    while y != 0:
        a = dice()
        if a == 1:
            a = dice()
            return 1
        else:
            score = score + a
        y = y - 1
    return score

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    y = num_rolls
    b = opponent_score
    if y == 0:
        return abs((b//10) - (b%10)) + 1
    else:
        return roll_dice(y, dice)

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    a = score
    b = opponent_score
    total = (a + b) % 7
    if total == 0:
        return four_sided
    else:
        return six_sided


def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    # The buggy code is below:
    if bid0 == bid1:
        return goal, goal, 0
    if bid0 == bid1 - 5:
        return 0, 10, 1
    if bid0 == bid1 + 5:
        return 10, 0, 0
    if bid1 > bid0:
        return bid1, bid0, 1
    else:
        return bid1, bid0, 0

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    temp = 0
    while score0 < 100 and score1 < 100:
        if who == 0:
            score0 = score0 + take_turn(strategy0(score0, score1), score1, select_dice(score0, score1))
            if score0 == 2*score1 or score1 == 2*score0:
                temp = score1
                score1 = score0
                score0 = temp
        else:
            score1 = score1 + take_turn(strategy1(score1, score0), score0, select_dice(score1, score0))
            if score0 == 2*score1 or score1 == 2*score0:
                temp = score1
                score1 = score0
                score0 = temp
        who = other(who)
    return score0, score1  # You may want to change this line.

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def avg(*args):
        a = 0
        result = 0
        while a < num_samples:
            result = result + fn(*args)
            a = a +1
        return result / num_samples
    return avg

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    a = 1
    b = 0
    x = 0
    while a <= 10:
        s = make_averaged(roll_dice)(a,dice)
        if s > b:
            b = s
            x = a
        a = a + 1
    return x

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    b = opponent_score
    a = abs((b//10) - (b%10)) + 1
    if a >= margin:
        return 0
    else:
        return num_rolls

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    b = opponent_score
    a = abs((b//10) - (b%10)) + 1
    t = score + a
    if b == 2*t:
        temp = b
        b = t
        t = temp
        return 0
    elif t == 2*b :
        return num_rolls
    elif a >= margin:
        return 0
    else:
        return num_rolls


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    The strategy takes expected score of our opponent. Then mainIf expected score:
        1. Equals to half of our opponent score, then take 0.
        2. Difference oppenent score and our score less than 21 then take 7.
        3. Score greater than 90, play any number between 1 to 3.
        4. Score greater than 85, take 4.
        5. Score greater than 75, take 5.
        6. The rest we take into account any possibilites that potentially optimizes our score.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    margin = 8
    calculation_score = 1 + abs(opponent_score // 10 - opponent_score % 10)
    expected_score = score + calculation_score
    difference = abs(score - opponent_score)
    if expected_score * 2 == opponent_score:
        return 0
    if (score + 1) * 2 == opponent_score:
        return 10
    if (expected_score + opponent_score) % 7 == 0:
        return 0
    if (score + opponent_score) % 7 == 0:
        if (score + 5) * 2 == opponent_score:
            return 2 
        if score > 95:
            return 2
        if score > 90:
            return 3
        return 3
    if (score + 7) * 2 == opponent_score:
        return 2
    if (score + 10) * 2 == opponent_score:
        return 3
    if (score + 14) * 2 == opponent_score:
        return 4
    if score > 95:
        return 2
    if score > 90:
        return 3
    if (calculation_score >= margin):
        return 0
    if score > 85:
        return 4
    if score > 75:
        return 5
    if opponent_score - score >= 20:
        return 7
    return 6


def avg():  
    i=0
    result=0
    n=50

    while(i<n):


        result=(result+average_win_rate(final_strategy))
        i=i+1

    return result/n






##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
