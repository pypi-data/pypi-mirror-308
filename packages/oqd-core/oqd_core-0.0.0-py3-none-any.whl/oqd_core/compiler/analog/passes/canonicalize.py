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

from oqd_compiler_infrastructure import Chain, FixedPoint, Post, Pre, In

########################################################################################
from oqd_core.compiler.analog.rewrite.canonicalize import (
    OperatorDistribute,
    GatherMathExpr,
    PauliAlgebra,
    NormalOrder,
    ProperOrder,
    ScaleTerms,
    SortedOrder,
    PruneIdentity,
    GatherPauli,
)
from oqd_core.compiler.analog.verify import (
    VerifyHilberSpaceDim,
    CanVerGatherMathExpr,
    CanVerGatherPauli,
    CanVerNormalOrder,
    CanVerOperatorDistribute,
    CanVerPauliAlgebra,
    CanVerProperOrder,
    CanVerPruneIdentity,
    CanVerScaleTerm,
    CanVerSortedOrder,
)
from oqd_core.compiler.math.rules import (
    DistributeMathExpr,
    ProperOrderMathExpr,
    PartitionMathExpr,
)

########################################################################################

__all__ = [
    "analog_operator_canonicalization",
]

########################################################################################

dist_chain = Chain(
    FixedPoint(Post(OperatorDistribute())),
    FixedPoint(Post(GatherMathExpr())),
    FixedPoint(Post(OperatorDistribute())),
)

pauli_chain = Chain(
    FixedPoint(Post(PauliAlgebra())),
    FixedPoint(Post(GatherMathExpr())),
    FixedPoint(Post(PauliAlgebra())),
)

normal_order_chain = Chain(
    FixedPoint(Post(NormalOrder())),
    FixedPoint(Post(OperatorDistribute())),
    FixedPoint(Post(GatherMathExpr())),
    FixedPoint(Post(ProperOrder())),
    FixedPoint(Post(NormalOrder())),
)

scale_terms_chain = Chain(
    FixedPoint(Pre(ScaleTerms())),
    FixedPoint(Post(GatherMathExpr())),
)

math_chain = Chain(
    FixedPoint(Post(DistributeMathExpr())),
    FixedPoint(Post(ProperOrderMathExpr())),
    FixedPoint(Post(PartitionMathExpr())),
)

verify_canonicalization = Chain(
    Post(CanVerOperatorDistribute()),
    Post(CanVerGatherMathExpr()),
    Post(CanVerProperOrder()),
    Post(CanVerPauliAlgebra()),
    Post(CanVerGatherPauli()),
    Post(CanVerNormalOrder()),
    Post(CanVerPruneIdentity()),
    Post(CanVerSortedOrder()),
    Pre(CanVerScaleTerm()),
)


def analog_operator_canonicalization(model):
    """
    This pass runs canonicalization chain for Operators with a verifies for canonicalization.

    Args:
        model (VisitableBaseModel):

    Returns:
        model (VisitableBaseModel):  [`Operator`][oqd_core.interface.analog.operator.Operator] of Analog level are in canonical form

    Assumptions:
        None

    Example:
        - for model = X@(Y + Z), output is 1*(X@Y) + 1 * (X@Z)
        - for model = [`AnalogGate`][oqd_core.interface.analog.operations.AnalogGate](hamiltonian = (A * J)@X), output is
            [`AnalogGate`][oqd_core.interface.analog.operations.AnalogGate](hamiltonian = 1 * (X@A))
            (where A = Annhiliation(), J = Identity() [Ladder])
    """
    return Chain(
        FixedPoint(dist_chain),
        FixedPoint(Post(ProperOrder())),
        FixedPoint(pauli_chain),
        FixedPoint(Post(GatherPauli())),
        In(VerifyHilberSpaceDim(), reverse=True),
        FixedPoint(normal_order_chain),
        FixedPoint(Post(PruneIdentity())),
        FixedPoint(scale_terms_chain),
        FixedPoint(Post(SortedOrder())),
        math_chain,
        verify_canonicalization,
    )(model=model)
