# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from typing import Optional

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)


@dataclass(kw_only=True)
class Wall(BoundaryCondition):
    """Wall boundary condition."""

    momentum: enum.WallMomentum = enum.WallMomentum.NO_SLIP
    "Condition applied to the momentum equations at a solid wall boundary."
    equivalent_sand_grain_roughness: Optional[float] = None
    "Equivalent sand-grain roughness of the wall. Set to None to disable roughness control."
    energy: enum.WallEnergy = enum.WallEnergy.FIXED_HEAT_FLUX
    "Condition applied to the energy equation at a solid wall boundary."
    fixed_heat_flux: float = 0.0
    "Heat flux per unit area at wall boundary surfaces. Negative values increase temperatures at the wall while positive values decrease it. Set to 0 for an adiabatic wall."

    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.WALL
        _proto.wall_energy = self.energy
        if self.equivalent_sand_grain_roughness is not None:
            _proto.roughness_control = True
            _proto.equivalent_sand_grain_roughness.value = self.equivalent_sand_grain_roughness
        _proto.fixed_heat_flux.value = self.fixed_heat_flux
        return _proto

    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.momentum = enum.WallMomentum(proto.wall_momentum)
        self.energy = enum.WallEnergy(proto.wall_energy)
        if proto.roughness_control:
            self.equivalent_sand_grain_roughness = proto.equivalent_sand_grain_roughness.value
        self.fixed_heat_flux = proto.fixed_heat_flux.value
