
from algorithms import GeneticAlgorithmRandomized
import calculations as calc


class RouteOptimisation:
    """klasa odpowiedzialana za realizcję obsługę optymalizacji"""

    def __init__(self):
        """inicjalizacja obiektu klasy route optimization"""

        # inicjalizacja pierwszego algorytmu
        self.ga_random = GeneticAlgorithmRandomized()

