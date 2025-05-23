import random
from typing import List

from src.config.settings import CROSSOVER_RATE, MUTATION_RATE

from .car_rna import CarRNA

CHROMOSOMES_AMOUNT: int = 12


class CarAlgGen:
    def __init__(self, population_size: int) -> None:
        """
        Initialize the genetic algorithm.

        Args:
            population_size: Number of individuals in the population

        Raises:
            ValueError: If population size is less than 2
        """
        if population_size < 2:
            raise ValueError("Population size must be greater than 2")

        self.population_size: int = population_size
        self.chromosomes_amount: int = CHROMOSOMES_AMOUNT
        self.population: List[CarRNA] = []
        self.generation: int = 0

    def generate_initial_population(self) -> List[CarRNA]:
        """
        Generate the initial population of neural networks.

        Returns:
            List of CarRNA objects representing the initial population
        """
        chromosomes_list: List[List[float]] = self.get_new_chromosomes(
            self.population_size
        )
        self.population = [CarRNA(chromosomes) for chromosomes in chromosomes_list]
        return self.population

    def get_new_population(self) -> List[CarRNA]:
        """
        Creates and returns a new population for the next generation.
        Also stores the new population as the current one.

        Returns:
            List of CarRNA objects representing the new population
        """
        self.generation += 1

        # Select best individuals from current population
        best_chromosomes: List[List[float]] = self.select_population(self.population)

        best_car: CarRNA = max(self.population, key=lambda rna: rna.get_score())

        # Create offspring through crossover
        crossovered_chromosomes: List[List[float]] = self.crossover_population(
            best_chromosomes
        )

        # Add some completely new individuals for genetic diversity
        additional_chromosomes: List[List[float]] = self.get_new_chromosomes(
            len(self.population) - len(crossovered_chromosomes)
        )
        all_chromosomes: List[List[float]] = (
            crossovered_chromosomes + additional_chromosomes
        )

        # Apply mutations to the entire new population
        mutated_chromosomes: List[List[float]] = self.mutate_population(all_chromosomes)

        # Create CarRNA objects from the chromosomes
        new_population: List[CarRNA] = [
            CarRNA(chromosomes) for chromosomes in mutated_chromosomes
        ]

        # Store as current population for next generation
        self.population = new_population

        print(f"Generation: {self.generation} - Best car score: {best_car.get_score()}")

        return new_population

    def select_population(self, population: List[CarRNA]) -> List[List[float]]:
        """
        Selects 2 * population_size parents using roulette wheel selection.

        Args:
            population: Current population of neural networks

        Returns:
            A list of chromosome sets for the selected individuals
        """
        # Ensures scores bigger or equal to 0
        scores = [max(rna.get_score(), 0.0) for rna in population]
        total_score = sum(scores)

        # Avoids division by zero if all scores are 0
        if total_score == 0:
            probabilities = [1 / len(population)] * len(population)
        else:
            probabilities = [score / total_score for score in scores]

        selected_parents = random.choices(
            population, weights=probabilities, k=2 * self.population_size
        )

        return [parent.get_chromosomes() for parent in selected_parents]

    def crossover_population(self, population: List[List[float]]) -> List[List[float]]:
        """
        Returns the crossovered population applying simple crossover.

        Args:
            population: List of chromosome sets to crossover

        Returns:
            List of child chromosome sets after crossover
        """
        crossover_population: List[List[float]] = []

        for i in range(0, len(population), 2):
            parent1: List[float] = population[i]
            parent2: List[float] = population[i + 1]

            a = CROSSOVER_RATE
            b = 1 - CROSSOVER_RATE

            child: List[float] = [
                max(-1, min(1, a * x + b * y)) for x, y in zip(parent1, parent2)
            ]

            crossover_population.append(child)

        return crossover_population

    def get_new_chromosomes(self, amount: int) -> List[List[float]]:
        """
        Returns a list of different chromosome sets (each one a list of weights).

        Args:
            amount: Number of chromosome sets to generate

        Returns:
            A list of lists, where each inner list is a set of chromosomes for one car
        """
        chromosome_sets: List[List[float]] = []

        for i in range(amount):
            new_chromosomes: List[float] = [
                random.uniform(-1, 1) for _ in range(self.chromosomes_amount)
            ]
            chromosome_sets.append(new_chromosomes)

        return chromosome_sets

    def mutate_population(self, population: List[List[float]]) -> List[List[float]]:
        """
        Applies mutation to the population with some probability.
        Increases mutation rate as generations progress to avoid local optima.

        Args:
            population: List of chromosome sets

        Returns:
            The mutated population
        """
        # Increase mutation rate slightly based on generation (up to 5%)
        base_mutation_rate: float = 0.02  # 2% base mutation rate
        adaptive_rate: float = min(
            MUTATION_RATE, base_mutation_rate + (self.generation * 0.001)
        )

        for chromosomes in population:
            # For each chromosome set, decide if it should be mutated
            should_mutate: bool = random.random() < adaptive_rate

            if should_mutate:
                # Pick 1-3 genes to mutate (more impact)
                num_mutations: int = random.randint(1, 3)
                for _ in range(num_mutations):
                    mutation_point: int = random.randint(0, self.chromosomes_amount - 1)

                    # Apply mutation (either small or large change)
                    if random.random() < 0.7:  # 70% chance of small mutation
                        # Small adjustment to existing value (-0.2 to +0.2)
                        chromosomes[mutation_point] += random.uniform(-0.2, 0.2)
                        # Clamp value between -1 and 1
                        chromosomes[mutation_point] = max(
                            -1, min(1, chromosomes[mutation_point])
                        )
                    else:
                        # Complete replacement with new random value
                        chromosomes[mutation_point] = random.uniform(-1, 1)

        return population

    def should_stop(self, population: List[CarRNA]) -> bool:
        """
        Determine if the genetic algorithm should stop.

        Args:
            population: Current population

        Returns:
            Whether the algorithm should stop
        """
        pass

    def run(self) -> None:
        """Run the genetic algorithm."""
        pass

    def get_best_rna(self, population: List[CarRNA]) -> CarRNA:
        """
        Get the best neural network from the population.

        Args:
            population: Population to evaluate

        Returns:
            The best performing CarRNA
        """
        pass

    def get_generation(self) -> int:
        """Get the current generation number."""
        return self.generation
