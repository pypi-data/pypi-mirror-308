# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class MassFlowInlet(Inlet):
    """Mass flow inlet boundary condition."""

    mass_flow_rate: float = 1.0
    "Mass flow rate at the inlet."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.MASS_FLOW_INLET
        _proto.mass_flow_rate.value = self.mass_flow_rate
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.mass_flow_rate = proto.mass_flow_rate.value
