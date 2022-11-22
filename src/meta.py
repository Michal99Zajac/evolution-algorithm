from matplotlib import pyplot

from metaheuristics.HL import hl
from metaheuristics.RS import rs
from metaheuristics.RW import rw
from metaheuristics.SA import sa


if __name__ == "__main__":
    LEFT_LIMIT = -50
    RIGHT_LIMIT = 50
    EPOCHS = 100
    STEP_SIZE = 20
    SA_STEP_SIZE = 0.5

    for meta in [[hl, "HL"], [rs, "RS"], [rw, "RW"], [sa, "SA"]]:
        with open(f"./meta/{meta[1]}.txt", "w+") as writer:
            best, score, scores = None, None, None

            if meta[1] == "RS":
                best, score, scores = meta[0](LEFT_LIMIT, RIGHT_LIMIT, EPOCHS)
            elif meta[1] == "SA":
                best, score, scores = meta[0](
                    LEFT_LIMIT, RIGHT_LIMIT, EPOCHS, SA_STEP_SIZE
                )
            else:
                best, score, scores = meta[0](
                    LEFT_LIMIT, RIGHT_LIMIT, EPOCHS, STEP_SIZE
                )

            writer.write("{:<8} {:<15}\n".format("epoch", "score"))
            writer.writelines(
                ["{:<8} {:<15}\n".format(index, s) for index, s in enumerate(scores)]
            )

            pyplot.plot(scores, ".-")
            pyplot.xlabel("Epoch")
            pyplot.ylabel("Evaluation f(x)")
            pyplot.axis([0, 100, 0, 1])
            pyplot.savefig(f"./meta/{meta[1]}.png")
            pyplot.close()
