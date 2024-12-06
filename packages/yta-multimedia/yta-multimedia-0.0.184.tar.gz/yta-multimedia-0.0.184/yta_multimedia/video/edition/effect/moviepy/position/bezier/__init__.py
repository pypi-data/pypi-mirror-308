from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator

import bezier
import numpy as np
import matplotlib.pyplot as plt


class BezierControlNode:
    """
    Class to represent a bezier control node, that is a 
    coordinate in a normalized 2D system (between 0.0 
    and 1.0). This nodes are used to build the bezier
    curve.

    This is represented by a pair of 'x' and 'y' values
    that must be between 0.0 and 1.0.
    """
    x: float
    """
    The 'x' axis control node (coordinate) value.
    """
    y: float
    """
    The 'y' axis control node (coordinate) value.
    """

    def __init__(self, x: float, y: float):
        if not NumberValidator.is_number_between(x, 0.0, 1.0) or not NumberValidator.is_number_between(y, 0.0, 1.0):
            raise Exception(f'The provided "x" and/or "y" parameters {str(x)},{str(y)} values are not between 0.0 and 1.0.')
        
        self.x = x
        self.y = y

class BezierCurve:
    """
    Class to encapsulate and simplify the funcitonality
    related to bezier curves.
    """
    curve: bezier.Curve
    """
    The instance of the Curve from the bezier library.
    """

    def __init__(self, control_nodes: list[BezierControlNode]):
        if not PythonValidator.is_list(control_nodes):
            if not PythonValidator.is_instance(control_nodes, BezierControlNode):
                raise Exception('The provided "control_nodes" parameter is not a list of BezierControlNode instances nor a single BezierControlNode instance.')
            else:
                control_nodes = [control_nodes]

        if any(not PythonValidator.is_instance(control_node, BezierControlNode) for control_node in control_nodes):
            raise Exception(f'At least one of the provided "control_nodes" parameter is not a BezierControlNode instance.')
        
        nodes_np_array = [[control_node.x for control_node in control_nodes], [control_node.y for control_node in control_nodes]]
        degree = len(control_nodes) - 1

        self.curve = bezier.Curve(nodes_np_array, degree = degree)
        # TODO: Anything else (?)

    def get_curve_point_value(self, t: float):
        """
        Obtain the curve value for the provided 't' that must
        be a value between 0.0 and 1.0.
        """
        if not NumberValidator.is_number_between(t, 0.0, 1.0):
            raise Exception(f'The provided "t" parameter value "{str(t)}" is not a valid value. Must be between 0.0 and 1.0.')

        return self.curve.evaluate(t)

    def plot(self, do_show_control_nodes: bool = True):
        """
        Plot and show the bezier curve using matplotlib.
        """
        # Set 100 points of the curve to draw it
        curve_points = self.curve.evaluate_multi(np.linspace(0, 1, 100))
        nodes = self.curve.nodes

        plt.plot(curve_points[0], curve_points[1], label = "Bezier curve", color = 'b')

        if do_show_control_nodes:
            plt.scatter(nodes[0], nodes[1], color = 'r', label = "Control nodes")
            # Draw control nodes lines in-between
            for i in range(len(nodes[0]) - 1):
                plt.plot([nodes[0][i], nodes[0][i + 1]], [nodes[1][i], nodes[1][i + 1]], 'r--')

        plt.legend()
        plt.title(f'Bezier curve (degree = {str(len(nodes[0]) - 1)})')
        plt.grid(True)
        plt.axis('equal')
        plt.show()