import json, numbers, math, random, numpy, operator


# Global value for all stat names that are present in every player
stats = []
ignore_these = ['GP', '+/-', 'Face-offs Taken', 'Age', 'Weight']
# Main function
def cluster(P, I, K, ignored):

	collect_stat_names(P, ignored)

	# Get random seeds
	seeds = random_seeds(P, K)

	# Clustering Iterations
	for num in range(I):
		old_seeds = seeds
		clusters = calculate_closest_seed(P, seeds)
		seeds = calculate_new_seeds(clusters, P)

	# Turns the indices into actual players
	R = {}
	for k,v in clusters.iteritems():
		if k not in R:
			R[k] = []
		for index in v:
			R[k].append(P[index])
	return R


# Coming up with random seeds
def random_seeds(players, clusters):
	seeds = []
	for i in range(clusters):
		seeds.append(calculate_vector(players[random.randint(0, len(players) - 1)]))
	return seeds


# Finding the closest seed given the TF-IDF
def calculate_closest_seed(players, seeds):
	clusters = {}
	for num in range(len(seeds)):
		clusters[num] = []
	for player in players:
		a = numpy.array(calculate_vector(player))
		closest = 0
		distance = float("inf")
		for seed in seeds:
			b = numpy.array(seed)
			euclidean = numpy.linalg.norm(a - b)
			if distance > euclidean:
				distance = euclidean
				closest = seeds.index(seed)
		clusters[closest].append(players.index(player))
	return clusters


# Calculating center of each cluster
def calculate_new_seeds(clusters, players):
	centroids = []
	for k,v in clusters.iteritems():
		a = numpy.zeros(len(stats))
		for index in v:
			b = numpy.array(calculate_vector(players[index]))
			a += b
		if len(v) > 0:
			a = a/len(v)
			centroids.append(a.tolist())
	return centroids


# Finds all stat names that are present in every player
#I edited this only to include relevant stats, removed stats like weight and height
def collect_stat_names(players, ignored):
	names = {}
	for player in players:
		for k,v in player.iteritems():
			if k in ignored:
				if k not in names:
					names[k] = 0
				names[k] += 1
	for k,v in names.iteritems():
		if v == len(players) and isinstance(players[0][k], numbers.Number) and k != 'id' and k != 'Number':
			stats.append(k)


# Turn player dictionary into vector
def calculate_vector(player):
	vector = []
	for name in stats:
		vector.append(player[name])
	return vector


if __name__ == '__main__':

	f = open('../stats.json', 'r')
	D = json.load(f)
	f.close()

	Players = []

	for league in D['Leagues']:
		for team in league['Teams']:
			for player in team['Players']:
				Players.append(player)

	C = cluster(Players, 10, 6, ignore_these)

	# Printing to screen
	for k,v in C.iteritems():
		print "Cluster " + str(k + 1) + ":"
		for player in v:
			print player["Position"]
		print '\n'


