from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

from models.chromosome import BinaryChromosome
from models.subject import X2Subject
from processes.crossover.factory import BinaryCrossoverFactory, BinaryCrossoverType
from processes.mutation.bin import (
    EdgeMutation,
    SinglePointMutation,
    TwoPointMutation,
    BinMutation,
)
from fitness import schaffer_N4, FitnessEnum
from processes.selection.bin import (
    TournamentSelection,
    TheBestSelection,
    RouletteSelection,
    BinSelection,
)
from models.subject.decorators import ValuerBinarySubject
from models.population.bin import BinaryPopulation
from processes.inversion import Inversion

app = FastAPI(debug=True)


@app.get("/api/bin")
def get_bin_config():
    return {
        "selection": [
            BinSelection.TOURNAMENT,
            BinSelection.THE_BEST,
            BinSelection.ROULETTE,
        ],
        "fitness": [FitnessEnum.SCHAFFER_N4],
        "crossover": [
            BinaryCrossoverType.HOMOGENEOUS,
            BinaryCrossoverType.ONE_POINT,
            BinaryCrossoverType.TWO_POINT,
            BinaryCrossoverType.THREE_POINT,
        ],
        "mutation": [BinMutation.EDGE, BinMutation.SINGLE, BinMutation.TWO_POINT],
    }


class BinConfig(BaseModel):
    epochs: int
    left_limit: float
    right_limit: float
    amount: int
    precision: int
    fitness: FitnessEnum


class BinSelectionConfig(BaseModel):
    selection: BinSelection
    type: str
    percentage: float
    group_size: Union[int, None]


class BinCrossoverConfig(BaseModel):
    type: BinaryCrossoverType
    probability: float = 0.3


class BinMutationConfig(BaseModel):
    type: BinMutation
    probability: float = 0.3


class BinInversionConfig(BaseModel):
    probability: float = 0.3


@app.post("/api/bin")
def get_bin_calc(
    config: BinConfig,
    selection_config: BinSelectionConfig,
    crossover_config: BinCrossoverConfig,
    mutation_config: BinMutationConfig,
    inversion_config: BinInversionConfig,
):
    # set fitness
    SubjectCreator = None
    fitness = None

    if config.fitness == FitnessEnum.SCHAFFER_N4:
        SubjectCreator = X2Subject
        fitness = schaffer_N4

    if SubjectCreator == None or fitness == None:
        raise Exception("Error: SubjectCreator or fitness is not set")

    # set crossover
    crossover_factory = BinaryCrossoverFactory(crossover_config.type)
    crossover = crossover_factory.create_crossover(
        SubjectCreator, crossover_config.probability
    )

    # set selection
    selection = None

    if selection_config.selection == BinSelection.THE_BEST:
        selection = TheBestSelection(selection_config.percentage, selection_config.type)
    elif selection_config.selection == BinSelection.ROULETTE:
        selection = RouletteSelection(
            selection_config.percentage, selection_config.type
        )
    elif selection_config.selection == BinSelection.TOURNAMENT:
        if not selection_config.group_size:
            raise Exception("Error: group_size is not provided")

        selection = TournamentSelection(
            selection_config.percentage,
            selection_config.group_size,
            selection_config.type,
        )

    if selection == None:
        raise Exception("Error: selection is not set")

    # mutation
    mutation = None

    if mutation_config.type == BinMutation.EDGE:
        mutation = EdgeMutation(mutation_config.probability)
    elif mutation_config.type == BinMutation.SINGLE:
        mutation = SinglePointMutation(mutation_config.probability)
    elif mutation_config.type == BinMutation.TWO_POINT:
        mutation = TwoPointMutation(mutation_config.probability)

    if mutation == None:
        raise Exception("Error: mutation is not set")

    # set inversion
    inversion = Inversion(inversion_config.probability)

    # create population
    population = BinaryPopulation(
        {
            "amount": config.amount,
            "SubjectCreator": SubjectCreator,
            "selection": selection,
            "crossover": crossover,
            "mutation": mutation,
            "inversion": inversion,
        },
        {
            "fitness": fitness,
            "left_limit": config.left_limit,
            "right_limit": config.right_limit,
            "precision": config.precision,
        },
    )

    data = population.run(config.epochs)

    return data
