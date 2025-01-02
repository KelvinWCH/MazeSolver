"""
DO NOT RUN THIS FILE. PLEASE RUN MazeSolver.PY

THIS IS A CLASS FILE. 

"""


import random  # Import random for shuffling directions during maze generation
from collections import deque  # Import deque for BFS

class Maze:
    # Explanation: Initializes the maze either by generating a new maze or loading a preset one.
    # Input parameters: size (int) - the size of the maze; preset (str or None) 
    # Return value: None
    def __init__(self, size, preset):
        if preset == None:  # If no preset is provided, generate a random maze
            self.size = size
            self.maze_array = [[1 for _ in range(size)] for _ in range(size)]  # Initialize all cells as walls
            self.__generate_maze(0, 0)  # Generate a random maze starting from (0, 0)
        else:  # If a preset is provided, parse it into a 2D array
            self.maze_array = []
            for i in preset.strip().split("\n"):
                row = list(map(int, i))  # Convert each line of text into a list of integers
                self.maze_array.append(row)
            self.size = len(self.maze_array)  # Set the size of the maze
        self.__breadthFirstSearch()  # Precompute BFS data for pathfinding

    # Explanation: Generates a maze using a recursive backtracking algorithm
    # Input parameters: x (int) - row index; y (int) - column index
    # Return value: None
    def __generate_maze(self, x, y):
        self.maze_array[x][y] = 0  # Mark the current cell as a path
        offset_directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Possible directions: up, down, left, right
        random.shuffle(offset_directions)  # Shuffle directions for random maze generation
        for dX, dY in offset_directions:  # Look ahead in each direction by two units
            newX, newY = x + dX, y + dY  # Calculate the new cell's coordinates
            if (0 <= newX < self.size) and (0 <= newY < self.size) and (self.maze_array[newX][newY] == 1):
                # If the new cell is within bounds and is a wall, convert to path
                self.maze_array[x + dX // 2][y + dY // 2] = 0  # Remove the wall between look ahead position and current position (in between);
                self.__generate_maze(newX, newY)  # Recursively generate the maze

    # Explanation: Performs BFS to precompute traversal order and parent nodes for pathfinding
    # Searches for possible path by checking in each direction, contrast to a regular BFS algorithm that looks into an adjacency list
    # Input parameters: None
    # Return value: None
    def __breadthFirstSearch(self):
        self.traversal_order = []  # List to store the order of traversal
        self.parents = {(0, 0): None}  # Dictionary to store the parent of each node
        queue = deque([(0, 0)])  # BFS queue starting at (0, 0)
        visited = set([(0, 0)])  # Set of visited nodes
        offset_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions

        while queue:  # While there are nodes to explore
            node_x, node_y = queue.popleft()  # Dequeue the current node
            self.traversal_order.append((node_x, node_y))  # Record traversal order
            for dX, dY in offset_directions:  # Explore each direction to determine if there is a possible path
                newX, newY = node_x + dX, node_y + dY  # Calculate new node coordinates
                if (0 <= newX < self.size and 0 <= newY < self.size):  # If within bounds
                    if (self.maze_array[newX][newY] == 0 and (newX, newY) not in visited):  # If path and unvisited
                        visited.add((newX, newY))  # Mark as visited
                        queue.append((newX, newY))  # Enqueue the new node
                        self.parents[(newX, newY)] = (node_x, node_y)  # Record the parent & child nord

    # Explanation: Finds the shortest path to a target cell using BFS data (parent data)
    # Input parameters: target (tuple) - the (row, column) coordinates of the target cell
    # Return value: List of tuples representing the path from start to target, or None if no path exists
    def findPath(self, target):
        if target not in self.parents:  # If the target is unreachable
            return None
        ans = []  # List to store the path
        current = target
        while current is not None:  # Trace back from the target to the start
            ans.append(current)
            current = self.parents.get(current)  # Get the parent of the current node
        return ans[::-1]  # Reverse the list to get the path from start to target

    # Explanation: Displays the maze in the console along with BFS data.
    # Input parameters: None
    # Return value: None
    def display_maze(self):
        print("--------------------------------------------------------------------------------------------------------------")
        print("Traversal Order:", self.traversal_order)  # Print the BFS traversal order
        print("--------------------------------------------------------------------------------------------------------------")
        print("Parent node-map:", self.parents)  # Print the BFS parent mapping
        print("--------------------------------------------------------------------------------------------------------------")
        for i in range(self.size):  # Iterate through each row of the maze
            for j in range(self.size):  # Iterate through each column
                if self.maze_array[i][j] == 0:  # If it's a path
                    print(" ", end="")
                else:  # If it's a wall
                    print("█", end="")
            print()  # Move to the next line after printing a row

    # Explanation: Returns the maze layout as a 2D array.
    # Input parameters: None
    # Return value: A 2D list representing the maze (0 for paths, 1 for walls)
    def get_maze(self):
        return self.maze_array

    # Explanation: Returns the BFS traversal order.
    # Input parameters: None
    # Return value: List of tuples representing the BFS traversal order
    def get_travesalOrder(self):
        return self.traversal_order

    # Explanation: Returns the BFS parent mapping.
    # Input parameters: None
    # Return value: A dictionary mapping each node to its parent node
    def get_parents(self):
        return self.parents
