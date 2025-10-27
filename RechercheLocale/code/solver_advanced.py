import solver_naive
import random

def solve(schedule, restarts=10, max_iters=1000, L_strategy='filter_free', Q_strategy='best', sample_k=100):
    """
    Multi-start: on construit plusieurs solutions initiales (en mélangeant l'ordre
    des cours), on lance recherche locale sur chacune et on garde la meilleure.
    """

    # baseline : solution naive (1 créneau par cours)
    best_solution = solver_naive.solve(schedule)
    best_score = evaluate(schedule, best_solution)

    # plusieurs redémarrages aléatoires
    for _ in range(restarts):
        # convertir le NodeView en liste puis mélanger
        courses = list(schedule.course_list)
        random.shuffle(courses)

        # construire une solution initiale avec un créneau unique par cours (1..n)
        init = {}
        slot = 1
        for c in courses:
            init[c] = slot
            slot += 1

        # lancer la recherche locale depuis cette initialisation
        current_solution = cherche_min_local(schedule, init, max_iters, L_strategy, Q_strategy, sample_k)

        # comparer via evaluate (pénalise fortement les conflits)
        curr_score = evaluate(schedule, current_solution)
        if curr_score < best_score:
            best_solution = current_solution.copy()
            best_score = curr_score

    return best_solution



def cherche_min_local(schedule, initial_solution, max_iters=1000, L_strategy='filter_free', Q_strategy='best', sample_k=100):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
     
    current_solution = initial_solution.copy()
    current_score = evaluate(schedule, current_solution)
    for i in range(1, max_iters + 1):
        # N(s) : generate neighbourhood G
        neighbors = get_neighbors(schedule, current_solution)
        if not neighbors:
            break
        best_neighbor, best_score = choose_best_neighbor(schedule, neighbors)
        if best_score >= current_score:
            break
        current_solution = best_neighbor
        current_score = best_score
    return current_solution



def choose_best_neighbor(schedule, neighbors):
    best_neighbor = None
    best_score = float('inf')
    for neighbor in neighbors:
        score = evaluate(schedule, neighbor)
        if score < best_score:
            best_score = score
            best_neighbor = neighbor
    return best_neighbor, best_score

def evaluate(schedule, solution):
    nb_conflicts = 0
    for course_1, course_2 in schedule.conflict_list:
        if solution[course_1] == solution[course_2]:
            nb_conflicts += 1
    nb_creneaux = schedule.get_n_creneaux(solution)
    return 1000*nb_conflicts + nb_creneaux

def get_neighbors(schedule, solution):

    neighbors = []
    for course in schedule.course_list:
        conflicts = schedule.get_node_conflicts(course)
        for i in range(1,schedule.get_n_creneaux(solution)+1):
            if i == solution[course]:
                continue
            if all(solution[conflict] != i for conflict in conflicts):
                neighbor = solution.copy()
                neighbor[course] = i
                neighbors.append(neighbor)
    return neighbors




























