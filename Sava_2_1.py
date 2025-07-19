"""
Assessment 2  - Question 1  

Sava Josè Maria  
"""
import random
import os

class QueensGA:
    """
    * Class name       :   QueensGA
    * Purpose         :   Implements a Genetic Algorithm to solve the 8-Queens problem
    * Attributes      :   start_state, pop_size, mix_ratio, mut_rate, cross_type, 
    *                   population, generation, max_generations
    * Methods         :   fitness(), initialize_population(), tournament_selection(),
    *                   single_point_crossover(), two_point_crossover(), uniform_crossover(),
    *                   crossover(), mutate(), evaluate_population(), get_best_individual(),
    *                   create_new_generation(), solve()
    """

    def __init__(self, start_state, pop_size, mix_ratio, mut_rate, cross_type):
        """
        * Function name     :   __init__
        * Arguments         :   start_state (list) = initial board state,
        *                       pop_size (int) = population size,
        *                       mix_ratio (float) = mixing ratio for uniform crossover,
        *                       mut_rate (float) = mutation rate,
        *                       cross_type (int) = crossover type (1-3)
        * Return value/s    :   None
        * Remarks           :   Initializes the GA with given parameters
        """
        self.start_state = start_state
        self.pop_size = pop_size
        self.mix_ratio = mix_ratio
        self.mut_rate = mut_rate
        self.cross_type = cross_type
        self.population = []
        self.generation = 0
        self.max_generations = 10000
    
    def fitness(self, state):
        """
        * Function name     :   fitness
        * Arguments         :   state (list) = current board state
        * Return value/s    :   int = fitness score (28 - number of attacking pairs)
        * Remarks           :   Calculates fitness by counting non-attacking queen pairs
        """
        attacks = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if state[i] == state[j]:  # same row
                    attacks += 1
                if abs(i - j) == abs(state[i] - state[j]):  # diagonal
                    attacks += 1
        return 28 - attacks
    
    def initialize_population(self):
        """
        * Function name     :   initialize_population
        * Arguments         :   None
        * Return value/s    :   None
        * Remarks           :   Initializes population with start state and random individuals
        """
        self.population = [self.start_state] + [[random.randint(1, 8) for _ in range(8)] 
                                               for _ in range(self.pop_size - 1)]
    
    def tournament_selection(self, fitnesses, k=3):
        """
        * Function name     :   tournament_selection
        * Arguments         :   fitnesses (list) = list of fitness scores,
        *                       k (int) = tournament size (default 3)
        * Return value/s    :   list = selected parent state
        * Remarks           :   Selects parent using tournament selection from k random individuals
        """
        k = min(k, len(self.population))
        selected = random.sample(list(enumerate(self.population)), k)
        idx, best = max(selected, key=lambda x: fitnesses[x[0]])
        return best
    
    def single_point_crossover(self, p1, p2):
        """
        * Function name     :   single_point_crossover
        * Arguments         :   p1 (list) = first parent state,
        *                       p2 (list) = second parent state
        * Return value/s    :   tuple = (child1, child2)
        * Remarks           :   Performs single-point crossover at random point
        """
        pt = random.randint(1, 6)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
        return c1, c2
    
    def two_point_crossover(self, p1, p2):
        """
        * Function name     :   two_point_crossover
        * Arguments         :   p1 (list) = first parent state,
        *                       p2 (list) = second parent state
        * Return value/s    :   tuple = (child1, child2)
        * Remarks           :   Performs two-point crossover at random points
        """
        pt1, pt2 = sorted(random.sample(range(1, 8), 2))
        c1 = p1[:pt1] + p2[pt1:pt2] + p1[pt2:]
        c2 = p2[:pt1] + p1[pt1:pt2] + p2[pt2:]
        return c1, c2
    
    def uniform_crossover(self, p1, p2):
        """
        * Function name     :   uniform_crossover
        * Arguments         :   p1 (list) = first parent state,
        *                       p2 (list) = second parent state
        * Return value/s    :   tuple = (child1, child2)
        * Remarks           :   Performs uniform crossover using mix_ratio
        """
        c1, c2 = [], []
        for i in range(8):
            if random.random() < self.mix_ratio:
                c1.append(p2[i])
                c2.append(p1[i])
            else:
                c1.append(p1[i])
                c2.append(p2[i])
        return c1, c2
    
    def crossover(self, p1, p2):
        """
        * Function name     :   crossover
        * Arguments         :   p1 (list) = first parent state,
        *                       p2 (list) = second parent state
        * Return value/s    :   tuple = (child1, child2)
        * Remarks           :   Applies crossover based on cross_type (1-3)
        """
        if self.cross_type == 1:
            return self.single_point_crossover(p1, p2)
        elif self.cross_type == 2:
            return self.two_point_crossover(p1, p2)
        else:  # cross_type == 3
            return self.uniform_crossover(p1, p2)
    
    def mutate(self, state):
        """
        * Function name     :   mutate
        * Arguments         :   state (list) = individual state to mutate
        * Return value/s    :   list = mutated state
        * Remarks           :   Mutates each gene with  mut_rate
        """
        return [random.randint(1, 8) if random.random() < self.mut_rate else gene for gene in state]
    
    def evaluate_population(self):
        """
        * Function name     :   evaluate_population
        * Arguments         :   None
        * Return value/s    :   list = fitness scores for all individuals
        * Remarks           :   Calculates fitness for each individual in population
        """
        return [self.fitness(state) for state in self.population]
    
    def get_best_individual(self, fitnesses):
        """
        * Function name     :   get_best_individual
        * Arguments         :   fitnesses (list) = list of fitness scores
        * Return value/s    :   tuple = (best_state, best_fitness)
        * Remarks           :   Returns the best individual and its fitness score
        """
        best_idx = max(range(self.pop_size), key=lambda i: fitnesses[i])
        return self.population[best_idx], fitnesses[best_idx]
    
    def create_new_generation(self, fitnesses):
        """
        * Function name     :   create_new_generation
        * Arguments         :   fitnesses (list) = list of fitness scores
        * Return value/s    :   None
        * Remarks           :   Creates new population through selection, crossover and mutation
        """
        new_population = []
        
        pairs_to_create = self.pop_size // 2
        
        for _ in range(pairs_to_create):
            p1 = self.tournament_selection(fitnesses)
            p2 = self.tournament_selection(fitnesses)
            
            c1, c2 = self.crossover(p1, p2)
            
            c1 = self.mutate(c1)
            c2 = self.mutate(c2)
            
            new_population.extend([c1, c2])
        
        if len(new_population) < self.pop_size:
            p1 = self.tournament_selection(fitnesses)
            p2 = self.tournament_selection(fitnesses)
            c1, c2 = self.crossover(p1, p2)
            c1 = self.mutate(c1)
            new_population.append(c1)
        
        self.population = new_population[:self.pop_size]
    
    def solve(self):
        """
        * Function name     :   solve
        * Arguments         :   None
        * Return value/s    :   list = solution state or None if not found
        * Remarks           :   Main GA loop that evolves population until solution found
        """
        self.initialize_population()
        
        while self.generation < self.max_generations:
            fitnesses = self.evaluate_population()
            
            best_state, best_fit = self.get_best_individual(fitnesses)
            
            print(f"Generation {self.generation + 1}: Best state: {best_state}, Fitness: {best_fit}")
            
            if best_fit == 28:
                print(f"Found solution: {best_state}")
                print("Fitness: 28")
                print(f"No. of generations: {self.generation + 1}")
                return best_state
            
            self.create_new_generation(fitnesses)
            self.generation += 1
        
        print("No solution found within max generations")
        return None

def create_sample_input_file():
    """
    * Function name     :   create_sample_input_file
    * Arguments         :   None
    * Return value/s    :   None
    * Remarks           :   Creates a sample GA_input.txt file if none exists with values from professor asessment 
    """
    sample_content = "2, 4, 7, 4, 8, 5, 5, 2; 15; 0.5; 0.15; 3"
    with open('GA_input.txt', 'w') as f:
        f.write(sample_content)
    print("Created sample GA_input.txt file")

def main():
    """
    * Function name     :   main
    * Arguments         :   None
    * Return value/s    :   None
    * Remarks           :   Main program entry point, reads input from GA_input.txt and runs GA
    """
    if not os.path.exists('GA_input.txt'):
        print("GA_input.txt file not found!")
        print("Creating a sample input file...")
        create_sample_input_file()
        print("Please modify GA_input.txt with your desired parameters and run again.")
        return
    
    try:
        with open('GA_input.txt', 'r') as f:
            data = f.read().strip().split(';')
        
        if len(data) < 5:
            print(f"Error: Expected 5 parameters in GA_input.txt, but found {len(data)}")
            print("Expected format: start_state;pop_size;mix_ratio;mut_rate;cross_type")
            print("Example: 1,2,3,4,5,6,7,8;100;0.5;0.1;1")
            return
        
        start_state = [int(x.strip()) for x in data[0].split(',')]
        pop_size = int(data[1])
        mix_ratio = float(data[2])
        mut_rate = float(data[3])
        cross_type = int(data[4])
        
        if len(start_state) != 8:
            print(f"Error: Start state must have 8 queens, but found {len(start_state)}")
            return
        
        if not all(1 <= q <= 8 for q in start_state):
            print("Error: Queen positions must be between 1 and 8")
            return
        
        if pop_size <= 0:
            print("Error: Population size must be positive")
            return
        
        if not (0 <= mix_ratio <= 1):
            print("Error: Mix ratio must be between 0 and 1")
            return
        
        if not (0 <= mut_rate <= 1):
            print("Error: Mutation rate must be between 0 and 1")
            return
        
        if cross_type not in [1, 2, 3]:
            print("Error: Crossover type must be 1, 2, or 3")
            return
        
        print(f"Starting GA with parameters:")
        print(f"Start state: {start_state}")
        print(f"Population size: {pop_size}")
        print(f"Mix ratio: {mix_ratio}")
        print(f"Mutation rate: {mut_rate}")
        print(f"Crossover type: {cross_type}")
        print()
        
        ga = QueensGA(start_state, pop_size, mix_ratio, mut_rate, cross_type)
        solution = ga.solve()
        
        if solution:
            print(f"Final solution: {solution}")
        else:
            print("No solution found")
            
    except ValueError as e:
        print(f"Error parsing input file: {e}")
        print("Please check that all numeric values are valid")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
