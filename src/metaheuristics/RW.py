import random

from fitness.schaffer_N4 import schaffer_N4


def objective(x):
    return schaffer_N4(x[0], x[1])


def rw(left_limit, right_limit, epochs, step_size):
    best = [
        random.uniform(left_limit, right_limit),
        random.uniform(left_limit, right_limit),
    ]
    scores = []

    for _ in range(epochs):
        tmp = [
            best[0] + random.uniform(left_limit, right_limit) * step_size,
            best[1] + random.uniform(left_limit, right_limit) * step_size,
        ]
        best = tmp
        scores.append(objective(best))

    return best, objective(best), scores


# print("Result:")
# print("x:", best)
# print("Fitness:", objective(best))
# pyplot.plot(scores, ".-")
# pyplot.xlabel("Improvement Number")
# pyplot.ylabel("Evaluation f(x)")
# pyplot.savefig("./plots/RW.png")
