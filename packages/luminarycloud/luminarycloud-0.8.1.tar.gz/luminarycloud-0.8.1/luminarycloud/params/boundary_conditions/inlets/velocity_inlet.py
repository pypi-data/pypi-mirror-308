# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class VelocityInlet(Inlet):
    """Velocity inlet boundary condition."""

    magnitude: float = 1.0
    "Velocity magnitude at the inlet boundary."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.VELOCITY_INLET
        _proto.inlet_velocity_magnitude.value = self.magnitude
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.magnitude = proto.inlet_velocity_magnitude.value
