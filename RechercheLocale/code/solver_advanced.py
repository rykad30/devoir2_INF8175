import solver_naive

"""
Contraintes dures: 
- Un professeur ne peut pas donner deux cours en même temps
- Etudiants ne peuvent pas avoir deux cours en même temps

Contraintes molles:
- Minimiser le nombre de créneaux utilisés

Méthode :
- Générer une solution initiale avec l'algorithme glouton (solver_naive)
- Améliorer la solution avec une recherche locale   :
    - Ensemble des voisins : déplacer un cours dans un autre créneau
    - fonction d'évaluation : nombre de créneaux utilisés + nombre de conflits (pénalité élevée)
    - Critère d'arrêt : pas d'amélioration possible

"""

def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    init_solution = solver_naive.solve(schedule)

    raise Exception("Agent is not implemented")

def evaluate(solution):
    """
    Evaluate the quality of a solution
    :param solution: a list of tuples of the form (c,t) where c is a course and t a time slot.
    :return: a float representing the quality of the solution (the lower the better)
    """
    raise Exception("Agent is not implemented")

def get_neighbors(solution):
    """
    Get the neighbors of a solution
    :param solution: a list of tuples of the form (c,t) where c is a course and t a time slot.
    :return: a list of neighbors (each neighbor is a list of tuples of the form (c,t) where c is a course and t a time slot.)
    """
    raise Exception("Agent is not implemented")

def choose_best_neighbor(neighbors):
    """
    Choose the best neighbor among a list of neighbors
    :param neighbors: a list of neighbors (each neighbor is a list of tuples of the form (c,t) where c is a course and t a time slot.)
    :return: the best neighbor (a list of tuples of the form (c,t) where c is a course and t a time slot.)
    """
    raise Exception("Agent is not implemented")