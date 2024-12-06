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

"""Options for SLSQP algorithm in PyOptSparse."""

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


class SLSQP_Settings(BasePyOptSparseSettings, BaseGradientBasedAlgorithmSettings):  # noqa: N801
    """SLSQP options."""

    _TARGET_CLASS_NAME = AlgoNames.SLSQP.value

    _forced_settings: ClassVar[dict[str, Any]] = {
        "MAXIT": int(1e9),  # using sys.maxsize leads to problem with the algo
        "ACC": float_info.min,
    }

    _redundant_settings: ClassVar[list[str]] = list(_forced_settings.keys())

    i_file: str = Field("SLSQP.out", description="Output file path", alias="IFILE")

    i_out: int = Field(60, description="Output unit number", alias="IOUT")

    i_print: int = Field(
        -1, description="Output Level (<0 - None, 0 - Screen, 1 - File)", alias="IPRINT"
    )
