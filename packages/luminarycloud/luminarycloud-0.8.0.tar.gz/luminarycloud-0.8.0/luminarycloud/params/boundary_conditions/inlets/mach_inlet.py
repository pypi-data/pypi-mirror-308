# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class MachInlet(Inlet):
    """Mach number inlet boundary condition."""

    farfield_temperature: float = 288.15
    "Temperature at the far-field."
    farfield_pressure: float = 101325
    "Pressure at the far-field."
    farfield_mach_number: float = 0.5
    "Mach number at the far-field."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.MACH_INLET
        _proto.farfield_temperature.value = self.farfield_temperature
        _proto.farfield_pressure.value = self.farfield_pressure
        _proto.farfield_mach_number.value = self.farfield_mach_number
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.farfield_temperature = proto.farfield_temperature.value
        self.farfield_pressure = proto.farfield_pressure.value
        self.farfield_mach_number = proto.farfield_mach_number.value
