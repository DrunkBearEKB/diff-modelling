from typing import Dict, List


class TrajectoryConfiguration:
    def __init__(self, point: str, color: str, tend_to_rest: bool):
        self.point = point
        self.color = color
        self.tend_to_rest = tend_to_rest


class DataObjConfiguration:
    def __init__(self, name: str, parameters: Dict[str, float],
                 trajectories: List[TrajectoryConfiguration],
                 plot_separate_line: bool):
        self.name = name
        self.parameters = parameters
        self.trajectories = trajectories
        self.plot_separate_line = plot_separate_line


class DataSetConfiguration:
    def __init__(self, values: List[DataObjConfiguration]):
        self.values = values


class ExpressionsConfiguration:
    def __init__(self, initial: List[str], simplified: List[str],
                 variables: List[str], parameters_variables: List[str]):
        self.initial = initial
        self.simplified = simplified
        self.variables = variables
        self.parameters_variables = parameters_variables


class PlottingConfiguration:
    def __init__(self, show_legend: bool, show_grid: bool):
        self.show_legend = show_legend
        self.show_grid = show_grid


class DataConfiguration:
    def __init__(self, expressions: ExpressionsConfiguration,
                 amount_iterations: int, h_step: float,
                 dataset: DataSetConfiguration,
                 plotting: PlottingConfiguration):
        self.expressions = expressions
        self.amount_iterations = amount_iterations
        self.h_step = h_step
        self.dataset = dataset
        self.plotting = plotting
