from scipy.special import comb

import numpy as np
import matplotlib.pyplot as plt



class BezierCurve:
    """
    Class to encapsulate and simplify the funcitonality
    related to bezier curves.
    """
    def curve(control_points, n_points = 100):
        """
        Genera una curva de Bézier de grado (n-1) dada una lista de puntos de control.
        control_points: Lista de puntos de control (cada uno es una tupla (x, y)).
        n_points: Número de puntos a generar en la curva.
        """
        n = len(control_points)
        t_values = np.linspace(0, 1, n_points)  # Valores de t entre 0 y 1
        curve = np.zeros((n_points, 2))  # Para almacenar las coordenadas de la curva

        for i, t in enumerate(t_values):
            # Calculamos el valor de la curva en el tiempo t usando la fórmula de Bézier
            curve_point = np.zeros(2)
            for j, p in enumerate(control_points):
                b = comb(n-1, j) * (t**j) * ((1-t)**(n-1-j))  # Polinomio de Bernstein
                curve_point += b * np.array(p)
            curve[i] = curve_point

        return curve
    
    def generate_random_control_points(n, x_range = (-10, 10), y_range = (-10, 10), nonlinear = True):
        """
        Genera puntos de control aleatorios. Si `nonlinear` es True, se aplica una distorsión no lineal.
        n: Número de puntos de control.
        x_range, y_range: Rangos en los que generar los puntos.
        """
        control_points = []
        
        # Generamos puntos aleatorios para los nodos iniciales
        for i in range(n):
            x = np.random.uniform(*x_range)
            y = np.random.uniform(*y_range)
            control_points.append((x, y))
        
        if nonlinear:
            # Aplicar distorsión no lineal a los puntos de control
            # Usamos una función seno o coseno para aplicar distorsión
            for i in range(1, n-1):  # No distorsionamos los primeros y últimos puntos
                x, y = control_points[i]
                distorsion_factor = np.sin(i / (n-1) * np.pi)  # Seno para variación no lineal
                control_points[i] = (x + distorsion_factor * np.random.uniform(-5, 5),
                                    y + distorsion_factor * np.random.uniform(-5, 5))
        
        return control_points