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
"""Options for SNOPT algorithm in PyOptSparse."""

from __future__ import annotations

from sys import float_info
from typing import Any
from typing import ClassVar

from gemseo.algos.opt.base_gradient_based_algorithm_settings import (
    BaseGradientBasedAlgorithmSettings,
)
from pydantic import Field

from gemseo_pyoptsparse.algos.opt.settings.base_py_opt_sparse_settings import AlgoNames
from gemseo_pyoptsparse.algos.opt.settings.base_py_opt_sparse_settings import (
    BasePyOptSparseSettings,
)


class SNOPT_Settings(BasePyOptSparseSettings, BaseGradientBasedAlgorithmSettings):  # noqa: N801
    """SNOPT options.

    The detailed description of the options with their default values can be found
    in the `SNOPT documentation <https://web.stanford.edu/group/SOL/guides/sndoc7.pdf>`_.
    When ``None`` are defined in the current model then default values of
    the SNOPT algorithm are used.
    Note that some of the options,
    such as `Save major iteration variables`,
    come from the
    `PyOptSparse wrapper https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/optimizers/SNOPT.html`_
    and cannot be found in the SNOPT documentation.
    """

    _TARGET_CLASS_NAME = AlgoNames.SNOPT.value

    _forced_settings: ClassVar[dict[str, Any]] = {
        "Derivative option": 1,
        "Derivative level": 3,
        "Iterations limit": int(1e9),
        "Major feasibility tolerance": float_info.min,
        "Major iterations limit": int(1e9),
        "Problem Type": "Minimize",
        "Return work arrays": False,
        "Start": "Cold",
    }

    _redundant_settings: ClassVar[list[str]] = list(_forced_settings.keys())

    backup_basis_file: int | None = Field(None, alias="Backup basis file")
    central_difference_interval: float | None = Field(
        None, alias="Central difference interval"
    )
    check_frequency: int | None = Field(None, alias="Check frequency")
    crash_option: int | None = Field(None, alias="Crash option")
    crash_tolerance: float | None = Field(None, alias="Crash tolerance")
    debug_level: int | None = Field(None, alias="Debug level")
    derivative_linesearch: dict[str, Any] | None = Field(
        None, alias="Derivative linesearch"
    )
    difference_interval: float | None = Field(None, alias="Difference interval")
    dump_file: int | None = Field(None, alias="Dump file")
    elastic_mode: str | None = Field(None, alias="Elastic mode")
    elastic_weight: float = Field(
        1e4,
        alias="Elastic weight",
        description="The initial elastic weight associated to "
        "the elastic mode activation.",
    )
    expand_frequency: int | None = Field(None, alias="Expand frequency")
    factorization_frequency: int | None = Field(None, alias="Factorization frequency")
    function_precision: float | None = Field(None, alias="Function precision")
    hessian_flush: int | None = Field(None, alias="Hessian flush")
    hessian_frequency: int | None = Field(None, alias="Hessian frequency")
    hessian_full_memory: dict[str, Any] | None = Field(
        None, alias="Hessian full memory"
    )
    hessian_limited_memory: dict[str, Any] | None = Field(
        None, alias="Hessian limited memory"
    )
    hessian_updates: int = Field(
        10,
        alias="Hessian updates",
        description="Iteration frequency to start again the hessian updating process",
    )
    infinite_bound: float | None = Field(None, alias="Infinite bound")
    insert_file: int | None = Field(None, alias="Insert file")
    i_print: int = Field(0, alias="iPrint", description="Print file output unit")
    i_summ: int = Field(0, alias="iSumm", description="Summary file output unit")
    linesearch_tolerance: float = Field(
        0.9,
        alias="Linesearch tolerance",
        description="Accuracy to control a steplength with "
        "the direction of search at each iteration",
    )
    load_file: int | None = Field(None, alias="Load file")
    lu_complete_pivoting: dict[str, Any] | None = Field(
        None, alias="LU complete pivoting"
    )
    lu_factor_tolerance: float | None = Field(None, alias="LU factor tolerance")
    lu_partial_pivoting: dict[str, Any] | None = Field(
        None, alias="LU partial pivoting"
    )
    lu_rook_pivoting: dict[str, Any] | None = Field(None, alias="LU rook pivoting")
    lu_singularity_tolerance: float | None = Field(
        None, alias="LU singularity tolerance"
    )
    lu_update_tolerance: float | None = Field(None, alias="LU update tolerance")
    major_optimality_tolerance: float = Field(1e-6, alias="Major optimality tolerance")
    major_print_level: int | None = Field(None, alias="Major print level")
    major_step_limit: float = Field(
        2.0,
        alias="Major step limit",
        description="Limitation of the change in design variables during a linesearch",
    )
    minor_feasibility_tolerance: float = Field(
        1e-6,
        alias="Minor feasibility tolerance",
        description="Fesibility tolerance of the minor problem",
    )
    minor_iterations_limit: int = Field(
        10000,
        alias="Minor iterations limit",
        description="The iterations limit for the minor problem",
    )
    minor_print_level: int | None = Field(None, alias="Minor print level")
    new_basis_file: int | None = Field(None, alias="New basis file")
    new_superbasics_limit: int | None = Field(None, alias="New superbasics limit")
    nonderivative_linesearch: dict[str, Any] | None = Field(
        None, alias="Nonderivative linesearch"
    )
    objective_row: int | None = Field(None, alias="Objective row")
    old_basis_file: int | None = Field(None, alias="Old basis file")
    partial_price: int | None = Field(None, alias="Partial price")
    penalty_parameter: float | None = Field(None, alias="Penalty parameter")
    pivot_tolerance: float | None = Field(None, alias="Pivot tolerance")
    print_file: str = Field("SNOPT_print.out", alias="Print file")
    print_frequency: int | None = Field(None, alias="Print frequency")
    proximal_point_method: int = Field(
        1,
        alias="Proximal point method",
        description="The method for the proximal point procedure",
    )
    proximal_iterations_limit: int = Field(
        10000,
        alias="Proximal iterations limit",
        description="The iterations limit for solving the proximal point problem",
    )
    punch_file: int | None = Field(None, alias="Punch file")
    reduced_hessian_dimension: int | None = Field(
        None, alias="Reduced Hessian dimension"
    )
    save_frequency: int | None = Field(None, alias="Save frequency")
    save_major_iteration_variables: list[str] = Field(
        [],
        alias="Save major iteration variables",
        description="The SNOPT internal variables that must be saved into "
        "the optimization database (specific to PyOptSparse wrapper).",
    )
    scale_option: int | None = Field(None, alias="Scale option")
    scale_tolerance: float | None = Field(None, alias="Scale tolerance")
    solution: str | None = None
    solution_file: int | None = Field(None, alias="Solution file")
    start_constraint_check_at_column: int | None = Field(
        None, alias="Start constraint check at column"
    )
    start_objective_check_at_column: int | None = Field(
        None, alias="Start objective check at column"
    )
    summary_file: str = Field("SNOPT_summary.out", alias="Summary file")
    summary_frequency: int | None = Field(None, alias="Summary frequency")
    superbasics_limit: int | None = Field(None, alias="Superbasics limit")
    suppress_options_listing: dict[str, Any] | None = Field(
        None, alias="Suppress options listing"
    )
    system_information: str | None = Field(None, alias="System information")
    timing_level: int | None = Field(None, alias="Timing level")
    unbounded_objective: float | None = Field(None, alias="Unbounded objective")
    unbounded_step_size: float | None = Field(None, alias="Unbounded step size")
    user_character_workspace: int | None = Field(None, alias="User character workspace")
    user_integer_workspace: int | None = Field(None, alias="User integer workspace")
    user_real_workspace: int | None = Field(None, alias="User real workspace")
    verify_level: int | None = Field(None, alias="Verify level")
    violation_limit: float = Field(
        10.0,
        alias="Violation limit",
        description="The absolute limit on the magnitude "
        "of the maximum constraint violation "
        "after the linesearch",
    )
