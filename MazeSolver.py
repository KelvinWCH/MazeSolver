"""
Kelvin Chung 


1. Generate a maze
2. Be able to find the shortest path from the start to any point of the maze
3. Save the current maze layout as file
4. Load the maze layout from file


Specifications:
1. Breadth-first search is used to find the shortest path
2. GUI is used as the medium for output/input

"""
import tkinter  # Import tkinter library for GUI creation
from tkinter import filedialog; #Import filedialog for file opening
import Maze  # Import the Maze class for maze generation and manipulation
import random  # Import random library

# Explanation: Updates the status label in the GUI and logs the message to the console
# Input parameters: newText (str) - the message to display on the status label
# Return value: None
def updateStatus(newText):
    statusLabel.config(text=newText)  # Update the text in the status label
    print(newText)  # Print the status to the console


# Explanation: Creates a new maze of a given size and updates the GUI to display it
# Input parameters: size (int) - the size of the maze; file (str or None) - the maze file or none
# Return value: None
def newMaze(size, file):
    global maze;
    maze = Maze.Maze(size, file)  # Create a new Maze object
    updateMazeDisplay(maze.get_maze())  # Update the GUI display with the new maze


# Explanation: Finds and highlights the shortest path in the maze from the current point to the end
# Input parameters: x (int) - the row index of the selected position; y (int) - the column index of the current position
# Return value: None
def findPath(x, y):
    global path;
    updateStatus(f"Finding path for: ({x}, {y})")  # Update the status with the selected point
    if path:  # If a path exists, reset the display
        for px, py in path:
            button = tkinter.Button(mazePanel, width=1, height=1, command=lambda row=px, col=py: findPath(row, col))
            button.grid(row=px + 1, column=py + 1, sticky="nsew")
    path = maze.findPath((x, y))  # Find a new path using the Maze class

    if not path:  # If no path is found update the status
        updateStatus("Visual error detected! Check console")
        print("Visual error detected! The point you clicked on is supposed to be a wall.")
        return

    for px, py in path:  # Highlight the path in red
        button = tkinter.Button(mazePanel, bg="red", width=1, height=1, command=lambda row=px, col=py: findPath(row, col))
        button.grid(row=px + 1, column=py + 1, sticky="nsew")

# Explanation: Updates the display of the maze in the GUI
# Input parameters: array - a 2D array representing the maze layout (0 for paths, 1 for walls)
# Return value: None
def updateMazeDisplay(array):
    updateStatus("Updating Maze")  # Update the status
    for children in mazePanel.winfo_children():  # Clear the existing display
        children.destroy()
    maze_size = len(array)  # Get the size of the maze

    # Add top border
    for i in range(maze_size + 2):
        border_label = tkinter.Label(mazePanel, bg="black", width=1, height=1)
        border_label.grid(row=0, column=i, sticky="nsew")

    # Add bottom border
    for i in range(maze_size + 2):
        border_label = tkinter.Label(mazePanel, bg="black", width=1, height=1)
        border_label.grid(row=maze_size + 1, column=i, sticky="nsew")

    # Add left and right borders
    for x in range(maze_size):
        tkinter.Label(mazePanel, bg="black", width=1, height=1).grid(row=x + 1, column=0, sticky="nsew")
        tkinter.Label(mazePanel, bg="black", width=1, height=1).grid(row=x + 1, column=maze_size + 1, sticky="nsew")

    # Fill the maze grid
    for x in range(maze_size):
        for y in range(maze_size):
            if array[x][y] == 0:  # If it's a path
                button = tkinter.Button(mazePanel, width=1, height=1, command=lambda row=x, col=y: findPath(row, col))
                button.grid(row=x + 1, column=y + 1, sticky="nsew", padx=0, pady=0)
            else:  # If it's a wall
                templabel = tkinter.Label(mazePanel, bg="green", width=1, height=1)
                templabel.grid(row=x + 1, column=y + 1, sticky="nsew", padx=0, pady=0)
    updateStatus("Done")  # Update the status when complete

# Explanation: Saves the current maze layout to a text file with a unique ID
# Input parameters: None
# Return value: None
def saveFile():
    randomID = random.randint(1, 100000)  # Generate a random ID for the filename (chances are slim if theres an existing ID)
    updateStatus(f"Saving file with ID: {randomID}")  # Update the status
    file = open(f"{randomID}_maze.txt", "w")  # Open a file for writing
    mazeArray = maze.get_maze()  # Get the maze array
    for i in range(len(mazeArray)):  # Write each row to the file
        for j in range(len(mazeArray)):
            file.write(str(mazeArray[i][j]))
        file.write("\n")
    file.close()  # Close the file

# Explanation: Opens a maze file and loads it into the GUI
# Input parameters: size (int) - the size of the maze
# Return value: None
def openFile(size):
    file_path = tkinter.filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"),)) #Prompt for file dialog 
    if not file_path:  # If no file is selected
        updateStatus("No file selected!")
        return
    try:
        file = open(file_path, "r")  # Open the selected file
        maze_data = file.read()  # Read the file
        file.close()  # Close the file
        newMaze(size, maze_data)  # Load the new maze
    except Exception as e:  # Handle errors
        print(f"An error occurred: {e}")

##Driver code 

# Create a new Maze object and initialize variables
maze = Maze.Maze(37, None)
path = []

# Initialize the main tkinter window
master = tkinter.Tk()
master.title("Maze Solver - Kelvin Chung (501-301-954)")  # Set the window title
master.geometry("1200x1000")  # Set the window size

# Create a panel for holding the maze content
mazePanel = tkinter.Frame(master, bg="light blue", width=1000, height=300)
mazePanel.pack(side="left", padx="15")
mazePanel.pack_propagate(False)

# Create a panel for control buttons
buttonPanel = tkinter.Frame(master, bg="light blue", width=200, height=700)
buttonPanel.pack(side="right", padx="15")
buttonPanel.grid_rowconfigure(0, weight=1)
buttonPanel.grid_columnconfigure(0, weight=1)

# Create a status label
statusLabel = tkinter.Label(master, bg="yellow", text="Welcome", font=("Arial", 15, "bold"))
statusLabel.place(x=700, y=10)

# Create a welcome label
welcomeLabel = tkinter.Label(master, text="Welcome, click on any path (grey squares in maze)\n on the maze to begin search!", font=("Arial", 15, "bold"))
welcomeLabel.place(x=700, y=40)


buttonFonts = ("Arial", 13, "bold")  # Common font used for buttons

# Add a "New Maze" button
newMazebutton = tkinter.Button(buttonPanel, text="New Maze", font=buttonFonts, bg="green", fg="white", width=20, height=2, command=lambda: newMaze(37, None))
newMazebutton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Add a "Print Maze" button
printMaze = tkinter.Button(buttonPanel, text="Print Maze", font=buttonFonts, bg="#5072A7", fg="white", width=20, height=2, command=lambda: maze.display_maze())
printMaze.grid(row=1, column=0, padx=5, pady=(5, 20), sticky="nsew")

# Add a "Save Maze File" button
saveMaze = tkinter.Button(buttonPanel, text="Save Maze File", font=buttonFonts, bg="#00308F", fg="white", width=20, height=2, command=lambda: saveFile())
saveMaze.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

# Add an "Open Maze File" button
openMaze = tkinter.Button(buttonPanel, text="Open Maze File", font=buttonFonts, bg="#00308F", fg="white", width=20, height=2, command=lambda: openFile(37))
openMaze.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

# Display the initial maze
updateMazeDisplay(maze.get_maze())

master.attributes("-topmost", True)  # Keep the window on top
master.resizable(0, 0)  # Disable window resizing
master.mainloop()  # Keeps tkinkter alive