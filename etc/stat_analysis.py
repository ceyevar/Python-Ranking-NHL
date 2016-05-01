import json
import operator


def main():
    f = open('../stats.json', 'r')
    json_data = f.read()

    D = json.loads(json_data)

    R = {}

    for league in D['Leagues']:
        PS = {}

        for team in league['Teams']:
            for player in team['Players']:
                if player['Shoots'] in PS:
                    PS[player['Shoots']] += 1
                else:
                    PS[player['Shoots']] = 0

        R[league['League Name']] = max(PS.iteritems(), key=operator.itemgetter(1))[0]

    print json.dumps(R)


if __name__ == '__main__':
    main()
