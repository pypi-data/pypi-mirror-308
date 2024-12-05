# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)
from luminarycloud.vector3 import Vector3


@dataclass(kw_only=True)
class Wall(BoundaryCondition):
    """Wall boundary condition."""

    wall_momentum: enum.WallMomentum = enum.WallMomentum.NO_SLIP
    "Condition applied to the momentum equations at a solid wall boundary."
    wall_movement_translation: Vector3 = field(default_factory=Vector3)
    "Translational velocity (x,y,z) of the wall surface."
    wall_movement_rotation_center: Vector3 = field(default_factory=Vector3)
    "Center of rotation (x,y,z) of the rotational velocity of the wall surface."
    wall_movement_angular_velocity: Vector3 = field(default_factory=Vector3)
    "Rotational velocity about the (x,y,z)-axes from the rotational center of the wall surface."
    wall_energy: enum.WallEnergy = enum.WallEnergy.FIXED_HEAT_FLUX
    "Condition applied to the energy equation at a solid wall boundary."
    roughness_control: bool = False
    "Turn roughness settings on or off."
    equivalent_sand_grain_roughness: float = 0.0
    "Equivalent sand-grain roughness of the wall."
    fixed_heat_flux: float = 0.0
    "Heat flux per unit area at wall boundary surfaces. Negative values increase temperatures at the wall while positive values decrease it. Enter 0 for an adiabatic wall."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.WALL
        _proto.wall_momentum = self.wall_momentum
        _proto.wall_movement_translation.CopyFrom(self.wall_movement_translation._to_ad_proto())
        _proto.wall_movement_rotation_center.CopyFrom(
            self.wall_movement_rotation_center._to_ad_proto()
        )
        _proto.wall_movement_angular_velocity.CopyFrom(
            self.wall_movement_angular_velocity._to_ad_proto()
        )
        _proto.wall_energy = self.wall_energy
        _proto.roughness_control = self.roughness_control
        _proto.equivalent_sand_grain_roughness.value = self.equivalent_sand_grain_roughness
        _proto.fixed_heat_flux.value = self.fixed_heat_flux
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.wall_momentum = enum.WallMomentum(proto.wall_momentum)
        self.wall_movement_translation._from_ad_proto(proto.wall_movement_translation)
        self.wall_movement_rotation_center._from_ad_proto(proto.wall_movement_rotation_center)
        self.wall_movement_angular_velocity._from_ad_proto(proto.wall_movement_angular_velocity)
        self.wall_energy = enum.WallEnergy(proto.wall_energy)
        self.roughness_control = proto.roughness_control
        self.equivalent_sand_grain_roughness = proto.equivalent_sand_grain_roughness.value
        self.fixed_heat_flux = proto.fixed_heat_flux.value
