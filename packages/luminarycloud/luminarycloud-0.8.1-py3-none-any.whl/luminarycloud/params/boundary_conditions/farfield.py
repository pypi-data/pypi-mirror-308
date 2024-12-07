# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)
from luminarycloud.params.turbulence import TurbulenceSpecification
from luminarycloud.vector3 import Vector3


@dataclass(kw_only=True)
class FarField(BoundaryCondition):
    """Far-field boundary condition."""

    pressure: float = 101325.0
    "Static pressure at the boundary relative to the reference pressure."
    mach_number: float = 0.5
    "Mach number at the boundary."
    velocity_magnitude: float = 1.0
    "Velocity magnitude at the far-field boundary."
    temperature: float = 288.15
    "Static temperature at the boundary."
    flow_direction_specification: enum.FarFieldFlowDirectionSpecification = (
        enum.FarFieldFlowDirectionSpecification.FARFIELD_DIRECTION
    )
    "Method of defining the flow direction at the far-field."
    flow_direction: Vector3 = field(default_factory=Vector3)
    "Vector specifying the flow direction at the far-field boundary. Automatically scaled to a unit vector internally."
    angle_alpha: float = 0.0
    "Angle of attack. Positive angle of attack results in a non-zero far-field velocity component in the negative body-z direction."
    angle_beta: float = 0.0
    "Angle of sideslip. Positive angle of sideslip results in a non-zero far-field velocity component in the positive body-y direction."
    turbulence: TurbulenceSpecification = field(default_factory=TurbulenceSpecification)
    "Specification for turbulence at the farfield boundary."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.FARFIELD
        _proto.farfield_pressure.value = self.pressure
        _proto.farfield_mach_number.value = self.mach_number
        _proto.farfield_velocity_magnitude.value = self.velocity_magnitude
        _proto.farfield_temperature.value = self.temperature
        _proto.far_field_flow_direction_specification = self.flow_direction_specification
        _proto.farfield_flow_direction.CopyFrom(self.flow_direction._to_ad_proto())
        _proto.farfield_angle_alpha.value = self.angle_alpha
        _proto.farfield_angle_beta.value = self.angle_beta
        _proto.turbulence_specification_spalart_allmaras = self.turbulence.spalart_allmaras.method
        _proto.turbulence_specification_komega = self.turbulence.komega.method
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.pressure = proto.farfield_pressure.value
        self.mach_number = proto.farfield_mach_number.value
        self.velocity_magnitude = proto.farfield_velocity_magnitude.value
        self.temperature = proto.farfield_temperature.value
        self.flow_direction_specification = enum.FarFieldFlowDirectionSpecification(
            proto.far_field_flow_direction_specification
        )
        self.flow_direction._from_ad_proto(proto.farfield_flow_direction)
        self.angle_alpha = proto.farfield_angle_alpha.value
        self.angle_beta = proto.farfield_angle_beta.value
        self.turbulence.spalart_allmaras.method = enum.TurbulenceSpecificationSpalartAllmaras(
            proto.turbulence_specification_spalart_allmaras
        )
        self.turbulence.komega.method = enum.TurbulenceSpecificationKomega(
            proto.turbulence_specification_komega
        )
