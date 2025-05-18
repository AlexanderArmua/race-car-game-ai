import math
from enum import Enum

NEURONS_FORMAT = [3, 3, 1] #[ (0,1,2), (3,4,5), (6) ]

class CarRNAResult(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

activation_function = math.tanh
class CarRNA:
    def __init__(self, chromsomes: list[float]):
        if len(chromsomes) != NEURONS_FORMAT[0] * NEURONS_FORMAT[1] + NEURONS_FORMAT[1] * NEURONS_FORMAT[2]:
            raise ValueError(f"Chromosomes amount must be equal to the chromosomes amount: {len(chromsomes)} != {NEURONS_FORMAT[0] * NEURONS_FORMAT[1] + NEURONS_FORMAT[1] * NEURONS_FORMAT[2]}")

        self.absolute_score = 0
        self.chromsomes = chromsomes

        # Create empty neurons for input
        # LAYER 0
        self.neurons = [0 for _ in range(NEURONS_FORMAT[0])]

        # Create empty weights
        # LAYER 1
        self.weight_l0_n0_to_l1_n0 = chromsomes[0]
        self.weight_l0_n0_to_l1_n1 = chromsomes[1]
        self.weight_l0_n0_to_l1_n2 = chromsomes[2]
        self.weight_l0_n1_to_l1_n0 = chromsomes[3]
        self.weight_l0_n1_to_l1_n1 = chromsomes[4]
        self.weight_l0_n1_to_l1_n2 = chromsomes[5]
        self.weight_l0_n2_to_l1_n0 = chromsomes[6]
        self.weight_l0_n2_to_l1_n1 = chromsomes[7]
        self.weight_l0_n2_to_l1_n2 = chromsomes[8]
        
        # LAYER 2
        self.weight_l1_n0_to_l2_n0 = chromsomes[9]
        self.weight_l1_n1_to_l2_n0 = chromsomes[10]
        self.weight_l1_n2_to_l2_n0 = chromsomes[11]

    def get_chromosomes(self) -> list[float]:
        return self.chromsomes
    
    def get_result(self, inputs: list[float]) -> float:
        """
        Get the result of the RNA.
        
        Args:
            inputs: List of inputs
        """
        if len(inputs) != NEURONS_FORMAT[0]:
            raise ValueError("Inputs length must be equal to the first layer neurons amount")

        value_l1_n0 = activation_function(self.weight_l0_n0_to_l1_n0 * inputs[0] + self.weight_l0_n1_to_l1_n0 * inputs[1] + self.weight_l0_n2_to_l1_n0 * inputs[2])
        value_l1_n1 = activation_function(self.weight_l0_n0_to_l1_n1 * inputs[0] + self.weight_l0_n1_to_l1_n1 * inputs[1] + self.weight_l0_n2_to_l1_n1 * inputs[2])
        value_l1_n2 = activation_function(self.weight_l0_n0_to_l1_n2 * inputs[0] + self.weight_l0_n1_to_l1_n2 * inputs[1] + self.weight_l0_n2_to_l1_n2 * inputs[2])

        value_l2_n0 = activation_function(self.weight_l1_n0_to_l2_n0 * value_l1_n0 + self.weight_l1_n1_to_l2_n0 * value_l1_n1 + self.weight_l1_n2_to_l2_n0 * value_l1_n2)

        return value_l2_n0

    def get_interpretated_result(self, inputs: list[float]) -> CarRNAResult:
        """
        Get the interpretated result of the RNA.
        
        Args:
            inputs: List of inputs
        """
        result = self.get_result(self.normalize_inputs(inputs))

        if result < -0.33:
            return CarRNAResult.LEFT
        elif result < 0.3:
            return CarRNAResult.STRAIGHT
        else:
            return CarRNAResult.RIGHT

    def normalize_inputs(self, inputs: list[float | None]) -> list[float]:
        """
        Normalize the inputs to be between 0 and 1.
        
        Args:
            inputs: List of inputs
        """
        return [input / 1000 if input is not None else 0 for input in inputs]

    def increase_score(self, new_value: int):
        self.absolute_score += new_value
    
    def get_score(self) -> int:
        return self.absolute_score
        