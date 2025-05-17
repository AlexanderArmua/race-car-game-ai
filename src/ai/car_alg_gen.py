from .car_rna import CarRNA
from ..config.settings import MUTATION_RATE
import random

CHROMOSOMES_AMOUNT = 12

class CarAlgGen:
    def __init__(self, population_size: int):
        if population_size < 2:
            raise ValueError("Population size must be greater than 2")

        self.population_size = population_size
        self.chromosomes_amount = CHROMOSOMES_AMOUNT

        self.population: list[CarRNA] = []

        self.generation = 0
    
    def generate_initial_population(self) -> list[CarRNA]:
        chromosomes_list = self.get_new_chromosomes(self.population_size)

        self.population = [CarRNA(chromosomes) for chromosomes in chromosomes_list]

        return self.population

    def get_new_population(self) -> list[CarRNA]:
        """
        Creates and returns a new population for the next generation.
        Also stores the new population as the current one.
        """
        self.generation += 1

        # Select best individuals from current population
        best_chromosomes = self.select_population(self.population)

        best_car = max(self.population, key=lambda rna: rna.get_score())

        # Create offspring through crossover
        crossovered_chromosomes = self.crossover_population(best_chromosomes)

        # Add some completely new individuals for genetic diversity
        additional_chromosomes = self.get_new_chromosomes(len(self.population) - len(crossovered_chromosomes))
        all_chromosomes = crossovered_chromosomes + additional_chromosomes

        # Apply mutations to the entire new population
        mutated_chromosomes = self.mutate_population(all_chromosomes)

        # Create CarRNA objects from the chromosomes
        new_population = [CarRNA(chromosomes) for chromosomes in mutated_chromosomes]

        # Store as current population for next generation
        self.population = new_population

        print(f"Generation: {self.generation} - Best car score: {best_car.get_score()}")

        return new_population

    def select_population(self, population: list[CarRNA]) -> list[list[float]]:
        """
        Returns the best half of the population applying tournament selection.
        """

        sorted_population = sorted(population, key=lambda rna: rna.get_score(), reverse=True)

        return [rna.get_chromosomes() for rna in sorted_population[:self.population_size // 2]]
              
    def crossover_population(self, population: list[list[float]]) -> list[list[float]]:
        """
        Returns the crossovered population applying simple crossover
        """
        
        crossover_population: list[list[float]] = []

        for i in range(0, len(population), 2):
            # break_point = random.randint(0, self.chromosomes_amount - 1)
            break_point = 10

            parent1 = population[i]
            parent2 = population[i + 1]

            child1 = parent1[:break_point] + parent2[break_point:]
            child2 = parent2[:break_point] + parent1[break_point:]

            crossover_population.append(child1)
            crossover_population.append(child2)

        return crossover_population
    
    def get_new_chromosomes(self, amount: int) -> list[list[float]]:
        """
        Returns a list of different chromosome sets (each one a list of weights).

        Args:
            amount: Number of chromosome sets to generate

        Returns:
            A list of lists, where each inner list is a set of chromosomes for one car
        """
        chromosome_sets: list[list[float]] = []

        for i in range(amount):
            new_chromosomes: list[float] = [random.uniform(-1, 1) for _ in range(self.chromosomes_amount)]
            chromosome_sets.append(new_chromosomes)

        return chromosome_sets

    def mutate_population(self, population: list[list[float]]) -> list[list[float]]:
        """
        Applies mutation to the population with some probability.
        Increases mutation rate as generations progress to avoid local optima.

        Args:
            population: List of chromosome sets

        Returns:
            The mutated population
        """
        # Increase mutation rate slightly based on generation (up to 5%)
        base_mutation_rate = 0.02  # 2% base mutation rate
        adaptive_rate = min(MUTATION_RATE, base_mutation_rate + (self.generation * 0.001))

        for chromosomes in population:
            # For each chromosome set, decide if it should be mutated
            should_mutate = random.random() < adaptive_rate

            if should_mutate:
                # Pick 1-3 genes to mutate (more impact)
                num_mutations = random.randint(1, 3)
                for _ in range(num_mutations):
                    mutation_point = random.randint(0, self.chromosomes_amount - 1)

                    # Apply mutation (either small or large change)
                    if random.random() < 0.7:  # 70% chance of small mutation
                        # Small adjustment to existing value (-0.2 to +0.2)
                        chromosomes[mutation_point] += random.uniform(-0.2, 0.2)
                        # Clamp value between -1 and 1
                        chromosomes[mutation_point] = max(-1, min(1, chromosomes[mutation_point]))
                    else:
                        # Complete replacement with new random value
                        chromosomes[mutation_point] = random.uniform(-1, 1)

        return population

    def should_stop(self, population: list[CarRNA]) -> bool:
        pass
        
    def run(self):
        pass

    def get_best_rna(self, population: list[CarRNA]) -> CarRNA:
        pass
               

    def get_generation(self) -> int:
        return self.generation
        
        