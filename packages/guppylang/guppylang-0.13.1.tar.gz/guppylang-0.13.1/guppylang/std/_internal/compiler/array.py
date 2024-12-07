"""Compilers building array functions on top of hugr standard operations."""

from __future__ import annotations

import hugr.std
from hugr import Wire, ops
from hugr import tys as ht

from guppylang.definition.custom import CustomCallCompiler
from guppylang.definition.value import CallReturnWires
from guppylang.error import InternalGuppyError
from guppylang.std._internal.compiler.arithmetic import convert_itousize
from guppylang.std._internal.compiler.prelude import (
    build_unwrap,
    build_unwrap_left,
    build_unwrap_right,
)
from guppylang.tys.arg import ConstArg, TypeArg
from guppylang.tys.const import ConstValue

# ------------------------------------------------------
# --------------- std.array operations -----------------
# ------------------------------------------------------


def _instantiate_array_op(
    name: str, elem_ty: ht.Type, length: int, inp: list[ht.Type], out: list[ht.Type]
) -> ops.ExtOp:
    return hugr.std.PRELUDE.get_op(name).instantiate(
        [ht.BoundedNatArg(length), ht.TypeTypeArg(elem_ty)], ht.FunctionType(inp, out)
    )


def array_type(elem_ty: ht.Type, length: int) -> ht.ExtType:
    """Returns the hugr type of a fixed length array."""
    length_arg = ht.BoundedNatArg(length)
    elem_arg = ht.TypeTypeArg(elem_ty)
    return hugr.std.PRELUDE.types["array"].instantiate([length_arg, elem_arg])


def array_new(elem_ty: ht.Type, length: int) -> ops.ExtOp:
    """Returns an operation that creates a new fixed length array."""
    arr_ty = array_type(elem_ty, length)
    return _instantiate_array_op(
        "new_array", elem_ty, length, [elem_ty] * length, [arr_ty]
    )


def array_get(elem_ty: ht.Type, length: int) -> ops.ExtOp:
    """Returns an array `get` operation."""
    assert elem_ty.type_bound() == ht.TypeBound.Copyable
    arr_ty = array_type(elem_ty, length)
    return _instantiate_array_op(
        "get", elem_ty, length, [arr_ty, ht.USize()], [ht.Option(elem_ty)]
    )


def array_set(elem_ty: ht.Type, length: int) -> ops.ExtOp:
    """Returns an array `set` operation."""
    arr_ty = array_type(elem_ty, length)
    return _instantiate_array_op(
        "set",
        elem_ty,
        length,
        [arr_ty, ht.USize(), elem_ty],
        [ht.Either([elem_ty, arr_ty], [elem_ty, arr_ty])],
    )


# ------------------------------------------------------
# --------- Custom compilers for non-native ops --------
# ------------------------------------------------------


class ArrayCompiler(CustomCallCompiler):
    """Base class for custom array op compilers."""

    @property
    def elem_ty(self) -> ht.Type:
        """The element type for the array op that is being compiled."""
        match self.type_args:
            case [TypeArg(ty=elem_ty), _]:
                return elem_ty.to_hugr()
            case _:
                raise InternalGuppyError("Invalid array type args")

    @property
    def length(self) -> int:
        """The length for the array op that is being compiled."""
        match self.type_args:
            case [_, ConstArg(ConstValue(value=int(length)))]:
                return length
            case _:
                raise InternalGuppyError("Invalid array type args")


class NewArrayCompiler(ArrayCompiler):
    """Compiler for the `array.__new__` function."""

    def build_classical_array(self, elems: list[Wire]) -> Wire:
        """Lowers a call to `array.__new__` for classical arrays."""
        # See https://github.com/CQCL/guppylang/issues/629
        return self.build_linear_array(elems)

    def build_linear_array(self, elems: list[Wire]) -> Wire:
        """Lowers a call to `array.__new__` for linear arrays."""
        elem_opt_ty = ht.Option(self.elem_ty)
        elem_opts = [
            self.builder.add_op(ops.Tag(1, elem_opt_ty), elem) for elem in elems
        ]
        return self.builder.add_op(array_new(elem_opt_ty, len(elems)), *elem_opts)

    def compile(self, args: list[Wire]) -> list[Wire]:
        if self.elem_ty.type_bound() == ht.TypeBound.Any:
            return [self.build_linear_array(args)]
        else:
            return [self.build_classical_array(args)]


class ArrayGetitemCompiler(ArrayCompiler):
    """Compiler for the `array.__getitem__` function."""

    def build_classical_getitem(self, array: Wire, idx: Wire) -> CallReturnWires:
        """Lowers a call to `array.__getitem__` for classical arrays."""
        # See https://github.com/CQCL/guppylang/issues/629
        elem_opt_ty = ht.Option(self.elem_ty)
        idx = self.builder.add_op(convert_itousize(), idx)
        result = self.builder.add_op(array_get(elem_opt_ty, self.length), array, idx)
        elem_opt = build_unwrap(self.builder, result, "Array index out of bounds")
        elem = build_unwrap(self.builder, elem_opt, "array.__getitem__: Internal error")
        return CallReturnWires(regular_returns=[elem], inout_returns=[array])

    def build_linear_getitem(self, array: Wire, idx: Wire) -> CallReturnWires:
        """Lowers a call to `array.__getitem__` for linear arrays."""
        # Swap out the element at the given index with `None`. The `to_hugr`
        # implementation of the array type ensures that linear element types are turned
        # into optionals.
        elem_opt_ty = ht.Option(self.elem_ty)
        none = self.builder.add_op(ops.Tag(0, elem_opt_ty))
        idx = self.builder.add_op(convert_itousize(), idx)
        result = self.builder.add_op(
            array_set(elem_opt_ty, self.length), array, idx, none
        )
        elem_opt, array = build_unwrap_right(
            self.builder, result, "Array index out of bounds"
        )
        elem = build_unwrap(
            self.builder, elem_opt, "Linear array element has already been used"
        )
        return CallReturnWires(regular_returns=[elem], inout_returns=[array])

    def compile_with_inouts(self, args: list[Wire]) -> CallReturnWires:
        [array, idx] = args
        if self.elem_ty.type_bound() == ht.TypeBound.Any:
            return self.build_linear_getitem(array, idx)
        else:
            return self.build_classical_getitem(array, idx)

    def compile(self, args: list[Wire]) -> list[Wire]:
        raise InternalGuppyError("Call compile_with_inouts instead")


class ArraySetitemCompiler(ArrayCompiler):
    """Compiler for the `array.__setitem__` function."""

    def build_classical_setitem(
        self, array: Wire, idx: Wire, elem: Wire
    ) -> CallReturnWires:
        """Lowers a call to `array.__setitem__` for classical arrays."""
        # See https://github.com/CQCL/guppylang/issues/629
        elem_opt_ty = ht.Option(self.elem_ty)
        idx = self.builder.add_op(convert_itousize(), idx)
        elem_opt = self.builder.add_op(ops.Tag(1, elem_opt_ty), elem)
        result = self.builder.add_op(
            array_set(elem_opt_ty, self.length), array, idx, elem_opt
        )
        # Unwrap the result, but we don't have to hold onto the returned old value
        _, array = build_unwrap_right(self.builder, result, "Array index out of bounds")
        return CallReturnWires(regular_returns=[], inout_returns=[array])

    def build_linear_setitem(
        self, array: Wire, idx: Wire, elem: Wire
    ) -> CallReturnWires:
        """Lowers a call to `array.__setitem__` for linear arrays."""
        # Embed the element into an optional
        elem_opt_ty = ht.Option(self.elem_ty)
        elem = self.builder.add_op(ops.Tag(1, elem_opt_ty), elem)
        idx = self.builder.add_op(convert_itousize(), idx)
        result = self.builder.add_op(
            array_set(elem_opt_ty, self.length), array, idx, elem
        )
        old_elem_opt, array = build_unwrap_right(
            self.builder, result, "Array index out of bounds"
        )
        # Check that the old element was `None`
        build_unwrap_left(
            self.builder, old_elem_opt, "Linear array element has not been used"
        )
        return CallReturnWires(regular_returns=[], inout_returns=[array])

    def compile_with_inouts(self, args: list[Wire]) -> CallReturnWires:
        [array, idx, elem] = args
        if self.elem_ty.type_bound() == ht.TypeBound.Any:
            return self.build_linear_setitem(array, idx, elem)
        else:
            return self.build_classical_setitem(array, idx, elem)

    def compile(self, args: list[Wire]) -> list[Wire]:
        raise InternalGuppyError("Call compile_with_inouts instead")
