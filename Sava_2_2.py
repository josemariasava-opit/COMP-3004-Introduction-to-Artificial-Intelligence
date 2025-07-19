"""
Assessment 2 - Question 2 

Sava Josè Maria 

* Requirements      :   fn.py must be in same directory of this file 
"""

import random
import math
from fn import f  # Import optimization function from external file

def hill_climbing(objective, x0, x_min, x_max, max_steps=10000):
    """
    * Function name     :   hill_climbing
    * Arguments         :   objective (str) = 'max' or 'min',
    *                       x0 (float) = starting x value,
    *                       x_min (float) = minimum x bound,
    *                       x_max (float) = maximum x bound,
    *                       max_steps (int) = maximum iterations (default 10000)
    * Return value/s    :   tuple = (best_x, best_val, steps)
    * Remarks           :   Basic hill climbing algorithm that explores immediate neighbors
    *                       and moves toward better solutions until local optimum found
    """
    step_size = (x_max - x_min) / 1000.0  # Relative step size for neighborhood search
    current_x = x0
    current_val = f(current_x)
    steps = 0

    for _ in range(max_steps):
        # Explore left and right neighbors within bounds
        left_x = max(x_min, current_x - step_size)
        right_x = min(x_max, current_x + step_size)
        left_val = f(left_x)
        right_val = f(right_x)
        neighbors = [(left_x, left_val), (right_x, right_val)]

        # Select best neighbor based on optimization objective
        if objective == 'max':
            next_x, next_val = max(neighbors, key=lambda x: x[1])
        else:
            next_x, next_val = min(neighbors, key=lambda x: x[1])

        # Termination condition - no improvement found
        if (objective == 'max' and next_val <= current_val) or \
           (objective == 'min' and next_val >= current_val):
            break

        current_x, current_val = next_x, next_val
        steps += 1

    return current_x, current_val, steps

def random_restart_hill_climbing(objective, x_min, x_max, restarts=10):
    """
    * Function name     :   random_restart_hill_climbing
    * Arguments         :   objective (str) = 'max' or 'min',
    *                       x_min (float) = minimum x bound,
    *                       x_max (float) = maximum x bound,
    *                       restarts (int) = number of random restarts (default 10)
    * Return value/s    :   tuple = (best_x, best_val, total_steps)
    * Remarks           :   Runs hill climbing multiple times from random starting points
    *                       to escape local optima and find global optimum
    """
    best_x, best_val = None, -math.inf if objective == 'max' else math.inf
    total_steps = 0

    for _ in range(restarts):
        # Random initialization within search space
        x0 = random.uniform(x_min, x_max)
        x, val, steps = hill_climbing(objective, x0, x_min, x_max)
        total_steps += steps
        
        # Update best solution found across all restarts
        if (objective == 'max' and val > best_val) or \
           (objective == 'min' and val < best_val):
            best_x, best_val = x, val

    return best_x, best_val, total_steps

def local_beam_search(objective, k, x_min, x_max, max_steps=1000):
    """
    * Function name     :   local_beam_search
    * Arguments         :   objective (str) = 'max' or 'min',
    *                       k (int) = number of parallel beams,
    *                       x_min (float) = minimum x bound,
    *                       x_max (float) = maximum x bound,
    *                       max_steps (int) = maximum iterations (default 1000)
    * Return value/s    :   tuple = (best_x, best_val, steps)
    * Remarks           :   Maintains k parallel searches, keeping top k candidates
    *                       at each iteration to explore multiple promising regions
    """
    # Initialize beam with random positions in search space
    beam = [random.uniform(x_min, x_max) for _ in range(k)]
    step_size = (x_max - x_min) / 1000.0
    steps = 0

    for _ in range(max_steps):
        candidates = []
        # Generate and evaluate neighbors for all current beam positions
        for x in beam:
            left_x = max(x_min, x - step_size)
            right_x = min(x_max, x + step_size)
            candidates.extend([
                (left_x, f(left_x)),
                (x, f(x)),
                (right_x, f(right_x))
            ])

        # Sort and select top k candidates based on objective
        candidates.sort(key=lambda x: x[1], reverse=(objective == 'max'))
        beam = [x[0] for x in candidates[:k]]
        steps += 1

    # Return best solution from final beam
    best_x = max(beam, key=f) if objective == 'max' else min(beam, key=f)
    return best_x, f(best_x), steps

def stochastic_beam_search(objective, k, x_min, x_max, max_steps=1000):
    """
    * Function name     :   stochastic_beam_search
    * Arguments         :   objective (str) = 'max' or 'min',
    *                       k (int) = number of parallel beams,
    *                       x_min (float) = minimum x bound,
    *                       x_max (float) = maximum x bound,
    *                       max_steps (int) = maximum iterations (default 1000)
    * Return value/s    :   tuple = (best_x, best_val, steps)
    * Remarks           :   Maintains k parallel searches, selecting candidates
    *                       probabilistically with higher fitness solutions having
    *                       better chance of being selected
    """
    # Initialize beam with random positions
    beam = [random.uniform(x_min, x_max) for _ in range(k)]
    step_size = (x_max - x_min) / 1000.0
    steps = 0

    for _ in range(max_steps):
        candidates = []
        # Generate and evaluate neighborhood for each beam position
        for x in beam:
            left_x = max(x_min, x - step_size)
            right_x = min(x_max, x + step_size)
            candidates.extend([
                (left_x, f(left_x)),
                (x, f(x)),
                (right_x, f(right_x))
            ])
        values = [val for _, val in candidates]

        # Calculate selection weights based on fitness
        if objective == 'max':
            weights = [val - min(values) + 1e-5 for val in values]  # Ensure positive weights
        else:
            weights = [max(values) - val + 1e-5 for val in values]  # Ensure positive weights

        # Probabilistically select next beam positions
        selected = random.choices(candidates, weights=weights, k=k)
        beam = [x[0] for x in selected]
        steps += 1

    # Return best solution from final beam
    best_x = max(beam, key=f) if objective == 'max' else min(beam, key=f)
    return best_x, f(best_x), steps

def main():
    """
    * Function name     :   main
    * Arguments         :   None
    * Return value/s    :   None
    * Remarks           :   Handles user interaction, input collection, and
    *                       execution of selected optimization algorithm
    """
    # Get optimization objective from user
    while True:
        objective = input("Enter objective (max or min): ").strip().lower()
        if objective in ['max', 'min']:
            break
        print("Invalid objective. Please enter 'max' or 'min'.")

    # Get starting position input
    x0_input = input("Enter starting value of x (0 for random x): ").strip()
    
    # Get search space bounds
    while True:
        try:
            x_min, x_max = map(float, input("Enter range of x (min, max): ").split(','))
            if x_min >= x_max:
                print("Error: min must be less than max")
                continue
            break
        except ValueError:
            print("Invalid range format. Please enter two numbers separated by comma.")

    # Set starting position
    x0 = random.uniform(x_min, x_max) if x0_input == '0' else float(x0_input)
    
    # Main algorithm selection loop
    while True:
        print("\nSelect algorithm:")
        print("[1] Hill Climbing")
        print("[2] Random Restart Hill Climbing")
        print("[3] Local Beam Search (k=5)")
        print("[4] Stochastic Beam Search (k=5)")
        print("[5] Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '5':
            print("Exiting program.")
            break
        
        algorithm_names = {
            '1': 'Hill Climbing',
            '2': 'Random Restart Hill Climbing',
            '3': 'Local Beam Search',
            '4': 'Stochastic Beam Search'
        }
        
        if choice in algorithm_names:
            # Execute selected algorithm
            if choice == '1':
                x, val, steps = hill_climbing(objective, x0, x_min, x_max)
            elif choice == '2':
                x, val, steps = random_restart_hill_climbing(objective, x_min, x_max)
            elif choice == '3':
                x, val, steps = local_beam_search(objective, 5, x_min, x_max)
            elif choice == '4':
                x, val, steps = stochastic_beam_search(objective, 5, x_min, x_max)
            
            # Display results
            print(f"\n{algorithm_names[choice]} Results:")
            print(f"Found {objective} f(x) = {val:.6f}")
            print(f"At x = {x:.6f}")
            print(f"Steps taken: {steps}")
        else:
            print("Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main()
