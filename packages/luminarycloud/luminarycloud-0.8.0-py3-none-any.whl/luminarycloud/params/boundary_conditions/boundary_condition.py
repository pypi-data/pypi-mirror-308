# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass, field

from luminarycloud.params.geometry import Surface
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params._param_wrappers import ParamGroupWrapper


@dataclass(kw_only=True)
class BoundaryCondition(ParamGroupWrapper):
    """Boundary condition for a fluid flow physics solver."""

    name: str = ""
    interface_id: str = ""
    "ID of the multiphysics interface that manages this boundary condition."
    surfaces: list[str] = field(default_factory=list)
    "Surfaces that this boundary condition is applied to."

    @abstractmethod
    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = clientpb.BoundaryConditionsFluid()
        _proto.boundary_condition_name = self.name
        _proto.boundary_condition_display_name = self.name
        _proto.boundary_condition_interface_id = self.interface_id
        _proto.surfaces.extend(self.surfaces)
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        self.name = proto.boundary_condition_name
        self.interface_id = proto.boundary_condition_interface_id
        self.surfaces = proto.surfaces
