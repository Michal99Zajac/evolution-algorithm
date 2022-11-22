# https://machinelearningmastery.com/stochastic-hill-climbing-in-python-from-scratch/
from numpy import asarray
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

from fitness.schaffer_N4 import schaffer_N4


# objective function
def objective(x):
    return schaffer_N4(x[0], x[1])


# hill climbing local search algorithm
def hillclimbing(objective, bounds, n_iterations, step_size):
    # generate an initial point
    solution = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
    # evaluate the initial point
    solution_eval = objective(solution)
    # run the hill climb
    scores = list()
    scores.append(solution_eval)
    for _ in range(n_iterations):
        # take a step
        candidate = solution + randn(len(bounds)) * step_size
        # evaluate candidate point
        candidte_eval = objective(candidate)
        # check if we should keep the new point
        if candidte_eval <= solution_eval:
            # store the new point
            solution, solution_eval = candidate, candidte_eval
            # keep track of scores
            # report progress
            # print(">%d f(%s) = %.5f" % (i, solution, solution_eval))
        scores.append(solution_eval)
    return [solution, solution_eval, scores]


def hl(left_limit, right_limit, epochs, step_size):
    # seed the pseudorandom number generator
    seed(5)
    # define range for input
    bounds = asarray([[left_limit, right_limit], [left_limit, right_limit]])
    # define the total iterations
    n_iterations = epochs
    # define the maximum step size
    step_size = step_size
    # perform the hill climbing search
    best, score, scores = hillclimbing(objective, bounds, n_iterations, step_size)

    return best, score, scores


# print("Done!")
# print("f(%s) = %f" % (best, score))
# # line plot of best scores
# pyplot.plot(scores, ".-")
# pyplot.xlabel("Improvement Number")
# pyplot.ylabel("Evaluation f(x)")
# pyplot.savefig("./plots/HL.png")
