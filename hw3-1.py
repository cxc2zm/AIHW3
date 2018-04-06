#Homework 3
#emh3fm, cxc2zm

import random


TEAM_NAME = "anxious_and_gay"
MEMBERS = ["emh3fm","cxc2zm"]




#returns average & std. dev.
def stats(arr):
    if (len(arr) < 2):
        return None

    total = 0
    for i in arr:
        total += arr[i]

    avg = total/len(arr)

    total = 0
    for i in arr:
        total += (arr[i]-avg)**2

    std_dev = sqrt(total/(len(arr)-1))

    return {
        "avg":avg, 
        "std_dev":std_dev
        }

    


# this is a test state function for you to drive the following test case with
# NOTE: you will receive this when the game playing program calls your get_move
"""
state = {
	"game":	"chicken",
	"opponent-name": "the_baddies",
	"team-code": "abc123",
	"prev-response-time": 0.5,
	"last-opponent-play": 0.71,
	"last-outcome": -10,
}
"""


# returns a random move (for sake of example)
def get_chicken_move(state):
    info = load_data() # info might be "{}" if first use, otherwise reads dictionary from your save file
    # example for storing previous response times

    

    if (state["prev-response-time"] is not None):
        info.setdefault("all_times",[]).append(state["prev-response-time"]) #add to the overall times array
        info.setdefault("opponents",{}).setdefault(state["opponent-name"],[]).append(state["prev-response-time"])
	
    save_data(info)

    prev_times_stats = stats(info["all_times"])

    #taking a very conservative first approach in case the reaction times are highly variable
    if (prev_times_stats is None):
        move = 10
    else:
        #the aim of this is to avoid crashes whenever possible, but still be reasonable with respect to reaction time
        move = prev_times_stats["avg"] + 2* prev_times_stats["std_dev"]

	return {
		"move": move,
		"team-code": state["team-code"],
	}






def get_move(state):
    if(state["game"] == "chicken"):
        return get_chicken_move(state)

    return get_connect_move(state)
