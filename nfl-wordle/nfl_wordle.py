import csv
import random
from collections import defaultdict

players_in_csv = 706
player_to_guess_dict = {}
score_history = defaultdict(list)
max_guesses = 6

divisions = {
    "nfc_east": ["NYG","DAL","PHI","WAS"],
    "nfc_north": ["GNB","CHI","DET","MIN"],
    "nfc_south": ["TAM","NOR","CAR","ATL"],
    "nfc_west": ["LAR","ARI","SFO","SEA"],
    "afc_east": ["BUF","NWE","MIA","NYJ"],
    "afc_north": ["CLE","PIT","CIN","BAL"],
    "afc_south": ["IND","TEN","HOU","JAX"],
    "afc_west": ["LAC","KAN","LVR","DEN"]
}

offense = ["QB","WR","RB","FB","G","C","RG","TE","T","LT","RT","OL"]
defense = ["LB","DT","DE","CB","S","NT","DB","DL"]

def load_players():
    converted_dict = {}
    with open("nfl-wordle/players2021.csv", newline='') as csvfile:
            nfl_players = csv.DictReader(csvfile)
            for row in nfl_players:
                name = row["Player"]
                team = ("team",row["Team"])
                position = ("position",row["Pos"])
                age = ("age",row["Age"])
                rank = ("rank",row["Rk"])
                converted_dict[name] = [team,position,age,rank]
            return converted_dict

def get_player_attributes(player_name,dict):
    player_key = dict[player_name]
    for attribute in player_key:
        if attribute[0] == "team":
            players_team = attribute[1]
        elif attribute[0] == "position":
            players_pos = attribute[1]
        elif attribute[0] == "age":
            players_age = attribute[1]
        elif attribute[0] == "rank":
            player_rank = attribute[1]
    return {
        "name": player_name, 
        "team": players_team,
        "position": players_pos,
        "age": players_age,
        "rank": player_rank
        }

def get_random_player(dict):
    # random_player = []
    random_row = str(random.randint(1,players_in_csv))
    for player in dict:
        player_attributes = get_player_attributes(player, dict)
        rank = player_attributes.get("rank")
        if rank == random_row:
            return player_attributes

# if the name isnt a match, this will get and process the results
def process_guess(guess_dict, dict_to_compare):
    # loop through keys and compare guessed dict and player dict
    guesses_list = []  
    # check names
    if guess_dict["name"] == dict_to_compare["name"]:
        guesses_list.append("green")
    else:
        # elif first letter of first name or last name is correct
        name_result = "grey"
        # get letter both names start with
        split_guess_name = guess_dict["name"].split()
        split_compare_name = dict_to_compare["name"].split()
        guess_first_letters = (split_guess_name[0][0],split_guess_name[1][0])
        compare_first_letters = (split_compare_name[0][0],split_compare_name[1][0])
        for letter in guess_first_letters:
            if letter in compare_first_letters:
                name_result = "yellow"
        guesses_list.append(name_result)
    #team check
    if guess_dict["team"] == dict_to_compare["team"]:
        guesses_list.append("green")
    else:
        for teams in divisions.values():
            result = "grey"
            if guess_dict["team"] in teams and dict_to_compare["team"] in teams:
                result = "yellow"
        guesses_list.append(result)
    # position check 
    if guess_dict["position"] == dict_to_compare["position"]:
        guesses_list.append("green")
    else:
         # if both are offensive players
        if guess_dict["position"] in offense and dict_to_compare["position"] in offense:
            guesses_list.append("yellow")
        # if both are defensive players
        elif guess_dict["position"] in defense and dict_to_compare["position"] in defense:
            guesses_list.append("yellow")
        else:
            guesses_list.append("grey")
    # age check
    if guess_dict["age"] == dict_to_compare["age"]:
        guesses_list.append("green")
    else:
        # if age is 2 
        guess_age  = int(guess_dict["age"])
        compare_age = int(dict_to_compare["age"])
        age_difference = abs(guess_age - compare_age)
        if age_difference <= 2:
            guesses_list.append("yellow")
        else:
            guesses_list.append("grey")
    # get rows in score history
    guess_count = len(score_history) + 1
    score_history[guess_count].append(guesses_list)
    print("   Name   Team    Position    Age")
    print_score()
        
def search_player(guess, dict):
    player_found = False
    while player_found == False:
        for player_name in dict:
            if guess.lower() in player_name.lower():
                player_found_dict = get_player_attributes(player_name,dict)
                player_found = True
                # remove rank bc it's confusing
                player_found_dict.pop("rank")
                print("Player found:", player_found_dict)
                # print(player_found_dict.values())
                return player_found_dict
        guess = input("Player not found! Guess again: ")

def print_score():
    for guess_row in score_history.values():
        print(guess_row)

def play_game():
    # convert the csv to the dict
    player_dict = load_players()
    # select random player from csv
    player_to_guess_dict = get_random_player(player_dict)
    # Print answer for testing purposes
    # print(player_to_guess_dict)
    # set bool to false while still guessing
    player_has_been_guessed = False
    # while the score history has less rows than max guesses
    while len(score_history) < max_guesses:
        if player_has_been_guessed == False:
            guess_input = input("Enter guess #: ")
            guess_found = search_player(guess_input,player_dict)
            # check if the name is right 
            process_guess(guess_found,player_to_guess_dict)
            if guess_found["name"] == player_to_guess_dict.get("name"):
                print("You won!")
                # print_score()
                player_has_been_guessed = True
                break
            else:
                guesses_left = max_guesses - len(score_history)
                print(str(guesses_left) + " guesses left!")
            # if not correct, then analyze the guesses
    if player_has_been_guessed == False:
        print("Sorry, you're out of guesses. The player was :" )
        print(player_to_guess_dict)

play_game()