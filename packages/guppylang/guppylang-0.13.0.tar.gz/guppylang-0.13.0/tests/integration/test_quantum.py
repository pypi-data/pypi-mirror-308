"""Various tests for the functions defined in `guppylang.prelude.quantum`."""

import pytest

from hugr.package import ModulePointer

import guppylang.decorator
from guppylang.decorator import guppy
from guppylang.module import GuppyModule
from guppylang.std.angles import angle

from guppylang.std.builtins import owned, py
from guppylang.std.quantum import (
    dirty_qubit,
    discard,
    measure,
    qubit
)
from guppylang.std.quantum_functional import (
    cx,
    cy,
    cz,
    h,
    t,
    s,
    x,
    y,
    z,
    tdg,
    sdg,
    zz_max,
    phased_x,
    rx,
    ry,
    rz,
    crz,
    toffoli,
    zz_phase,
    reset,
    quantum_functional,
    measure_return,
)


def compile_quantum_guppy(fn) -> ModulePointer:
    """A decorator that combines @guppy with HUGR compilation.

    Modified version of `tests.util.compile_guppy` that loads the quantum module.
    """
    assert not isinstance(
        fn,
        GuppyModule,
    ), "`@compile_quantum_guppy` does not support extra arguments."

    module = GuppyModule("module")
    module.load(angle, qubit, dirty_qubit, discard, measure)
    module.load_all(quantum_functional)
    guppylang.decorator.guppy(module)(fn)
    return module.compile()


def test_dirty_qubit(validate):
    @compile_quantum_guppy
    def test() -> tuple[bool, bool]:
        q1, q2 = qubit(), dirty_qubit()
        q1, q2 = cx(q1, q2)
        return (measure(q1), measure(q2))

    validate(test)


def test_1qb_op(validate):
    @compile_quantum_guppy
    def test(q: qubit @owned) -> qubit:
        q = h(q)
        q = t(q)
        q = s(q)
        q = x(q)
        q = y(q)
        q = z(q)
        q = tdg(q)
        q = sdg(q)
        return q

    validate(test)


def test_2qb_op(validate):
    @compile_quantum_guppy
    def test(q1: qubit @owned, q2: qubit @owned) -> tuple[qubit, qubit]:
        q1, q2 = cx(q1, q2)
        q1, q2 = cy(q1, q2)
        q1, q2 = cz(q1, q2)
        q1, q2 = zz_max(q1, q2)
        return (q1, q2)

    validate(test)


def test_3qb_op(validate):
    @compile_quantum_guppy
    def test(q1: qubit @owned, q2: qubit @owned, q3: qubit @owned) -> tuple[qubit, qubit, qubit]:
        q1, q2, q3 = toffoli(q1, q2, q3)
        return (q1, q2, q3)

    validate(test)


def test_measure_ops(validate):
    """Compile various measurement-related operations."""

    @compile_quantum_guppy
    def test(q1: qubit @owned, q2: qubit @owned) -> tuple[bool, bool]:
        q1, b1 = measure_return(q1)
        q1 = discard(q1)
        q2 = reset(q2)
        b2 = measure(q2)
        return (b1, b2)

    validate(test)


def test_parametric(validate):
    """Compile various parametric operations."""

    @compile_quantum_guppy
    def test(q1: qubit @owned, q2: qubit @owned, a1: angle, a2: angle, a3: angle) -> tuple[qubit, qubit]:
        q1 = rx(q1, a1)
        q1 = ry(q1, a1)
        q2 = rz(q2, a3)
        q1 = phased_x(q1, a1, a2)
        q1, q2 = zz_phase(q1, q2, a1)
        q1, q2 = crz(q1, q2, a3)
        return (q1, q2)
