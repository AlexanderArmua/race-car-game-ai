from .car_rna import CarRNA
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
        chromosomes = self.get_new_chromosomes(self.population_size)

        self.population = [CarRNA(chromosomes) for chromosomes in chromosomes]

        return self.population

    def get_new_population(self) -> list[CarRNA]:
        self.generation += 1

        best_rnas = self.select_population(self.population)

        crossovered_rnas = self.crossover_population(best_rnas)

        new_chromosomes = self.get_new_chromosomes(len(self.population) - len(crossovered_rnas))

        crossovered_rnas.extend(new_chromosomes)

        mutated_rnas = self.mutate_population(crossovered_rnas)

        new_population = [CarRNA(chromsomes) for chromsomes in mutated_rnas]

        print(f"best_rnas: {len(best_rnas)} - crossovered_rnas: {len(crossovered_rnas)} - mutated_rnas: {len(mutated_rnas)} - new_population: {len(new_population)}")

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
        
        crossover_population = []

        for i in range(0, len(population), 2):
            break_point = random.randint(0, self.chromosomes_amount - 1)

            parent1 = population[i]
            parent2 = population[i + 1]

            crossover_population.append(parent1[:break_point] + parent2[break_point:])
            crossover_population.append(parent2[:break_point] + parent1[break_point:])           

        return crossover_population
    
    def get_new_chromosomes(self, amount: int) -> list[list[float]]:
        """
        Returns a new population of the given amount.
        """
        population = []

        for i in range(amount):
            chromsomes: list[float] = [random.uniform(-1, 1) for _ in range(self.chromosomes_amount)]

            population.append(chromsomes)

        return population   

    def mutate_population(self, population: list[list[float]]) -> list[list[float]]:
        """
        Returns the mutated population applying mutation.
        """

        for rna in population:
            should_mutate = random.random() < 0.01

            if should_mutate:
                mutation_point = random.randint(0, self.chromosomes_amount - 1)

                rna[mutation_point] = random.uniform(-1, 1)

        return population

    def should_stop(self, population: list[CarRNA]) -> bool:
        pass
        
    def run(self):
        pass

    def get_best_rna(self, population: list[CarRNA]) -> CarRNA:
        pass
               

    def get_generation(self) -> int:
        return self.generation
        
        