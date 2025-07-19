# Question 2 
# Sava Josè Maria 
import timeit  # For measuring execution time
import heapq   # For priority queue implementation in A* algorithm

class EightPuzzle:
    """
    Class to represent and solve the 8-puzzle using A* search algorithm.
    The puzzle is a 3x3 grid with tiles numbered 1-8 and one blank space (0).
    """
    
    def __init__(self, start_state, goal_state):
        """
        Initialize the 8-puzzle with start and goal states.
        
        Args:
            start_state: List of 9 integers representing initial puzzle configuration
            goal_state: List of 9 integers representing target puzzle configuration
        """
        self.start_state = tuple(start_state)  # Convert to tuple for immutability
        self.goal_state = tuple(goal_state)    # Convert to tuple for immutability
        self.rows = 3                          # Number of rows in the puzzle
        self.cols = 3                          # Number of columns in the puzzle
        self.actions = ['L', 'R', 'U', 'D']    # Possible moves: Left, Right, Up, Down

    def get_blank_pos(self, state):
        """
        Find the position (index) of the blank tile (0) in the current state.
        
        Args:
            state: Tuple representing current puzzle configuration
            
        Returns:
            Integer index (0-8) where the blank tile is located
        """
        return state.index(0)

    def is_goal(self, state):
        """
        Check if the current state matches the goal state.
        
        Args:
            state: Tuple representing current puzzle configuration
            
        Returns:
            Boolean: True if state equals goal state, False otherwise
        """
        return state == self.goal_state

    def move(self, state, action):
        """
        Generate a new state by moving a tile into the blank space.
        
        The action represents moving a tile INTO the blank space:
        - 'L': Move tile from right side into blank (blank effectively moves right)
        - 'R': Move tile from left side into blank (blank effectively moves left)
        - 'U': Move tile from below into blank (blank effectively moves down)
        - 'D': Move tile from above into blank (blank effectively moves up)
        
        Args:
            state: Current puzzle state as tuple
            action: String representing move direction ('L', 'R', 'U', 'D')
            
        Returns:
            New state as tuple after move, or None if move is invalid
        """
        idx = self.get_blank_pos(state)           # Get current blank position
        row, col = divmod(idx, self.cols)         # Convert index to row, column coordinates
        new_idx = None                            # Initialize target position

        # Determine the position of tile to move into blank space
        if action == 'L' and col < self.cols - 1:  # Move tile from right into blank
            new_idx = idx + 1
        elif action == 'R' and col > 0:           # Move tile from left into blank
            new_idx = idx - 1
        elif action == 'U' and row < self.rows - 1:  # Move tile from below into blank
            new_idx = idx + self.cols
        elif action == 'D' and row > 0:           # Move tile from above into blank
            new_idx = idx - self.cols

        # Return None if move is invalid (out of bounds)
        if new_idx is None:
            return None

        # Create new state by swapping blank with target tile
        state = list(state)                       # Convert to list for modification
        state[idx], state[new_idx] = state[new_idx], state[idx]  # Swap positions
        return tuple(state)                       # Return as immutable tuple

    def get_neighbors(self, state):
        """
        Generate all valid neighboring states from the current state.
        
        Args:
            state: Current puzzle state as tuple
            
        Returns:
            List of tuples: Each tuple contains (new_state, action_taken)
        """
        neighbors = []
        # Try each possible action
        for action in self.actions:
            new_state = self.move(state, action)
            # Only add valid moves that result in different states
            if new_state and new_state != state:
                neighbors.append((new_state, action))
        return neighbors

    def manhattan_distance(self, state):
        """
        Calculate Manhattan Distance heuristic for A* search.
        
        Manhattan distance is the sum of horizontal and vertical distances
        each tile needs to move to reach its goal position. This is an
        admissible heuristic (never overestimates the actual cost).
        
        Args:
            state: Current puzzle state as tuple
            
        Returns:
            Integer: Sum of Manhattan distances for all tiles
        """
        distance = 0
        for i, tile in enumerate(state):
            if tile == 0:  # Skip the blank tile
                continue
            # Find where this tile should be in goal state
            goal_idx = self.goal_state.index(tile)
            # Convert current and goal positions to row,col coordinates
            row1, col1 = divmod(i, self.cols)         # Current position
            row2, col2 = divmod(goal_idx, self.cols)  # Goal position
            # Add Manhattan distance for this tile
            distance += abs(row1 - row2) + abs(col1 - col2)
        return distance

    def out_of_place(self, state):
        """
        Calculate Out-of-Place heuristic for A* search.
        
        Counts the number of tiles that are not in their correct positions.
        This is also an admissible heuristic but generally less informed
        than Manhattan distance.
        
        Args:
            state: Current puzzle state as tuple
            
        Returns:
            Integer: Number of tiles in wrong positions (excluding blank)
        """
        return sum(1 for i in range(len(state)) 
                  if state[i] != 0 and state[i] != self.goal_state[i])

    def a_star(self, heuristic_func):
        """
        Implement A* search algorithm to find optimal solution.
        
        A* uses f(n) = g(n) + h(n) where:
        - g(n) = actual cost from start to current node
        - h(n) = heuristic estimate from current node to goal
        - f(n) = estimated total cost of path through current node
        
        Args:
            heuristic_func: Function to calculate heuristic value (h(n))
            
        Returns:
            List of actions leading to goal, or None if no solution exists
        """
        # Priority queue: (f_score, g_score, state, path_to_state)
        heap = []
        initial_h = heuristic_func(self.start_state)
        heapq.heappush(heap, (initial_h, 0, self.start_state, []))
        
        # Set to keep track of visited states (avoid cycles)
        visited = set()
        visited.add(self.start_state)

        while heap:
            # Get state with lowest f-score
            f, g, state, path = heapq.heappop(heap)
            
            # Check if we've reached the goal
            if self.is_goal(state):
                return path
            
            # Explore all neighbors
            for neighbor, action in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Calculate costs for neighbor
                    new_g = g + 1                        # Cost increases by 1 for each move
                    h = heuristic_func(neighbor)         # Heuristic estimate to goal
                    new_f = new_g + h                    # Total estimated cost
                    # Add to priority queue
                    heapq.heappush(heap, (new_f, new_g, neighbor, path + [action]))
        
        return None  # No solution found

def get_valid_eight_puzzle_state(prompt):
    """
    Get and validate user input for 8-puzzle state.
    
    Ensures input contains exactly 9 integers from 0-8, each used exactly once.
    Continues prompting until valid input is provided.
    
    Args:
        prompt: String to display when asking for input
        
    Returns:
        List of 9 integers representing a valid puzzle state
    """
    while True:
        try:
            # Get user input and split into individual numbers
            user_input = input(prompt).split()
            
            # Check if exactly 9 numbers are entered
            if len(user_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            
            # Convert to integers and validate range
            state = []
            for num_str in user_input:
                num = int(num_str)
                if num < 0 or num > 8:
                    print("Error: All numbers must be between 0 and 8.")
                    raise ValueError
                state.append(num)
            
            # Check if all numbers 0-8 are present exactly once
            if sorted(state) != [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                print("Error: You must use each number from 0 to 8 exactly once.")
                continue
            
            return state
            
        except ValueError:
            print("Error: Please enter valid integers between 0 and 8.")

def main():
    """
    Main function to run the 8-puzzle solver program.
    
    Provides an interactive menu allowing users to:
    1. Solve using Manhattan Distance heuristic
    2. Solve using Out-of-Place heuristic  
    3. Change start state
    4. Change goal state
    5. Exit program
    """
    # Get initial puzzle states from user with validation
    start_state = get_valid_eight_puzzle_state("Enter the 8-puzzle start state: ")
    goal_state = get_valid_eight_puzzle_state("Enter the 8-puzzle goal state: ")
    
    # Create puzzle solver instance
    puzzle = EightPuzzle(start_state, goal_state)

    # Main program loop
    while True:
        print("Make selection: [1]: MD, [2]: OOPT, [3]: New start state, [4]: New goal state, [5] Exit")
        choice = input()
        
        if choice == '1':
            # Solve using Manhattan Distance heuristic
            start_time = timeit.default_timer()
            moves = puzzle.a_star(puzzle.manhattan_distance)
            elapsed_time = timeit.default_timer() - start_time
            print(f"Sequence of moves (MD): {' '.join(moves) if moves else 'No solution'}")
            print(f"No. of moves (MD): {len(moves) if moves else 0}")
            print(f"Time taken: {elapsed_time:.6f}")
            
        elif choice == '2':
            # Solve using Out-of-Place heuristic
            start_time = timeit.default_timer()
            moves = puzzle.a_star(puzzle.out_of_place)
            elapsed_time = timeit.default_timer() - start_time
            print(f"Sequence of moves (OOPT): {' '.join(moves) if moves else 'No solution'}")
            print(f"No. of moves (OOPT): {len(moves) if moves else 0}")
            print(f"Time taken: {elapsed_time:.6f}")
            
        elif choice == '3':
            # Allow user to input new start state
            start_state = get_valid_eight_puzzle_state("Enter the 8-puzzle start state: ")
            puzzle.start_state = tuple(start_state)
            
        elif choice == '4':
            # Allow user to input new goal state
            goal_state = get_valid_eight_puzzle_state("Enter the 8-puzzle goal state: ")
            puzzle.goal_state = tuple(goal_state)
            
        elif choice == '5':
            # Exit the program
            break
            
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()  # Execute main function when script is run directly