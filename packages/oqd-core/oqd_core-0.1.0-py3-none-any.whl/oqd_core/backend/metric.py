# Copyright 2024 Open Quantum Design

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Union

from pydantic.types import NonNegativeInt

from oqd_compiler_infrastructure import VisitableBaseModel

########################################################################################

from oqd_core.interface.analog.operator import OperatorSubtypes

########################################################################################

__all__ = [
    "Expectation",
    "EntanglementEntropyReyni",
    "EntanglementEntropyVN",
]

########################################################################################


class Expectation(VisitableBaseModel):
    operator: OperatorSubtypes


class EntanglementEntropyVN(VisitableBaseModel):
    qreg: List[NonNegativeInt] = []
    qmode: List[NonNegativeInt] = []


class EntanglementEntropyReyni(VisitableBaseModel):
    alpha: NonNegativeInt = 1
    qreg: List[NonNegativeInt] = []
    qmode: List[NonNegativeInt] = []


Metric = Union[EntanglementEntropyVN, EntanglementEntropyReyni, Expectation]
