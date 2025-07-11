# !DISCLAIMER!
# the idea behind this code was taken from an assignment, where we were asked to implement the entire GA and the necessary parts of the (given) EA.
# however, for originality, i've gotten rid of any of the assignment code, and implemented the entire algorithm from scratch (with a different approach).
# the parts i haven't changed, are the parts that i originally created myself in the assignment as well - therefore this code is 100% my own work.

import numpy as np
import matplotlib.pyplot as plt

example_solution = [2, 4, 1, 3]

def visualize_solution(solution):
    """visualize the placement of queens on the chessboard."""

    # INITIALIZING A LIST OF N LISTS (for NxN board)
    outputs = []
    for _ in range(len(solution)):
        output = []     # initialize N lists (for N)
        for _ in range(len(solution)):
            output.append(0)    # append 0 to all N lists
        outputs.append(output)   # combine all N lists into one list,
                        # resulting in a list of N lists: [[], [], [], []] for N=4

    # REPLACING APPROPRIATE POSITIONS WITH QUEENS
    for row in range(len(outputs)):     # iterate over each row (each list)
        col = solution[row] - 1         # the column we are interested in is stored in the row-th index
                                        # of "solution" with a -1 to convert back to 0-index

        outputs[col][row] = 'Q'
        continue                        # via the column we computed, the col-th row-th index of
                                        # the outputs is then set to 'Q' for queen

    # PRINTING VISUALIZATION
    for row in outputs:               # iterate over each row
        print(str(row).replace(',', '').replace("'", ""))  # print the str. version of the list with the
                                                        # commas and quotation marks replaced by empty strings.

def evaluate_solution_n_queens(solution):
    """calculate the fitness of an solution."""

    # since the representation itself avoids horizontal and vertical conflicts,
    # the only conflicts left we have to account for are the diagonal conflicts.

    conflicts = 0                     # initialize conflict amount as 0
    for i in range(len(solution)):    # iterate over the i-th and the i+1th element
                                    # (i+1 to ensure different than i itself)
        for j in range(i + 1, len(solution)):
            if abs(i - j) == abs(solution[i] - solution[j]):  # check for diagonal conflict of the two elements
                conflicts += 1        # if so, increment amount by 1

    max_conflicts = (len(solution) * (len(solution)-1)) / 2
    fitness = 1.0 - (conflicts / max_conflicts)

    # source (INSPIRATION FOR DIAGONAL CONFLICT TRICK): https://www.zemris.fer.hr/~golub/clanci/eurocon2003.pdf
    # source (FITNESS COMPUTATION): https://aljrico.github.io/blog/genetic-algorithms/

    return fitness

print("Genotype (solution representation):", example_solution)
print("Phenotype (solution visualization):")
visualize_solution(example_solution)
print("Solution fitness", evaluate_solution_n_queens(example_solution))

#initialize a population of solutions for the N queens problem where num_dims = N
def initialization_n_queens(population_size, num_of_dims):
    """generate a population of solutions."""

    x = []        # initialize x as empty list
    for _ in range(population_size):      # iterate over the population size
        x.append(np.random.permutation(num_of_dims) + 1)  # and add a random permutation depending on the nr. dims + 1 (because 0-indexed)

    return x


def evaluation_n_queens(x):
    """evaluate the whole population and return the fitness of each."""
    return [evaluate_solution_n_queens(solution) for solution in x]


def crossover_n_queens(x_parents, p_crossover):
    """perform crossover to create offsprings."""

    offspring = []            # initialize offsprings to store in as list
    chance = np.random.rand() # initialize a chance (float between 0 and 1) for crossover

    for i in range(0, len(x_parents), 2): # step size 2 --> skips every 2nd element
        parent1, parent2 = x_parents[i], x_parents[i+1] # extract parent1 and parent2

        if chance < p_crossover:          # if chance condition is passed,
                            # we use Order (1) crossover (OX),
                            # this crossover method is specifically tailored for permutation problems
                            # essentially, we take one gene from the first parent, and fill the rest
                            # of the genes of the child with the genes of the second parent.

            size = len(parent1)   # extract gene size from parent
            cx1, cx2 = sorted(np.random.choice(size, 2, replace=False)) # randomly choose crossover points/genes
            child1 = [-1] * size    # initialize children with 'empty' values, wrt. to the size of the genes of the parent
            child2 = [-1] * size
            child1[cx1:cx2+1] = parent1[cx1:cx2+1]  # copy the selected slice of genes into the children from the parents
            child2[cx1:cx2+1] = parent2[cx1:cx2+1]
            # at this point, the children contain -1 for every gene except the chosen genes above

            # filling in the rest of the genes for child1
            p2_idx = (cx2+1) % size       # cx2 stands for the end of the part of the genes we extracted
                                        # and since python uses 0-indexing, we add 1.
                                        # the modulo operator afterwards, ensures that if the remaining genes
                                        # go beyond the last valid index, continues back from the start or 'wraps around'
                                        # ensuring we don't end up out of index bounds.
                                        # p2_idx gives us the starting index in parent2 from which we fill the rest of the genes in child1 in
            c1_idx = (cx2+1) % size       # and c1_idx gives us the point where we will start inserting new genes
                                        # from parent2 after the crossover slice is over, also with the modulo operator to ensure no out-of-bounds index.
            while -1 in child1:           # iterate until no 'empty' values/genes left in child
                if parent2[p2_idx] not in child1: # if the selected gene is not inside the child, (selected gene being accessed from parent2 with p2_idx)
                    child1[c1_idx] = parent2[p2_idx] # then place the gene in the next available spot
                    c1_idx = (c1_idx + 1) % size    # move to next index for next gene
                p2_idx = (p2_idx + 1) % size    # move to next gene in parent2

            # filling in the rest of the genes for child2
            p1_idx = (cx2+1) % size     # same operations as above, only for child2 with the remaining genes from parent1.
            c2_idx = (cx2+1) % size      # the idea is very simple in essence, simply take an index X in parent 1, insert that index in child1,
            while -1 in child2:         # and take the rest from parent2 - that is all this crossover operation does.
                if parent1[p1_idx] not in child2:
                    child2[c2_idx] = parent1[p1_idx]
                    c2_idx = (c2_idx + 1) % size
                p1_idx = (p1_idx + 1) % size

            offspring.extend([child1, child2])    # when crossover happens, we append them to the offsprings.
                                        # otherwise,
        else:                 # if crossover chance condition fails
            offspring.extend([parent1, parent2])     # we continue with the same parents

    # source (OX1 CROSSOVER): https://www.baeldung.com/cs/ga-order-one-crossover

    return offspring


def mutation_n_queens(x, mutation_rate):
    """apply mutation to an individual."""

    for i in range(len(x)):         # iterate over population
        if np.random.rand() < mutation_rate:    # set a chance condition
            idx1, idx2 = sorted(np.random.choice(len(x[i]), 2, replace=False)) # to mutate, we pick two genes with random.choice, which we do
                                                                        # with setting the size to 2,to get two indexes/genes.
                                                                        # to ensure that the two indexes/genes are different from
                                                                        # eachother, we set replace to False to ensure that the genes are unique,
                                                                        # that is, we don't 'sample with replacement'
                                                                        # furthermore, the genes selected might be in any order since its randomized.
                                                                        # therefore we sort the two indexes to ensure the smaller index is ranked first
                                                                        # for correct slicing.
            permutation = x[i][idx1:idx2+1]          # extracts the genes from idx1 until idx2 (+1 since 0-indexed) in x[i] (x[i] is one individual)
            np.random.shuffle(permutation)        # shuffles the extracted genes (mutates them)
            x[i][idx1:idx2+1] = permutation   # swap the old gene with the new permutation (mutated gene)

        # this approach ensures to preserve permutation validity, since we do not randomly change the values of the genes (which are numbers)
        # but instead we scramble them, so each number still appears only once to avoid conflicts.
        # this is a critical point since this specific problem is a permutation problem.

    return x


def parent_selection_n_queens(x, f):
    """select parents for the next generation"""

    tournament_size = 3   # initializations
    x_parents = []
    f_parents = []

    for _ in range(len(x)):   # iterate over population
        competitors = np.random.choice(len(x), tournament_size)   # randomly pick competitors in compliance w/ the tournament size
        best_idx = competitors[np.argmax((f)[c] for c in competitors)] # extract best idx with respect to its fitness
        x_parents.append(x[best_idx])   # add values to respective lists
        f_parents.append(f[best_idx])

    # source: same as the tournament selection link above, https://www.baeldung.com/cs/ga-tournament-selection

    return x_parents, f_parents


def survivor_selection_n_queens(x, f, x_offspring, f_offspring):
    """select the survivors, for the population of the next generation"""


    combined_x = x + x_offspring    # combine parents and offspring
    combined_f = f + f_offspring    # and their corr. fitnesses
    next_x, next_f = [], []         # initializations
    for _ in range(len(x)):         # iterate over population
        competitors = np.random.choice(len(combined_x), 2)      # randomly pick competitors in compliance w/ the tournament size (2 in this case)
        best_idx = competitors[np.argmax([combined_f[c] for c in competitors])]  # extract best idx with respect to its combined fitness
        next_x.append(combined_x[best_idx])     # append found values to respective lists
        next_f.append(combined_f[best_idx])

    # source: again same as the tournament selection link above, however this time instead of
    # replacing the worst offspring with the best parents, we replace the worst parents with
    # the best offspring - this ensures diversity, however does not use sorting for an "optimal" selection.
    # https://www.baeldung.com/cs/ga-tournament-selection

    return next_x, next_f

def ea_n_queens(pop_size, max_evals, p_cx, m_rate, board_size):
    """Evolutionary algorithm for solving N-Queens."""

    max_generations = max_evals // pop_size

    # === INITIAL POPULATION ===
    population = initialization_n_queens(pop_size, board_size)
    fitnesses = evaluation_n_queens(population)

    # store best-so-far individual and its fitness
    best_individuals = [population[np.argmax(fitnesses)]]
    best_scores = [max(fitnesses)]

    # === EVOLUTION LOOP ===
    for _ in range(max_generations - 1):

        # step 1: select parents
        selected_parents, selected_scores = parent_selection_n_queens(population, fitnesses)

        # step 2: apply crossover
        offspring = crossover_n_queens(selected_parents, p_cx)

        # step 3: apply mutation
        offspring = mutation_n_queens(offspring, m_rate)

        # step 4: evaluate offspring
        offspring_scores = evaluation_n_queens(offspring)

        # step 5: choose survivors
        population, fitnesses = survivor_selection_n_queens(population, fitnesses, offspring, offspring_scores)

        # step 6: check if we improved
        current_best_idx = np.argmax(fitnesses)
        current_best_fit = fitnesses[current_best_idx]
        current_best = population[current_best_idx]

        if current_best_fit > best_scores[-1]:
            best_individuals.append(current_best)
            best_scores.append(current_best_fit)
        else:
            # keep previous best if no improvement
            best_individuals.append(best_individuals[-1])
            best_scores.append(best_scores[-1])

    return best_individuals, best_scores

def solve_until_perfect(N=8, population_size=100, max_fit_evals=10000, p_crossover=0.8, m_rate=0.1):
    attempts = 0
    while True:
        attempts += 1
        print(f"\nAttempt {attempts}...")

        x_best, f_best = ea_n_queens(
            pop_size=population_size,
            max_evals=max_fit_evals,
            p_cx=p_crossover,
            m_rate=m_rate,
            board_size=N
        )

        final_solution = list(x_best[-1])
        final_fitness = evaluate_solution_n_queens(final_solution)

        print(f"  → Fitness: {final_fitness:.4f}")
        if final_fitness == 1.0:
            print("\n✅ Perfect solution found!")
            print("Final solution:", final_solution)
            print("Terminal board:")
            visualize_solution(final_solution)

            # matplotlib board
            board_size = len(final_solution)
            _, ax = plt.subplots(figsize=(6, 6))
            ax.set_xlim(0, board_size)
            ax.set_ylim(0, board_size)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f"N = {N} | Fitness = 1.0")

            for row in range(board_size):
                for col in range(board_size):
                    color = 'white' if (row + col) % 2 == 0 else 'gray'
                    rect = plt.Rectangle((col, board_size - row - 1), 1, 1, facecolor=color)
                    ax.add_patch(rect)

            for row, col1 in enumerate(final_solution):
                col = col1 - 1
                ax.text(col + 0.5, board_size - row - 0.5, '♛', ha='center', va='center', fontsize=20, color='red')

            plt.axis('off')
            plt.show()
            break

if __name__ == "__main__":
    solve_until_perfect(N=4)
    solve_until_perfect(N=8)
    solve_until_perfect(N=16)