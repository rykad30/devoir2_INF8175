import solver_naive
import random
import time

MAX_ITER = 100
TIME_LIMIT = 60



def solve(schedule, restarts=10):
    """
    Multi-start: on construit plusieurs solutions initiales (en mélangeant l'ordre
    des cours), on lance recherche locale sur chacune et on garde la meilleure.
    """

    # baseline : solution naive (1 créneau par cours)
    start_time = time.time()
    best_solution = solver_naive.solve(schedule)
    best_score = evaluate(schedule, best_solution)

    # plusieurs redémarrages aléatoires
    for _ in range(restarts):

        elapsed = time.time() - start_time
        print(f"RESTART : {elapsed:.2f}s - best score so far: {best_score}")
        if elapsed >= TIME_LIMIT:
            print(f"⏰ Timeout after {elapsed:.2f}s in local search.")
            break

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
        current_solution = cherche_min_local(schedule, init, start_time)

        # comparer via evaluate (pénalise fortement les conflits)
        curr_score = evaluate(schedule, current_solution)
        if curr_score < best_score:
            best_solution = current_solution.copy()
            best_score = curr_score

    return best_solution



def cherche_min_local(schedule, initial_solution, start_time):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    # Add here your agent
     
    current_solution = initial_solution.copy()
    current_score = evaluate(schedule, current_solution)
    nb_it = current_score +1
    for i in range(1, nb_it):

        elapsed = time.time() - start_time
        print(f"time : {elapsed:.2f}s - best score so far: {current_score}")
        if  elapsed >= TIME_LIMIT:
            print(f"⏰ Timeout after {elapsed:.2f}s in local search.")
            break
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
    sample_rate = 0.1
    courses = list(schedule.course_list)
    random.shuffle(courses)
    n_creneaux = schedule.get_n_creneaux(solution)
    n_courses = len(courses)

    # Adaptive sample rate
    if n_courses <= 100:
        sample_rate = 1.0
    elif n_courses >= 200:
        sample_rate = 0.1
        courses = courses[:200]
    else:
        # Linear interpolation between 1.0 and 0.1
        sample_rate = 1.0 - ((n_courses - 100) / 400) * 0.9
    
    for course in courses:
        conflicts = schedule.get_node_conflicts(course)
        for i in range(1,n_creneaux+1):
            if i == solution[course]:
                continue
            if all(solution[conflict] != i for conflict in conflicts):
                    if random.random() < sample_rate:
                        neighbor = solution.copy()
                        neighbor[course] = i
                        neighbors.append(neighbor)
                        if len(neighbors) > 500:
                            break

    
    return neighbors

