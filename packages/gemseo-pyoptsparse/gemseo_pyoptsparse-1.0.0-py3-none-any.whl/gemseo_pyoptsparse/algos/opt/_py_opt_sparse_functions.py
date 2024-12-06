# Copyright 2021 IRT Saint Exupéry, https://www.irt-saintexupery.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Definition of PyOptSparse functions for |g|."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

from numpy import isnan

if TYPE_CHECKING:
    from collections.abc import Mapping
    from collections.abc import MutableMapping

    from gemseo.typing import RealArray


class PyOptSparseFunctions:
    """PyOptsparse interface to :class:`.MDOFunctions`."""

    __input_name: str
    """The name of the input design variable for PyOptSparse functions."""

    __output_functions: MutableMapping[str, Callable[[RealArray], RealArray]]
    """The mapping from output names to the functions that compute output values."""

    __jac_functions: MutableMapping[str, Callable[[RealArray], RealArray]]
    """The mapping from output names to the functions that compute the Jacobian of those
    outputs."""

    def __init__(self, input_name: str) -> None:
        """
        Args:
            input_name: The name of the input design variable.
        """  # noqa: D205, D212, D415
        self.__input_name = input_name
        self.__output_functions = {}
        self.__jac_functions = {}

    @property
    def has_jac(self) -> bool:
        """Whether the Jacobian of the functions exists."""
        return len(self.__output_functions) == len(self.__jac_functions) != 0

    def add_function(
        self,
        name: str,
        compute_outputs: Callable[[RealArray], RealArray],
        compute_jacobian: Callable[[RealArray], RealArray] | None = None,
    ) -> None:
        """Add a new function to the PyOptSparse optimization problem.

        Args:
            name: The name of the output.
            compute_outputs: The function to compute the value of ``name``.
            compute_jacobian: The function to compute the Jacobian of ``name``.
                If ``None``, a finite difference approximation is used.
        """
        self.__output_functions[name] = compute_outputs
        if compute_jacobian is not None:
            self.__jac_functions[name] = compute_jacobian

    def compute_outputs(
        self, inputs: Mapping[str, RealArray]
    ) -> tuple[dict[str, RealArray], bool]:
        """Execute all the functions.

        Args:
            inputs: The input data.

        Returns:
            The output data of all functions and
            whether the computation has failed (returns ``True`` in that case)
            or succeded (returns ``False``).
        """
        input_value = inputs[self.__input_name]
        outputs = {
            output_name: compute_output(input_value)
            for output_name, compute_output in self.__output_functions.items()
        }
        for output_value in outputs.values():
            if isnan(output_value).any():
                return outputs, True

        return outputs, False

    def compute_jacobian(
        self,
        inputs: Mapping[str, RealArray],
        function_values: Mapping[str, RealArray] | None = None,
    ) -> tuple[dict[str, dict[str, RealArray]], bool]:
        """Execute all Jacobian functions.

        Args:
            inputs: The input data.
            function_values: The value of the functions at input values.

        Returns:
            The Jacobian data of all functions and
            whether the computation has failed (returns ``True`` in that case)
            or succeded (returns ``False``).
        """
        input_value = inputs[self.__input_name]
        jac = {
            output_name: {self.__input_name: compute_jacobian(input_value)}
            for output_name, compute_jacobian in self.__jac_functions.items()
        }
        for sub_jac in jac.values():
            if isnan(sub_jac[self.__input_name]).any():
                return jac, True

        return jac, False
