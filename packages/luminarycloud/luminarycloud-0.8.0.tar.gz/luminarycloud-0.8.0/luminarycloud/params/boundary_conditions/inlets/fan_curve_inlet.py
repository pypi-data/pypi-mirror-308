# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from luminarycloud.params.boundary_conditions import Inlet
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class FanCurveInlet(Inlet):
    """Fan curve inlet boundary condition."""

    fan_curve_table_data: str = ""
    "Table data for the fan curve."
    total_pressure: float = 101325
    "Total pressure at the inlet."
    head_loss_coefficient: float = 0.0
    "Head loss coefficient for the fan."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.inlet_momentum = enum.InletMomentum.FAN_CURVE_INLET
        _proto.fan_curve_table_data = self.fan_curve_table_data
        _proto.total_pressure.value = self.total_pressure
        _proto.head_loss_coefficient.value = self.head_loss_coefficient
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.fan_curve_table_data = proto.fan_curve_table_data
        self.total_pressure = proto.total_pressure.value
        self.head_loss_coefficient = proto.head_loss_coefficient.value
