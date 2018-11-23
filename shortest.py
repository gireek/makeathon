import collections
num_to_indx = {1: (3, 1), 2: (2, 1), 3: (1, 1), 4: (0, 1), 5: (0, 2), 6: (0, 3), 7: (1, 3), 8: (2, 3), 9: (3, 3), 10: (3, 2)}
indx_to_num = {(3, 1): 1, (2, 1): 2, (1, 1): 3, (0, 1): 4, (0, 2): 5, (0, 3): 6, (1, 3): 7, (2, 3): 8, (3, 3): 9, (3, 2): 10}


class Queue:
	def __init__(self):
		self.elements = collections.deque()

	def empty(self):
		return len(self.elements) == 0

	def put(self, x):
		self.elements.append(x)

	def get(self):
		return self.elements.popleft()


class Grid:
	def __init__(self, ncols, nrows , obstacles):
		self.nrows = nrows
		self.ncols = ncols
		self.obstacles = obstacles
		self.path_mat = [[0 for x in range(self.nrows)] for y in range(self.ncols)]

	def inside(self, id):
		(x, y) = id
		return 0 <= x < self.ncols and 0 <= y < self.nrows

	def not_obs(self, id):
		return id not in self.obstacles

	def neighbors(self, id):
		(x, y) = id
		res = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
		res = filter(self.inside, res)
		res = filter(self.not_obs, res)
		return res


def bfs(graph, start):
	frontier = Queue()
	frontier.put(start)
	came_from = {}
	came_from[start] = None
	while not frontier.empty():
		current = frontier.get()
		for next in graph.neighbors(current):
			if next not in came_from:
				frontier.put(next)
				came_from[next] = current
	return came_from


def draw_tile(graph, id, style):
	r = "."
	if 'point_to' in style and style['point_to'].get(id, None) is not None:
		(x1, y1) = id
		(x2, y2) = style['point_to'][id]
		if x2 == x1 + 1: r = "v"
		if x2 == x1 - 1: r = "^"
		if y2 == y1 + 1: r = ">"
		if y2 == y1 - 1: r = "<"
	if 'goal' in style and id == style['goal']:
		r = "Z"
	if id in graph.obstacles:
		r = "#"
	return r


def draw_grid(graph, **style):
	for x in range(graph.ncols):
		for y in range(graph.nrows):
			character = draw_tile(graph, (x, y), style)
			graph.path_mat[x][y] = character
	print(graph.path_mat)


def go(graph, start, end):
	path_q = [start]
	curr = num_to_indx[start]
	while(indx_to_num[curr]!= (end)):
		if (graph.path_mat[curr[0]][curr[1]]=="^"):
			path_q.append(indx_to_num[(curr[0] - 1, curr[1])])
			curr = (curr[0]-1 , curr[1])
		elif (graph.path_mat[curr[0]][curr[1]] == ">"):
			path_q.append(indx_to_num[(curr[0], curr[1] + 1)])
			curr = (curr[0], curr[1] + 1)
		elif (graph.path_mat[curr[0]][curr[1]] == "<"):
			path_q.append(indx_to_num[(curr[0], curr[1] - 1)])
			curr = (curr[0], curr[1] - 1)
		elif (graph.path_mat[curr[0]][curr[1]] == "v"):
			path_q.append(indx_to_num[(curr[0] + 1, curr[1])])
			curr = (curr[0] + 1, curr[1])
	return path_q


def path(nrows, ncols, obs, start, end):
	g = Grid(nrows, ncols, obs)
	parents = bfs(g, num_to_indx[end])
	draw_grid(g, point_to=parents, goal=num_to_indx[end])
	return go(g, start, end)


print(path(4, 4, [(0, 0), (1, 0), (2, 0), (3, 0), (1, 2), (2, 2)], 2, 6))