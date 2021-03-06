import os
import json


def import_data():

    # Gets files from teams directory
    team_files = os.listdir('./data/teams/')

    D = {}
    D['Leagues'] = []

    team_id = 1
    player_id = 1

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
        team_headers = team_file.readline().rstrip().split(',')

        # Get the team stats
        for line in team_file:
            team_index = 0
            team_name = ''
            T = {}
            T["id"] = team_id
            team_data = line.rstrip().split(',')
            for team_stat in team_data:
                if team_headers[team_index] == 'Team Name':
                    team_name = team_stat
                T[team_headers[team_index]] = team_stat
                team_index += 1

            # Get player stats for team
            T['Players'] = []
            player_file = open('./data/players/' + league + "_players.csv", 'r')
            player_headers = player_file.readline().rstrip().split(',')
            for row in player_file:
                player_data = row.split(',')
                if team_name in player_data:
                    player_index = 0
                    P = {}
                    P["id"] = player_id
                    player_data = row.rstrip().split(',')
                    for player_stat in player_data:
                        # Makes Last, First convention for player name
                        if player_headers[player_index] == 'Name':
                            names = player_stat.split()
                            player_stat = names[1] + ', ' + names[0]
                        P[player_headers[player_index]] = player_stat
                        player_index += 1

                    # Append player data to team
                    T['Players'].append(P)
                    player_id += 1

            # Append team data to league
            L['Teams'].append(T)
            team_id += 1

        # Append league data to main object
        D['Leagues'].append(L)

    # Create json object
    json_data = json.dumps(D)

    # Dump json into file
    output = open('./stats.json', 'w')
    output.write(json_data)

if __name__ == '__main__':
    import_data()
