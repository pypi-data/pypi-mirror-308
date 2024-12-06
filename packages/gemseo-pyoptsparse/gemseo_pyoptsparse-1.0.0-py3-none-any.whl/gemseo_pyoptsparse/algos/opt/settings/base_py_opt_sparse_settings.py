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

"""Common options to all algorithms, controlled by |g|."""

from __future__ import annotations

from functools import partial

from gemseo.algos.opt.base_gradient_based_algorithm_settings import (
    BaseGradientBasedAlgorithmSettings,
)
from gemseo.algos.opt.base_optimizer_settings import BaseOptimizerSettings
from gemseo.utils.pydantic import copy_field
from pydantic import Field
from pydantic import NonNegativeFloat  # noqa:TCH002
from strenum import StrEnum

copy_field_opt = partial(copy_field, model=BaseOptimizerSettings)


class AlgoNames(StrEnum):
    """Definition of names for algorithms."""

    SLSQP = "PYOPTSPARSE_SLSQP"
    SNOPT = "PYOPTSPARSE_SNOPT"


class BasePyOptSparseSettings(
    BaseOptimizerSettings, BaseGradientBasedAlgorithmSettings
):
    """Common options of PyOptSparse algorithms controlled by |g|."""

    ftol_abs: NonNegativeFloat = copy_field_opt("ftol_abs", default=1e-6)

    ftol_rel: NonNegativeFloat = copy_field_opt("ftol_rel", default=1e-6)

    xtol_rel: NonNegativeFloat = copy_field_opt("xtol_rel", default=1e-6)

    xtol_abs: NonNegativeFloat = copy_field_opt("xtol_abs", default=1e-6)

    options_file: str | None = Field(
        None, description="The file name where all options are written."
    )
