########################################
# This section can be commented out if
# imported into another script.
########################################

import json

# Open file and import data
f = open('./stats.json', 'r')
json_data = f.read()
f.close()
D = json.loads(json_data)

########################################


# Returns the average of a given stat for the given league
def find_avg_of_stat(league_name, stat_name):
    for league in D['Leagues']:
        # Find given league
        if league['League Name'] == league_name:
            # Set variables
            num_player = 0
            total_stat = 0
            # Iterate teams and players
            for team in league['Teams']:
                for player in team['Players']:
                    # Find stat for player
                    if stat_name in player:
                        total_stat += float(player[stat_name])
                        num_player += 1
            # Make sure not dividing by 0
            if num_player > 0:
                return total_stat/num_player
            # If the stat isn't present
            else:
                print 'Stat not found for players in league...'
                return 0
    # Will only reach here if the league isn't found
    print 'League not found...'
    return 0


########################################
# This section is for testing
########################################

def main():
    league = 'OHL'
    stat = 'Weight'
    print 'The average ' + stat + ' in the ' + league + ' is ' + str(find_avg_of_stat(league, stat))


if __name__ == '__main__':
    main()

########################################
