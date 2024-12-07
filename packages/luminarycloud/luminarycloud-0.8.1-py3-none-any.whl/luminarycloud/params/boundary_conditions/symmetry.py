# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)


@dataclass(kw_only=True)
class Symmetry(BoundaryCondition):
    """Symmetry boundary condition."""

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.SYMMETRY
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        if proto.physical_boundary == enum.PhysicalBoundary.SYMMETRY:
            raise ValueError("Invalid physical boundary for symmetry BC.")
