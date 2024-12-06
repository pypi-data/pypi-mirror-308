from enum import Enum
from functools import partial

import numpy as np
from qiskit.transpiler.passes import SabreLayout


class LayoutIterTypes(str, Enum):
    Random = "random"
    Sabre = "sabre"
    Improve = "improve"
    Auto = "auto"


def keep_layout_gen(qc):
    while True:
        yield np.arange(qc.num_qubits, dtype=int)


def random_layout_gen(qc):
    while True:
        yield np.random.permutation(qc.num_qubits)


def sabre_layout_gen(qc, cmap):
    sl = SabreLayout(cmap, swap_trials=16, layout_trials=16)
    while True:
        sl.property_set.clear()
        yield np.array(list(sl(qc).layout.final_index_layout(filter_ancillas=False)))


def get_layout_iter(layout_iterator_type, cmap):
    match layout_iterator_type:
        case LayoutIterTypes.Random:
            return random_layout_gen
        case LayoutIterTypes.Sabre:
            return partial(sabre_layout_gen, cmap=cmap)
        case LayoutIterTypes.Improve:
            return keep_layout_gen
        case _:
            raise ValueError(f"Invalid LayoutIterTypes {layout_iterator_type.name}")
