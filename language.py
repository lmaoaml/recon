import random, copy

class Language:
	def __init__(self, constraints, ranking=None, name='1'):
		self.constraints = constraints
		# Ranking: digraph stored as adjacency list
		self.c = len(constraints)
		if not ranking:
			self.ranking = {constraint:[] for constraint in self.constraints}
		else:
			self.ranking = ranking
		self.__name__ = name
		self.normalized_ranking = []
		self.length = 0.0

	def __str__(self):
		return self.__name__

	def __repr__(self):
		return self.__name__

	def randomize_ranking(self):
		# Fully, randomly rank the constraint set
		random.shuffle(self.constraints)
		for i in range(self.c - 1):
			self.ranking[self.constraints[i]].append(self.constraints[i+1])

	def normalize_ranking(self):
		sorted_constraints = sorted(self.constraints)
		# Get pairwise comparison vector; 1 if a >> b, -1 if b >> a, 0 if no relation
		pairwise_ranking = []
		for con1 in sorted_constraints:
			for con2 in sorted_constraints:
				if con2 in self.ranking[con1]:
					pairwise_ranking.append(1.0)
				elif con1 in self.ranking[con2]:
					pairwise_ranking.append(-1.0)
				else:
					pairwise_ranking.append(0.0)
		# Get length of vector: square root of sum of squares of values
		for p in pairwise_ranking:
			self.length += p**2
		self.length **= .5
		# Divide each entry in pairwise vector by the length of the vector
		self.normalized_ranking = [p/self.length for p in pairwise_ranking]

	def tweak_ranking(self):
		# Randomly modify ranking
		r = random.random()
		if r < .5:
			# Remove a link
			r1 = random.randint(0, self.c - 1)
			constraint = self.constraints[r1]
			if self.ranking[constraint]:
				r2 = random.randint(0, len(self.ranking[constraint]) - 1)
				self.ranking[constraint].pop(r2)
		else:
			# Add a link
			r1 = random.randint(0, self.c - 1)
			r2 = random.randint(0, self.c - 1)
			if r1 != r2: # constraints cannot dominate themselves
				con1 = self.constraints[r1]
				con2 = self.constraints[r2]
				if con2 not in self.ranking[con1]:
					# make sure the new link would not result in a loop
					tempranking = copy.deepcopy(self.ranking)
					tempranking[con1].append(con2)
					if not self.check_for_loops(tempranking):
						self.ranking[con1].append(con2)

	def check_for_loops(self,G):
		# checks a graph for loops; returns True if a loop is found, else False
		color = {u:'white' for u in G}
		found_cycle = False
		for u in G:
			if color[u] == 'white':
				self.dfs_visit(G, u, color, found_cycle)
			if found_cycle:
				break
		return found_cycle
	
	def dfs_visit(self, G, u, color, found_cycle):
		# helper function for check_for_loops
		if found_cycle:
			return
		color[u] = 'gray'
		for v in G[u]:
			if color[v] == 'gray':
				found_cycle = True
				return
			if color[v] == 'white':
				self.dfs_visit(G, v, color, found_cycle)
		color[u] = 'black'
