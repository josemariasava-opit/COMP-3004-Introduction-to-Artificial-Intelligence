# Question 1
# Sava Josè Maria

import timeit  # For measuring execution time
from collections import deque  # For implementing BFS queue

class FivePuzzle:
    """
    Class to represent and solve the 5-puzzle (2x3 grid) using BFS and IDS.
    The puzzle consists of tiles numbered 1–5 and a blank space (0).
    """

    def __init__(self, start_state, goal_state):
        """
        Initialize the 5-puzzle with start and goal states.

        Args:
            start_state: List of 6 integers representing the initial configuration
            goal_state: List of 6 integers representing the target configuration
        """
        self.start_state = tuple(start_state)   # Immutable format
        self.goal_state = tuple(goal_state)
        self.rows = 2                           # Number of rows in puzzle
        self.cols = 3                           # Number of columns in puzzle
        self.actions = ['U', 'D', 'L', 'R']     # Possible moves: Up, Down, Left, Right

    def get_blank_position(self, state):
        """
        Get the index of the blank tile (0) in the state.

        Args:
            state: Tuple representing puzzle state

        Returns:
            Integer index (0–5) of the blank tile
        """
        return state.index(0)

    def is_goal(self, state):
        """
        Check if the current state matches the goal state.

        Args:
            state: Tuple representing puzzle state

        Returns:
            True if goal is reached, False otherwise
        """
        return state == self.goal_state

    def move(self, state, action):
        """
        Generate a new state by moving a tile into the blank space.

        Actions describe where the tile comes from:
        - 'U': Move tile from below into blank
        - 'D': Move tile from above into blank
        - 'L': Move tile from right into blank
        - 'R': Move tile from left into blank

        Args:
            state: Current puzzle state as tuple
            action: Direction of the move ('U', 'D', 'L', 'R')

        Returns:
            New state as a tuple or None if move is invalid
        """
        idx = self.get_blank_position(state)
        row, col = divmod(idx, self.cols)
        new_idx = None

        # Determine index to swap with blank based on direction
        if action == 'U' and row < self.rows - 1:
            new_idx = idx + self.cols
        elif action == 'D' and row > 0:
            new_idx = idx - self.cols
        elif action == 'L' and col < self.cols - 1:
            new_idx = idx + 1
        elif action == 'R' and col > 0:
            new_idx = idx - 1

        if new_idx is None:
            return None  # Invalid move

        # Perform the swap and return new state
        state = list(state)
        state[idx], state[new_idx] = state[new_idx], state[idx]
        return tuple(state)

    def get_neighbors(self, state):
        """
        Generate all valid neighboring states from the current state.

        Args:
            state: Tuple representing current puzzle state

        Returns:
            List of (new_state, action) pairs
        """
        neighbors = []
        for action in self.actions:
            new_state = self.move(state, action)
            if new_state and new_state != state:
                neighbors.append((new_state, action))
        return neighbors

    def bfs(self):
        """
        Solve the puzzle using Breadth-First Search (BFS).

        Returns:
            List of actions to reach goal, or None if no solution exists
        """
        queue = deque()
        queue.append((self.start_state, []))  # (state, path)
        visited = set()
        visited.add(self.start_state)

        while queue:
            state, path = queue.popleft()
            if self.is_goal(state):
                return path
            for neighbor, action in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [action]))
        return None

    def ids(self):
        """
        Solve the puzzle using Iterative Deepening Search (IDS).

        Returns:
            List of actions to reach goal, or None if no solution exists
        """
        def dls(state, path, depth, visited):
            if self.is_goal(state):
                return path
            if depth == 0:
                return None
            for neighbor, action in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result = dls(neighbor, path + [action], depth - 1, visited)
                    if result is not None:
                        return result
                    visited.remove(neighbor)
            return None

        depth = 0
        while True:
            visited = set([self.start_state])
            result = dls(self.start_state, [], depth, visited)
            if result is not None:
                return result
            depth += 1

def get_valid_state(prompt):
    """
    Prompt user to input a valid 5-puzzle state.

    Ensures input contains exactly 6 integers from 0 to 5, each appearing once.

    Args:
        prompt: Message displayed to the user

    Returns:
        List of 6 integers representing a valid puzzle state
    """
    while True:
        try:
            user_input = input(prompt).split()

            # Check for correct length
            if len(user_input) != 6:
                print("Error: Please enter exactly 6 numbers.")
                continue

            # Convert to integers and validate range
            state = []
            for num_str in user_input:
                num = int(num_str)
                if num < 0 or num > 5:
                    print("Error: All numbers must be between 0 and 5.")
                    raise ValueError
                state.append(num)

            # Validate all digits from 0 to 5 are present
            if sorted(state) != [0, 1, 2, 3, 4, 5]:
                print("Error: You must use each number from 0 to 5 exactly once.")
                continue

            return state

        except ValueError:
            print("Error: Please enter valid integers between 0 and 5.")

def main():
    """
    Main function to run the 5-puzzle solver program.

    Allows users to:
    1. Solve using BFS
    2. Solve using IDS
    3. Change start state
    4. Change goal state
    5. Exit program
    """
    # Get initial start and goal states from user
    start_state = get_valid_state("Enter the 5-puzzle start state: ")
    goal_state = get_valid_state("Enter the 5-puzzle goal state: ")
    puzzle = FivePuzzle(start_state, goal_state)

    # Interactive menu loop
    while True:
        print("Make selection: [1]: BFS, [2]: IDS, [3]: New start state, [4]: New goal state, [5] Exit")
        choice = input()
        if choice == '1':
            # Solve using Breadth-First Search
            start_time = timeit.default_timer()
            moves = puzzle.bfs()
            elapsed_time = timeit.default_timer() - start_time
            print(f"Sequence of moves (BFS): {' '.join(moves) if moves else 'No solution'}")
            print(f"No. of steps (BFS): {len(moves) if moves else 0}")
            print(f"Time taken: {elapsed_time:.6f}")
        elif choice == '2':
            # Solve using Iterative Deepening Search
            start_time = timeit.default_timer()
            moves = puzzle.ids()
            elapsed_time = timeit.default_timer() - start_time
            print(f"Sequence of moves (IDS): {' '.join(moves) if moves else 'No solution'}")
            print(f"No. of steps (IDS): {len(moves) if moves else 0}")
            print(f"Time taken: {elapsed_time:.6f}")
        elif choice == '3':
            # Change start state
            start_state = get_valid_state("Enter the 5-puzzle start state: ")
            puzzle.start_state = tuple(start_state)
        elif choice == '4':
            # Change goal state
            goal_state = get_valid_state("Enter the 5-puzzle goal state: ")
            puzzle.goal_state = tuple(goal_state)
        elif choice == '5':
            # Exit program
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()  # Run main function when script is executed directly
