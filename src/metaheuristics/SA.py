# https://machinelearningmastery.com/simulated-annealing-from-scratch-in-python/
from numpy import asarray
from numpy import exp
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

from fitness.schaffer_N4 import schaffer_N4


# objective function
def objective(x):
    return schaffer_N4(x[0], x[1])


# simulated annealing algorithm
def simulated_annealing(objective, bounds, n_iterations, step_size, temp):
    # generate an initial point
    best = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
    # evaluate the initial point
    best_eval = objective(best)
    # current working solution
    curr, curr_eval = best, best_eval
    scores = list()
    # run the algorithm
    for i in range(n_iterations):
        # take a step
        candidate = curr + randn(len(bounds)) * step_size
        # evaluate candidate point
        candidate_eval = objective(candidate)
        # check for new best solution
        if candidate_eval < best_eval:
            # store new best point
            best, best_eval = candidate, candidate_eval
            # keep track of scores
            # report progress
            # print(">%d f(%s) = %.5f" % (i, best, best_eval))
        scores.append(best_eval)
        # difference between candidate and current point evaluation
        diff = candidate_eval - curr_eval
        # calculate temperature for current epoch
        t = temp / float(i + 1)
        # calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
        # check if we should keep the new point
        if diff < 0 or rand() < metropolis:
            # store the new current point
            curr, curr_eval = candidate, candidate_eval
    return [best, best_eval, scores]


def sa(left_limit, right_limit, epochs, step_size):
    # seed the pseudorandom number generator
    seed(1)
    # define range for input
    bounds = asarray([[left_limit, right_limit], [left_limit, right_limit]])
    # define the total iterations
    n_iterations = epochs
    # define the maximum step size
    step_size = step_size
    # initial temperature
    temp = 10
    # perform the simulated annealing search
    best, score, scores = simulated_annealing(
        objective, bounds, n_iterations, step_size, temp
    )

    return best, score, scores


# print("Done!")
# print("f(%s) = %f" % (best, score))
# # line plot of best scores
# pyplot.plot(scores, ".-")
# pyplot.xlabel("Improvement Number")
# pyplot.ylabel("Evaluation f(x)")
# pyplot.savefig("./plots/SA.png")
