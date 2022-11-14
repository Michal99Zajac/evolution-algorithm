from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

from models.subject.bin import X2Subject
from processes.crossover.factory import (
    BinaryCrossoverFactory,
    BinaryCrossoverType,
    DecimalCrossoverFactory,
    DecimalCrossoverType,
)
from processes.mutation.bin import (
    EdgeMutation,
    SinglePointMutation,
    TwoPointMutation,
    BinMutation,
)
from processes.mutation.decimal import (
    GaussMutation,
    UniformMutation,
    DecimalMutationEnum,
)
from fitness import schaffer_N4, FitnessEnum
from processes.selection import (
    TournamentSelection,
    TheBestSelection,
    RouletteSelection,
    SelectionEnum,
)
from processes.elite import Eliter
from models.population.bin import BinaryPopulation
from models.population.decimal import DecimalPopulation
from processes.inversion import Inversion

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="https:\/\/.*\.vercel\.app|http:\/\/localhost:3000",
)


@app.get("/api/bin")
def get_bin_config():
    return {
        "selection": [
            SelectionEnum.TOURNAMENT,
            SelectionEnum.THE_BEST,
            SelectionEnum.ROULETTE,
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
    type: str = "min"


class DecimalConfig(BaseModel):
    epochs: int
    left_limit: float
    right_limit: float
    amount: int
    fitness: FitnessEnum
    type: str = "min"


class SelectionConfig(BaseModel):
    type: SelectionEnum
    percentage: float
    group_size: Union[int, None]


class BinCrossoverConfig(BaseModel):
    type: BinaryCrossoverType
    probability: float = 0.3


class DecimalCrossoverConfig(BaseModel):
    type: DecimalCrossoverType
    probability: float = 0.3
    k: float = 0.5
    alpha: float = 0.1
    beta: float = 0.2


class BinMutationConfig(BaseModel):
    type: BinMutation
    probability: float = 0.3


class DecimalMutationConfig(BaseModel):
    type: DecimalMutationEnum
    probability: float = 0.3


class BinInversionConfig(BaseModel):
    probability: float = 0.3


class EliteStrategy(BaseModel):
    percentage: float = 0.1


@app.post("/api/bin")
def get_bin_calc(
    config: BinConfig,
    selection_config: SelectionConfig,
    crossover_config: BinCrossoverConfig,
    mutation_config: BinMutationConfig,
    inversion_config: BinInversionConfig,
    elite_config: EliteStrategy,
):
    # set fitness
    fitness = None

    if config.fitness == FitnessEnum.SCHAFFER_N4:
        fitness = schaffer_N4

    if fitness == None:
        raise Exception("Error: fitness is not set")

    # eliter
    eliter = Eliter(elite_config.percentage, config.type)

    # set crossover
    crossover_factory = BinaryCrossoverFactory(crossover_config.type)
    crossover = crossover_factory.create_crossover(
        X2Subject, crossover_config.probability
    )

    # set selection
    selection = None

    if selection_config.type == SelectionEnum.THE_BEST:
        selection = TheBestSelection(selection_config.percentage, config.type)
    elif selection_config.type == SelectionEnum.ROULETTE:
        selection = RouletteSelection(selection_config.percentage, config.type)
    elif selection_config.type == SelectionEnum.TOURNAMENT:
        if not selection_config.group_size:
            raise Exception("Error: group_size is not provided")

        selection = TournamentSelection(
            selection_config.percentage,
            selection_config.group_size,
            config.type,
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
            "selection": selection,
            "crossover": crossover,
            "mutation": mutation,
            "inversion": inversion,
            "eliter": eliter,
        },
        {
            "fitness": fitness,
            "left_limit": config.left_limit,
            "right_limit": config.right_limit,
            "precision": config.precision,
            "type": config.type,
        },
    )

    data = population.run(config.epochs)

    return data


@app.post("/api/decimal")
def get_decimal_calc(
    config: DecimalConfig,
    selection_config: SelectionConfig,
    crossover_config: DecimalCrossoverConfig,
    mutation_config: DecimalMutationConfig,
    elite_config: EliteStrategy,
):
    # set fitness
    fitness = None

    if config.fitness == FitnessEnum.SCHAFFER_N4:
        fitness = schaffer_N4

    if fitness == None:
        raise Exception("Error: fitness is not set")

    # eliter
    eliter = Eliter(elite_config.percentage, config.type)

    # set crossover
    crossover_factory = DecimalCrossoverFactory(crossover_config.type)
    crossover = crossover_factory.create_crossover(
        crossover_config.probability,
        left_limit=config.left_limit,
        right_limit=config.right_limit,
        k=crossover_config.k,
        alpha=crossover_config.alpha,
        beta=crossover_config.beta,
        fitness=fitness,
        type=config.type,
    )

    # set selection
    selection = None

    if selection_config.type == SelectionEnum.THE_BEST:
        selection = TheBestSelection(selection_config.percentage, config.type)
    elif selection_config.type == SelectionEnum.ROULETTE:
        selection = RouletteSelection(selection_config.percentage, config.type)
    elif selection_config.type == SelectionEnum.TOURNAMENT:
        if not selection_config.group_size:
            raise Exception("Error: group_size is not provided")

        selection = TournamentSelection(
            selection_config.percentage,
            selection_config.group_size,
            config.type,
        )

    if selection == None:
        raise Exception("Error: selection is not set")

    # mutation
    mutation = None

    if mutation_config.type == DecimalMutationEnum.GAUSS:
        mutation = GaussMutation(
            mutation_config.probability, config.left_limit, config.right_limit
        )
    elif mutation_config.type == DecimalMutationEnum.UNIFORM:
        mutation = UniformMutation(
            mutation_config.probability, config.left_limit, config.right_limit
        )

    if mutation == None:
        raise Exception("Error: mutation is not set")

    # create population
    population = DecimalPopulation(
        {
            "amount": config.amount,
            "selection": selection,
            "crossover": crossover,
            "mutation": mutation,
            "eliter": eliter,
        },
        {
            "fitness": fitness,
            "left_limit": config.left_limit,
            "right_limit": config.right_limit,
            "type": config.type,
        },
    )

    data = population.run(config.epochs)

    return data
