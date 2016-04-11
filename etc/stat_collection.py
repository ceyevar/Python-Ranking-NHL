import os
import json


def main():

    # Gets files from teams directory
    team_files = os.listdir('./data/teams/')

    D = {}
    D['Leagues'] = []

    # Iterate through all files
    for num in range(len(team_files)):
        # Read in file
        team_file = open('./data/teams/' + team_files[num], 'r')

        # Get league name
        filename = os.path.basename(team_file.name)
        league = filename[:-4]

        # Create league object
        L = {}
        L['League Name'] = league
        L['Teams'] = []

        # Get headers for keys
        team_headers = team_file.readline()[:-1].split(',')

        # Get the team stats
        for line in team_file:
            team_index = 0
            team_name = ''
            T = {}
            team_data = line[:-1].split(',')
            for team_stat in team_data:
                if team_headers[team_index] == 'Team Name':
                    team_name = team_stat
                T[team_headers[team_index]] = team_stat
                team_index += 1

            # Get player stats for team
            T['Players'] = []
            player_file = open('./data/players/' + league + "_players.csv", 'r')
            player_headers = player_file.readline()[:-1].split(',')
            for row in player_file:
                player_data = row.split(',')
                if team_name in player_data:
                    player_index = 0
                    P = {}
                    player_data = row[:-1].split(',')
                    for player_stat in player_data:
                        # Makes Last, First convention for player name
                        if player_headers[player_index] == 'Name':
                            names = player_stat.split()
                            player_stat = names[1] + ', ' + names[0]
                        P[player_headers[player_index]] = player_stat
                        player_index += 1

                    # Append player data to team
                    T['Players'].append(P)

            # Append team data to league
            L['Teams'].append(T)

        # Append league data to main object
        D['Leagues'].append(L)

    # Create json object
    json_data = json.dumps(D)

    # Dump json into file
    output = open('./stats.json', 'w')
    output.write(json_data)

if __name__ == '__main__':
    main()
