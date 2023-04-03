class OptimizerStrategy:
    def __init__(self, func=None):
        if func:
            self.optimize = func

    def optimize(self):
        print("Concrete function is not initialized")
