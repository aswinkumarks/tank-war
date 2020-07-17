import pygame
import settings


def distance(node,cor):
	return abs(node.x - cor[0]) + abs(node.y - cor[1])

def checkCollision(x,y):
	# x, y = x*settings.TILE_SIZE, y*settings.TILE_SIZE
	# x , y = x//settings.TILE_SIZE, y//settings.TILE_SIZE
	pos_rect = pygame.Rect(x,y,48,48)
	collision = False
	for obstacle in settings.allObstacles:
		if pos_rect.colliderect(obstacle.rect):
			collision = True
			break

	return not collision

	# if grid[x][y]:
	# 	return False
	# else:
	# 	return True

# max_x = (settings.HEIGHT // settings.TILE_SIZE) - 1
# max_y = (settings.WIDTH // settings.TILE_SIZE) - 1

max_x = settings.HEIGHT - settings.TILE_SIZE
max_y = settings.WIDTH - settings.TILE_SIZE

def inRange(x,y):
	if x >= 0 and y >= 0 and x <= max_x and y <= max_y:
		return True
	else:
		return False

class Node:
	parent  = None
	value = -1
	curr_dist = 0

	def __init__(self,x,y,action="IDLE"):
		self.x = x
		self.y = y
		self.action = action
		
	def findSuccessors(self):
		x, y = self.x, self.y
		successors = []
		speed = 3

		# if inRange(x-speed,y-speed) and checkCollision(x-speed,y-speed):
		# 	successors.append(Node(x-speed,y-speed))

		if inRange(x-speed,y) and checkCollision(x-speed,y):
			successors.append(Node(x-speed,y,"LEFT"))

		# if inRange(x-speed,y+speed) and checkCollision(x-speed,y+speed):
		# 	successors.append(Node(x-speed,y+speed))

		if inRange(x,y-speed) and checkCollision(x,y-speed):
			successors.append(Node(x,y-speed,"UP"))

		if inRange(x,y+speed) and checkCollision(x,y+speed):
			successors.append(Node(x,y+speed,"DOWN"))

		# if inRange(x+speed,y-speed) and checkCollision(x+speed,y-speed):
		# 	successors.append(Node(x+speed,y-speed))

		if inRange(x+speed,y) and checkCollision(x+speed,y):
			successors.append(Node(x+speed,y,"RIGHT"))

		# if inRange(x+speed,y+speed) and checkCollision(x+speed,y+speed):
		# 	successors.append(Node(x+speed,y+speed))

		for node in successors:
			node.curr_dist = self.curr_dist + speed
			node.parent = self

		return successors

		

def tracePath(node):
	actions = []
	while node.parent != None:
		actions.append(node.action)
		node = node.parent

	return actions

class AstarSearch:

	@staticmethod
	def findPath(curr_cor,target_cor):
		open_nodes = []
		closed_nodes = []

		start_node = Node(curr_cor[0], curr_cor[1])
		start_node.value = 0
		open_nodes.append(start_node)

		while len(open_nodes) != 0:
			min_node = min(open_nodes,key=lambda node:node.value)
			open_nodes.remove(min_node)
			successors = min_node.findSuccessors()

			for successor in successors:
				dist = distance(successor,target_cor)
				if dist < 20:
					# print("Target found")
					actions = tracePath(successor)
					return actions

				successor.value = min_node.curr_dist + dist

				found = False
				for node in open_nodes:
					if node.x == successor.x and node.y == successor.y \
					   and node.value <= successor.value:
					   found = True
					   break

				if found:
					continue

				found = False
				for node in closed_nodes:
					if node.x == successor.x and node.y == successor.y \
					   and node.value <= successor.value:
					   found = True
					   break

				if found:
					continue
				else:
					open_nodes.append(successor)

			closed_nodes.append(min_node)

		return []

# print(AstarSearch.findPath((4,4),(0,14)))