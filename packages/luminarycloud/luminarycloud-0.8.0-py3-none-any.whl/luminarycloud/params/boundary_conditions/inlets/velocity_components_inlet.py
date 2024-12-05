# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud.vector3 import Vector3
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class VelocityComponentsInlet(Inlet):
    """Velocity components inlet boundary condition."""

    inlet_velocity_components: Vector3 = field(default_factory=lambda: Vector3(x=1.0))
    "Velocity components at the inlet boundary."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.VELOCITY_COMPONENTS_INLET
        _proto.inlet_velocity_components.CopyFrom(self.inlet_velocity_components._to_ad_proto())
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.inlet_velocity_components._from_ad_proto(proto.inlet_velocity_components)
