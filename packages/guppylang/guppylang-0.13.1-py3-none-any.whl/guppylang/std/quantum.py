"""Guppy standard module for quantum operations."""

# mypy: disable-error-code="empty-body, misc, valid-type"

from typing import no_type_check

from hugr import tys as ht

from guppylang.decorator import guppy
from guppylang.std._internal.compiler.quantum import (
    HSERIES_EXTENSION,
    MeasureReturnCompiler,
    RotationCompiler,
)
from guppylang.std._internal.util import quantum_op
from guppylang.std.angles import angle
from guppylang.std.builtins import owned


@guppy.type(ht.Qubit, linear=True)
class qubit:
    @guppy
    @no_type_check
    def __new__() -> "qubit":
        q = dirty_qubit()
        reset(q)
        return q

    @guppy
    @no_type_check
    def measure(self: "qubit" @ owned) -> bool:
        return measure(self)

    @guppy
    @no_type_check
    def measure_return(self: "qubit") -> bool:
        return measure_return(self)

    @guppy
    @no_type_check
    def measure_reset(self: "qubit") -> bool:
        """Projective measure and reset without discarding the qubit."""
        res = self.measure_return()
        if res:
            x(self)
        return res

    @guppy
    @no_type_check
    def discard(self: "qubit" @ owned) -> None:
        discard(self)


@guppy.hugr_op(quantum_op("H"))
@no_type_check
def h(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("CZ"))
@no_type_check
def cz(control: qubit, target: qubit) -> None: ...


@guppy.hugr_op(quantum_op("CY"))
@no_type_check
def cy(control: qubit, target: qubit) -> None: ...


@guppy.hugr_op(quantum_op("CX"))
@no_type_check
def cx(control: qubit, target: qubit) -> None: ...


@guppy.hugr_op(quantum_op("T"))
@no_type_check
def t(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("S"))
@no_type_check
def s(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("X"))
@no_type_check
def x(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("Y"))
@no_type_check
def y(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("Z"))
@no_type_check
def z(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("Tdg"))
@no_type_check
def tdg(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("Sdg"))
@no_type_check
def sdg(q: qubit) -> None: ...


@guppy.hugr_op(quantum_op("ZZMax", ext=HSERIES_EXTENSION))
@no_type_check
def zz_max(q1: qubit, q2: qubit) -> None: ...


@guppy.custom(RotationCompiler("Rz"))
@no_type_check
def rz(q: qubit, angle: angle) -> None: ...


@guppy.custom(RotationCompiler("Rx"))
@no_type_check
def rx(q: qubit, angle: angle) -> None: ...


@guppy.custom(RotationCompiler("Ry"))
@no_type_check
def ry(q: qubit, angle: angle) -> None: ...


@guppy.custom(RotationCompiler("CRz"))
@no_type_check
def crz(control: qubit, target: qubit, angle: angle) -> None: ...


@guppy.hugr_op(quantum_op("Toffoli"))
@no_type_check
def toffoli(control1: qubit, control2: qubit, target: qubit) -> None: ...


@guppy.hugr_op(quantum_op("QAlloc"))
@no_type_check
def dirty_qubit() -> qubit: ...


@guppy.custom(MeasureReturnCompiler())
@no_type_check
def measure_return(q: qubit) -> bool: ...


@guppy.hugr_op(quantum_op("QFree"))
@no_type_check
def discard(q: qubit @ owned) -> None: ...


@guppy
@no_type_check
def measure(q: qubit @ owned) -> bool:
    res = measure_return(q)
    discard(q)
    return res


@guppy
@no_type_check
def phased_x(q: qubit, angle1: angle, angle2: angle) -> None:
    f1 = float(angle1)
    f2 = float(angle2)
    _phased_x(q, f1, f2)


@guppy
@no_type_check
def zz_phase(q1: qubit, q2: qubit, angle: angle) -> None:
    f = float(angle)
    _zz_phase(q1, q2, f)


@guppy.hugr_op(quantum_op("Reset"))
@no_type_check
def reset(q: qubit) -> None: ...


# ------------------------------------------------------
# --------- Internal definitions -----------------------
# ------------------------------------------------------


@guppy.hugr_op(quantum_op("PhasedX", ext=HSERIES_EXTENSION))
@no_type_check
def _phased_x(q: qubit, angle1: float, angle2: float) -> None:
    """PhasedX operation from the hseries extension.

    See `guppylang.prelude.quantum.phased_x` for a public definition that
    accepts angle parameters.
    """


@guppy.hugr_op(quantum_op("ZZPhase", ext=HSERIES_EXTENSION))
@no_type_check
def _zz_phase(q1: qubit, q2: qubit, angle: float) -> None:
    """ZZPhase operation from the hseries extension.

    See `guppylang.prelude.quantum.phased_x` for a public definition that
    accepts angle parameters.
    """
