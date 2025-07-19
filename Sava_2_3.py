"""
Assessment 2  - Question 3  

Sava Josè Maria  
"""
from sorobn import BayesNet
import pandas as pd

def main():
    """
    * Function name     :   main
    * Arguments         :   None
    * Return value/s    :   None
    * Remarks           :   Main program that creates and queries a Bayesian Network for exam performance analysis
    """
    
    # Create Bayesian Network
    """
    * Variable name     :   bn
    * Type             :   BayesNet
    * Purpose           :   The main Bayesian Network object that will hold all nodes and probabilities
    """
    net = BayesNet()
    
    # Add nodes and their probability distributions
    
    # Root nodes (no parents)
    """
    * Probability assignment : net.P['I']
    * Type                  : pd.Series
    * Purpose               : Defines marginal probabilities for Intelligence node
    * Values                : {0: 0.3, 1: 0.7} where 0=not intelligent, 1=intelligent
    """
    net.P['I'] = pd.Series({0: 0.3, 1: 0.7})      # P(-i)=0.3, P(+i)=0.7
    
    """
    * Probability assignment : net.P['H']
    * Type                  : pd.Series
    * Purpose               : Defines marginal probabilities for Hardworking node
    * Values                : {0: 0.35, 1: 0.65} where 0=not hardworking, 1=hardworking
    """
    net.P['H'] = pd.Series({0: 0.35, 1: 0.65})    # P(-h)=0.35, P(+h)=0.65
    
    # GoodTestTaker (depends on Intelligence)
    """
    * Probability assignment : net.P['G']
    * Type                  : pd.Series
    * Purpose               : Defines conditional probabilities for GoodTestTaker node
    * Format                : (parent_state, child_state): probability
    * Values                : (0,0)=P(-g|I=0), (0,1)=P(+g|I=0), etc.
    """
    net.P['G'] = pd.Series({
        (0, 0): 0.45, (0, 1): 0.55,  # I=0: P(-g)=0.45, P(+g)=0.55
        (1, 0): 0.16, (1, 1): 0.84   # I=1: P(-g)=0.16, P(+g)=0.84
    })
    
    # UnderstandsMaterial (depends on Intelligence and Hardworking)
    """
    * Probability assignment : net.P['U']
    * Type                  : pd.Series
    * Purpose               : Defines conditional probabilities for UnderstandsMaterial node
    * Format                : (I_state, H_state, U_state): probability
    * Values                : All combinations of parent and child states
    """
    net.P['U'] = pd.Series({
        (0, 0, 0): 0.85, (0, 0, 1): 0.15,  # I=0,H=0: P(-u)=0.85, P(+u)=0.15
        (0, 1, 0): 0.66, (0, 1, 1): 0.34,  # I=0,H=1: P(-u)=0.66, P(+u)=0.34
        (1, 0, 0): 0.23, (1, 0, 1): 0.77,  # I=1,H=0: P(-u)=0.23, P(+u)=0.77
        (1, 1, 0): 0.05, (1, 1, 1): 0.95   # I=1,H=1: P(-u)=0.05, P(+u)=0.95
    })
    
    # ExamScore (depends on UnderstandsMaterial and GoodTestTaker)
    """
    * Probability assignment : net.P['E']
    * Type                  : pd.Series
    * Purpose               : Defines conditional probabilities for ExamScore node
    * Format                : (U_state, G_state, E_state): probability
    * Values                : All combinations of parent and child states
    """
    net.P['E'] = pd.Series({
        (0, 0, 0): 0.95, (0, 0, 1): 0.05,  # U=0,G=0: P(-e)=0.95, P(+e)=0.05
        (0, 1, 0): 0.75, (0, 1, 1): 0.25,  # U=0,G=1: P(-e)=0.75, P(+e)=0.25
        (1, 0, 0): 0.18, (1, 0, 1): 0.82,  # U=1,G=0: P(-e)=0.18, P(+e)=0.82
        (1, 1, 0): 0.02, (1, 1, 1): 0.98   # U=1,G=1: P(-e)=0.02, P(+e)=0.98
    })
    
    # Define the network structure
    """
    * Variable assignment   : net.parents
    * Type                 : dict
    * Purpose              : Specifies parent relationships for each node
    * Structure            : {'node': ['parent1', 'parent2']}
    """
    net.parents = {
        'G': ['I'],
        'U': ['I', 'H'], 
        'E': ['U', 'G']
    }
    
    """
    * Variable assignment   : net.children
    * Type                 : dict
    * Purpose              : Specifies child relationships for each node
    * Structure            : {'node': ['child1', 'child2']}
    """
    net.children = {
        'I': ['G', 'U'],
        'H': ['U'],
        'U': ['E'],
        'G': ['E']
    }
    
    """
    * Variable assignment   : net.nodes
    * Type                 : list
    * Purpose              : Lists all nodes in the network in topological order
    """
    net.nodes = ['I', 'H', 'G', 'U', 'E']
    
    # Prepare the network (important!)
    """
    * Function call        : net.prepare()
    * Purpose             : Finalizes the network structure for querying
    * Remarks             : Must be called after defining all probabilities and relationships
    """
    net.prepare()


    print("Variable Legends:")
    print("==================")
    print("I: Intelligence (0 = not intelligent, 1 = intelligent)")
    print("H: Hardworking (0 = not hardworking, 1 = hardworking)")
    print("G: Good Test Taker (0 = not good test taker, 1 = good test taker)")
    print("U: Understands Material (0 = doesn't understand, 1 = understands)")
    print("E: Exam Score (0 = bad score, 1 = good score)")
    print("\n" + "="*50 + "\n")

    # Define and execute queries
    """
    * Variable name       : queries
    * Type               : list of tuples
    * Purpose            : Contains all queries to be executed
    * Format             : (description, query_var, evidence_dict)
    """
    queries = [
        ("Probability of understanding material given good exam score (P(+u | +e))", 
         'U', {'E': 1}),
        
        ("Probability of being intelligent given bad exam score (P(+i | -e))", 
         'I', {'E': 0}),
        
        ("Probability of NOT being intelligent given good test taker (P(-i | +g))", 
         'I', {'G': 1}),
        
        ("Probability of NOT being hardworking given understands material but bad exam (P(-h | +u, -e))", 
         'H', {'U': 1, 'E': 0})
    ]
    
    print("\nBayesian Network Query Results:")
    print("=" * 60)
    
    for desc, query_var, evidence in queries:
        # Convert evidence values to match the data types in the network
        """
        * Variable name     : converted_evidence
        * Type             : dict
        * Purpose          : Stores evidence after converting to proper data types
        """
        converted_evidence = {}
        for var, value in evidence.items():
            # Convert to integer since states are binary 0-1 
            converted_evidence[var] = int(value)
        
        # Print current query information
        print(f"\nQuery: {desc}")
        print(f"Evidence: {converted_evidence}")
        
        try:
            # Execute query
            """
            * Function call    : net.query()
            * Purpose         : Performs probabilistic inference
            * Arguments       : query_var = variable to query,
            *                   event = evidence dictionary
            * Return value    : Probability distribution as pd.Series
            """
            result = net.query(query_var, event=converted_evidence)
            
            # For binary variables, result[0] is P(0), result[1] is P(1)
            # Check if result is a Series with index [0, 1]
            if isinstance(result, pd.Series):
                # Print the full probability distribution
                print("\nFull Probability Distribution:")
                print(result.to_string())
                
                # Determine which probability we need based on query description
                if "NOT" in desc or "P(-" in desc:  # Negative query
                    prob = result[0]
                    state_desc = "negative state (0)"
                else:  # Positive query
                    prob = result[1]
                    state_desc = "positive state (1)"
                
                print(f"\nRelevant Probability (for {state_desc}): {prob:.4f}")
                print(f"Interpretation: {desc.split('(')[0].strip()} = {prob:.2%}")
            else:
                # Handle cases where result might be in different format
                print("\nUnexpected result format:")
                print(result)
            
            print("-" * 60)
            
        except Exception as e:
            print(f"\nError executing query: {e}")
            print("-" * 60)

if __name__ == "__main__":
    main()
