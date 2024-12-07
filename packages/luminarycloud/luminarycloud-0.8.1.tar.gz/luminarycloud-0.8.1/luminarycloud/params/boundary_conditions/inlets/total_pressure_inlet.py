# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class TotalPressureInlet(Inlet):
    """Total pressure inlet boundary condition."""

    total_pressure: float = 101325
    "Total pressure at the inlet boundary."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.TOTAL_PRESSURE_INLET
        _proto.total_pressure.value = self.total_pressure
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.total_pressure = proto.total_pressure.value
