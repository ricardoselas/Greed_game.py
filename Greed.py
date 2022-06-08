import random

DEFAULT_DICE_NUMBER = 5
NB_POINTS_TO_START = 300

class Player(object):
    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        if self.name:
            return "'{0}'".format(self.name)
        else:
            return "'Anonymous player'"

    def __repr__(self):
        return self.__str__()


def roll(n):
    return [random.randint(1, 6) for _ in range(n)]


def score(dice):
    result = 0
    if len(dice) <= 5:
        dice_dict = dict((i, dice.count(i)) for i in dice)
        if dice_dict.get(1) >= 3:
            result += 1000
            dice_dict[1] -= 3
        for number in dice_dict:
            if dice_dict.get(number) >= 3:
                result += number * 100
                dice_dict[number] -= 3
        if 1 in dice_dict:
            result += dice_dict[1] * 100
            dice_dict[1] = 0
        if 5 in dice_dict:
            result += dice_dict[5] * 50
            dice_dict[5] = 0

    remaining_dice = len([die for die in dice_dict.keys() if dice_dict[die] != 0])
    remaining_dice = remaining_dice if remaining_dice else DEFAULT_DICE_NUMBER
    return result, remaining_dice


def print_turn(player, score):
    print "\n------------------------------------------\nStarting turn of {0} [Score: {1}]\n".format(player, score)


def ask_yes_no_question(prompt):
    user_input = raw_input(prompt)
    return user_input.upper() in ["Y", "YES"]


def ask_roll_again(player):
    return ask_yes_no_question("\n{0}, will you roll again? (y/n): ".format(player))


def turn_score(player):
    total_score = 0
    nb_dice = DEFAULT_DICE_NUMBER

    while True:
        dice = roll(nb_dice)
        print "\n{0} rolls the dice and gets {1}.".format(player, dice)
        rolling_score, nb_dice = score(dice)
        if rolling_score == 0:
            if total_score:
                print "That's a zero-point roll, you lost your turn and all your won points in this turn."
            else:
                print "That's a zero-point roll, you cannot roll again in this turn."
            return 0
        else:
            print "That's a score of {0} points and {1} non-scoring {2} can be rolled again.".format(rolling_score, nb_dice, "die" if nb_dice == 1 else "dice")
            if total_score + rolling_score >= NB_POINTS_TO_START:
                total_score += rolling_score
                print "Since you reached more than {0} points this turn, your turn score is now {1}".format(NB_POINTS_TO_START, total_score)
            else:
                total_score = rolling_score
                print "Your turn score is less than {0} points, so now it's just the rolling score, {1} points.".format(NB_POINTS_TO_START, total_score)
            if not ask_roll_again(player):
                return total_score


def get_winner(players_scores):
    return max(players_scores, key = players_scores.get)


def play_game(players, goal = 3000):
    if len(players) < 2:
        raise "This game is for 2 or more players."
    players_scores = dict((player, 0) for player in players)
    number_of_players = len(players_scores)
    players = [player for player in players_scores.keys()]

    first_player_to_reach_final_round = None
    turn = random.randint(0, len(players)-1)

    while turn != first_player_to_reach_final_round:
        player = players[turn]
        score = players_scores[player]
        print_turn(player, score)
        won_score = turn_score(player)
        players_scores[player] += won_score
        print "{0} has won {1} points (total {2}).".format(player, won_score, players_scores[player])
        if players_scores[player] >= goal:
            if first_player_to_reach_final_round is None:
                first_player_to_reach_final_round = turn
            print "{0} has reached over {1} points. Next round will be the last round.".format(player, goal)
            print "\n\nLAST ROUND!!! Let's see who wins!"
        turn = (turn + 1) % number_of_players

    winner = get_winner(players_scores)
    print "\n\nCongratulations, {0}! You have won the Greed Game!".format(winner)


player1 = Player("Player 1")
player2 = Player("Player 2")
play_game([player1, player2], 1500)