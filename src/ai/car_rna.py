import math
from enum import Enum
from typing import Callable, List, Optional, TypeVar, Union

NEURONS_FORMAT: List[int] = [3, 3, 1]  # [ (0,1,2), (3,4,5), (6) ]


class CarRNAResult(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


activation_function: Callable[[float], float] = math.tanh


class CarRNA:
    def __init__(self, chromsomes: List[float]) -> None:
        if (
            len(chromsomes)
            != NEURONS_FORMAT[0] * NEURONS_FORMAT[1]
            + NEURONS_FORMAT[1] * NEURONS_FORMAT[2]
        ):
            raise ValueError(
                f"Chromosomes amount must be equal to the chromosomes amount: {len(chromsomes)} != {NEURONS_FORMAT[0] * NEURONS_FORMAT[1] + NEURONS_FORMAT[1] * NEURONS_FORMAT[2]}"
            )

        self.absolute_score: int = 0
        self.chromsomes: List[float] = chromsomes

        # Create empty neurons for input
        # LAYER 0
        self.neurons: List[float] = [0 for _ in range(NEURONS_FORMAT[0])]

        # Create empty weights
        # LAYER 1
        self.weight_l0_n0_to_l1_n0: float = chromsomes[0]
        self.weight_l0_n0_to_l1_n1: float = chromsomes[1]
        self.weight_l0_n0_to_l1_n2: float = chromsomes[2]
        self.weight_l0_n1_to_l1_n0: float = chromsomes[3]
        self.weight_l0_n1_to_l1_n1: float = chromsomes[4]
        self.weight_l0_n1_to_l1_n2: float = chromsomes[5]
        self.weight_l0_n2_to_l1_n0: float = chromsomes[6]
        self.weight_l0_n2_to_l1_n1: float = chromsomes[7]
        self.weight_l0_n2_to_l1_n2: float = chromsomes[8]

        # LAYER 2
        self.weight_l1_n0_to_l2_n0: float = chromsomes[9]
        self.weight_l1_n1_to_l2_n0: float = chromsomes[10]
        self.weight_l1_n2_to_l2_n0: float = chromsomes[11]

    def get_chromosomes(self) -> List[float]:
        """Return the chromosome weights."""
        return self.chromsomes

    def get_result(self, inputs: List[float]) -> float:
        """
        Get the result of the RNA.

        Args:
            inputs: List of inputs

        Returns:
            The output value of the neural network

        Raises:
            ValueError: If the inputs length doesn't match the input layer size
        """
        if len(inputs) != NEURONS_FORMAT[0]:
            raise ValueError(
                "Inputs length must be equal to the first layer neurons amount"
            )

        value_l1_n0: float = activation_function(
            self.weight_l0_n0_to_l1_n0 * inputs[0]
            + self.weight_l0_n1_to_l1_n0 * inputs[1]
            + self.weight_l0_n2_to_l1_n0 * inputs[2]
        )
        value_l1_n1: float = activation_function(
            self.weight_l0_n0_to_l1_n1 * inputs[0]
            + self.weight_l0_n1_to_l1_n1 * inputs[1]
            + self.weight_l0_n2_to_l1_n1 * inputs[2]
        )
        value_l1_n2: float = activation_function(
            self.weight_l0_n0_to_l1_n2 * inputs[0]
            + self.weight_l0_n1_to_l1_n2 * inputs[1]
            + self.weight_l0_n2_to_l1_n2 * inputs[2]
        )

        value_l2_n0: float = activation_function(
            self.weight_l1_n0_to_l2_n0 * value_l1_n0
            + self.weight_l1_n1_to_l2_n0 * value_l1_n1
            + self.weight_l1_n2_to_l2_n0 * value_l1_n2
        )

        return value_l2_n0

    def get_interpretated_result(self, inputs: List[Optional[float]]) -> CarRNAResult:
        """
        Get the interpretated result of the RNA.

        Args:
            inputs: List of inputs (sensor distances)

        Returns:
            The interpreted action (LEFT, STRAIGHT, or RIGHT)
        """
        result: float = self.get_result(self.normalize_inputs(inputs))

        if result < -0.33:
            return CarRNAResult.LEFT
        elif result < 0.3:
            return CarRNAResult.STRAIGHT
        else:
            return CarRNAResult.RIGHT

    def normalize_inputs(self, inputs: List[Optional[float]]) -> List[float]:
        """
        Normalize the inputs to be between 0 and 1.

        Args:
            inputs: List of inputs (sensor distances, possibly None)

        Returns:
            Normalized inputs list
        """
        return [input / 100 if input is not None else 0 for input in inputs]

    def increase_score(self, new_value: int) -> None:
        """
        Increase the car's score.

        Args:
            new_value: Value to add to the score
        """
        self.absolute_score += new_value

    def get_score(self) -> int:
        """Get the current score of this neural network."""
        return self.absolute_score
