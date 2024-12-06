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

"""Interface to the PyOptSparse library."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import ClassVar

from gemseo.algos.design_space_utils import get_value_and_bounds
from gemseo.algos.opt.base_optimization_library import BaseOptimizationLibrary
from gemseo.algos.opt.base_optimization_library import OptimizationAlgorithmDescription
from gemseo.typing import RealArray
from gemseo.utils.pydantic import create_model
from numpy import array
from numpy import isfinite
from pyoptsparse import OPT

from gemseo_pyoptsparse.algos.opt._py_opt_sparse_optimization_problem import (
    PyOptSparseOptimizationProblem,
)
from gemseo_pyoptsparse.algos.opt.settings.base_py_opt_sparse_settings import AlgoNames
from gemseo_pyoptsparse.algos.opt.settings.base_py_opt_sparse_settings import (
    BasePyOptSparseSettings,
)
from gemseo_pyoptsparse.algos.opt.settings.slsqp import SLSQP_Settings
from gemseo_pyoptsparse.algos.opt.settings.snopt import SNOPT_Settings

if TYPE_CHECKING:
    from gemseo.algos.base_algorithm_settings import BaseAlgorithmLibrarySettings
    from gemseo.algos.optimization_problem import OptimizationProblem


OptProblemJacType = Callable[
    [Mapping[str, RealArray], Mapping[str, RealArray]], dict[str, dict[str, RealArray]]
]


@dataclass
class PyOptSparseAlgorithmDescription(OptimizationAlgorithmDescription):
    """The description of PyOptSparse algorithms."""

    library_name: str = "pyOptSparse"

    website: str = "https://mdolab-pyoptsparse.readthedocs-hosted.com"


class PyOptSparse(BaseOptimizationLibrary):
    """PyOptSparse optimization library interface.

    Contrary to other optimization libraries in |g|, the PyOptSparse library uses
    pydantic models in order to manage options grammar.
    """

    ALGORITHM_INFOS: ClassVar[dict[str, PyOptSparseAlgorithmDescription]] = {
        AlgoNames.SLSQP.value: PyOptSparseAlgorithmDescription(
            algorithm_name=AlgoNames.SLSQP,
            internal_algorithm_name=AlgoNames.SLSQP.name,
            description="Sequential Least-Squares Quadratic "
            "Programming (SLSQP) implemented in "
            "pyOptSparse library",
            handle_equality_constraints=True,
            handle_inequality_constraints=True,
            require_gradient=True,
            Settings=SLSQP_Settings,
        ),
        AlgoNames.SNOPT.value: PyOptSparseAlgorithmDescription(
            algorithm_name=AlgoNames.SNOPT,
            internal_algorithm_name=AlgoNames.SNOPT.name,
            description="SNOPT implemented in PyOptSparse library",
            handle_equality_constraints=True,
            handle_inequality_constraints=True,
            require_gradient=True,
            Settings=SNOPT_Settings,
        ),
    }

    def __init__(self, algo_name: str) -> None:  # noqa: D107
        super().__init__(algo_name)

        # Options to be forced that needs the current instance
        if algo_name == AlgoNames.SNOPT:
            self.ALGORITHM_INFOS[algo_name].Settings._forced_settings.update({
                "snSTOP function handle": self._store_major_iterations_variables
            })

    def __write_options(self, **settings) -> None:
        """Write the option file."""
        option_file = settings["options_file"]
        if not option_file:
            return

        default_settings = BasePyOptSparseSettings()

        with Path(option_file).open("w") as f:
            line = "Algorithm options:"
            f.write(f"{line}\n{'-' * len(line)}\n")
            for name, value in default_settings.model_fields.items():
                val = settings.get(name, getattr(default_settings, name))
                f.write(
                    f"* {name}\n"
                    f"\t- value = {val}\n"
                    f"\t- description: {value.description}\n"
                )

    def _store_major_iterations_variables(
        self, data: Mapping[str, float | RealArray]
    ) -> None:
        """Store PyOptSparse internal variables into the database.

        This function is called through the callback mechanism of PyOptSparse
        in order to to store into the |g| database internal variables of
        the SNOPT algorithm (e.g. feasibility, optimality...).
        Additional SNOPT variables can be stored,
        depending on the option `Save major iteration variables`.

        Args:
            data: The data to stored.
        """
        database = self._problem.database
        last_x = database.get_x_vect(-1)
        database.store(last_x, data)

    def _validate_settings(
        self,
        settings_model: BaseAlgorithmLibrarySettings | None = None,
        **settings: Any,
    ) -> dict[str, Any]:
        return create_model(
            self.ALGORITHM_INFOS[self.algo_name].Settings,
            settings_model=settings_model,
            **settings,
        ).model_dump(by_alias=True)

    def _run(self, problem: OptimizationProblem, **settings: Any) -> tuple[str, Any]:
        initial_x, lower_bnd, upper_bnd = get_value_and_bounds(
            problem.design_space, self._normalize_ds
        )

        l_b = array([val if isfinite(val) else None for val in lower_bnd])
        u_b = array([val if isfinite(val) else None for val in upper_bnd])

        self.__write_options(**settings)
        algo_options = self._filter_settings(settings, BasePyOptSparseSettings)
        algo_options.update(
            self.ALGORITHM_INFOS[self.algo_name].Settings._forced_settings
        )

        # None are filtered to that the algo uses their default settings in that case
        options_without_none = {
            name: value for name, value in algo_options.items() if value is not None
        }

        optimizer = OPT(
            self.ALGORITHM_INFOS[self.algo_name].internal_algorithm_name,
            options=options_without_none,
        )
        optim_prob = PyOptSparseOptimizationProblem(problem, initial_x, l_b, u_b)
        # storeHistory is set but not used since the history is mocked,
        # it is however useful in order to retrieve some SNOPT variables
        # into the database
        solution = optimizer(
            optim_prob, sens=optim_prob.jac or "FD", storeHistory="tmp.hst"
        )

        inform = solution.optInform
        return inform["text"], inform["value"]
