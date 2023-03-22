from optimizer import optimizerStrategy
from optimizer.bruteforce import bruteforce1

def main():
    optimizer = optimizerStrategy.OptimizerStrategy(bruteforce1.optimize)
    optimizer.optimize()
    
if __name__ == "__main__":
    main()
    

