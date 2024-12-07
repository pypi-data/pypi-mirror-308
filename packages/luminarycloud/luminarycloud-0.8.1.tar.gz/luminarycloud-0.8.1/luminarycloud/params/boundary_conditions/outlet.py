# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)


@dataclass(kw_only=True)
class Outlet(BoundaryCondition):
    """Outlet boundary condition."""

    strategy: enum.OutletStrategy = enum.OutletStrategy.OUTLET_PRESSURE
    "Outlet strategy."
    pressure_constraint: enum.OutletPressureConstraint = (
        enum.OutletPressureConstraint.OUTLET_LOCAL_CONSTRAINT
    )
    "Mode of imposing pressure at the outlet."
    target_mass_flow_rate: float = 1.0
    "Target mass flow rate (or corrected mass flow rate)."
    pressure: float = 101325.0
    "Static pressure at the outlet boundary relative to the reference pressure."
    reference_pressure: float = 101325.0
    "Absolute total pressure used to compute the corrected mass flow target."
    reference_temperature: float = 288.15
    "Total temperature used to compute the corrected mass flow target."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.OUTLET
        _proto.outlet_strategy = self.strategy
        _proto.outlet_pressure_constraint = self.pressure_constraint
        _proto.outlet_target_mass_flow_rate.value = self.target_mass_flow_rate
        _proto.outlet_pressure.value = self.pressure
        _proto.outlet_reference_pressure.value = self.reference_pressure
        _proto.outlet_reference_temperature.value = self.reference_temperature
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.strategy = enum.OutletStrategy(proto.outlet_strategy)
        self.pressure_constraint = enum.OutletPressureConstraint(proto.outlet_pressure_constraint)
        self.target_mass_flow_rate = proto.outlet_target_mass_flow_rate.value
        self.pressure = proto.outlet_pressure.value
        self.reference_pressure = proto.outlet_reference_pressure.value
        self.reference_temperature = proto.outlet_reference_temperature.value
