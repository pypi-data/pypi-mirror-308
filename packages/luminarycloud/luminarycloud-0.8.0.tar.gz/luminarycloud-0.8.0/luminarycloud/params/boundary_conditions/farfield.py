# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)
from luminarycloud.vector3 import Vector3


@dataclass(kw_only=True)
class FarField(BoundaryCondition):
    """Far-field boundary condition."""

    farfield_pressure: float = 101325.0
    "Static pressure at the boundary relative to the reference pressure."
    farfield_mach_number: float = 0.5
    "Mach number at the boundary."
    farfield_velocity_magnitude: float = 1.0
    "Velocity magnitude at the far-field boundary."
    farfield_temperature: float = 288.15
    "Static temperature at the boundary."
    far_field_flow_direction_specification: enum.FarFieldFlowDirectionSpecification = (
        enum.FarFieldFlowDirectionSpecification.FARFIELD_DIRECTION
    )
    "Method of defining the flow direction at the far-field."
    farfield_flow_direction: Vector3 = field(default_factory=Vector3)
    "Vector specifying the flow direction at the far-field boundary. Automatically scaled to a unit vector internally."
    farfield_angle_alpha: float = 0.0
    "Angle of attack. Positive angle of attack results in a non-zero far-field velocity component in the negative body-z direction."
    farfield_angle_beta: float = 0.0
    "Angle of sideslip. Positive angle of sideslip results in a non-zero far-field velocity component in the positive body-y direction."
    turbulence_specification_spalart_allmaras: enum.TurbulenceSpecificationSpalartAllmaras = (
        enum.TurbulenceSpecificationSpalartAllmaras.TURBULENT_VISCOSITY_RATIO_SA
    )
    "Condition applied to the Spalart-Allmaras turbulence equation at the boundary."
    turbulence_specification_komega: enum.TurbulenceSpecificationKomega = (
        enum.TurbulenceSpecificationKomega.BC_TURBULENT_VISCOSITY_RATIO_AND_INTENSITY_KOMEGA
    )
    "Condition applied to the k-ω turbulence variables at the boundary."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.FARFIELD
        _proto.farfield_pressure.value = self.farfield_pressure
        _proto.farfield_mach_number.value = self.farfield_mach_number
        _proto.farfield_velocity_magnitude.value = self.farfield_velocity_magnitude
        _proto.farfield_temperature.value = self.farfield_temperature
        _proto.far_field_flow_direction_specification = self.far_field_flow_direction_specification
        _proto.farfield_flow_direction.CopyFrom(self.farfield_flow_direction._to_ad_proto())
        _proto.farfield_angle_alpha.value = self.farfield_angle_alpha
        _proto.farfield_angle_beta.value = self.farfield_angle_beta
        _proto.turbulence_specification_spalart_allmaras = (
            self.turbulence_specification_spalart_allmaras
        )
        _proto.turbulence_specification_komega = self.turbulence_specification_komega
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.farfield_pressure = proto.farfield_pressure.value
        self.farfield_mach_number = proto.farfield_mach_number.value
        self.farfield_velocity_magnitude = proto.farfield_velocity_magnitude.value
        self.farfield_temperature = proto.farfield_temperature.value
        self.far_field_flow_direction_specification = enum.FarFieldFlowDirectionSpecification(
            proto.far_field_flow_direction_specification
        )
        self.farfield_flow_direction._from_ad_proto(proto.farfield_flow_direction)
        self.farfield_angle_alpha = proto.farfield_angle_alpha.value
        self.farfield_angle_beta = proto.farfield_angle_beta.value
        self.turbulence_specification_spalart_allmaras = (
            enum.TurbulenceSpecificationSpalartAllmaras(
                proto.turbulence_specification_spalart_allmaras
            )
        )
        self.turbulence_specification_komega = enum.TurbulenceSpecificationKomega(
            proto.turbulence_specification_komega
        )
