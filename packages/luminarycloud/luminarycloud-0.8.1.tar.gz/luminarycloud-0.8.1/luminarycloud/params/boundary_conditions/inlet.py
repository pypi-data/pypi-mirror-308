# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.turbulence import TurbulenceSpecification
from luminarycloud.params.boundary_conditions import BoundaryCondition


@dataclass(kw_only=True)
class Inlet(BoundaryCondition):
    """Inlet boundary condition."""

    turbulence: TurbulenceSpecification = field(default_factory=TurbulenceSpecification)
    "Specification for turbulence at the inlet."

    @abstractmethod
    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.INLET
        _proto.inlet_energy = enum.InletEnergy.TOTAL_TEMPERATURE_INLET
        _proto.total_temperature.value = 300.0
        _proto.turbulence_specification_spalart_allmaras = self.turbulence.spalart_allmaras.method
        _proto.turbulence_specification_komega = self.turbulence.komega.method
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.turbulence.spalart_allmaras.method = enum.TurbulenceSpecificationSpalartAllmaras(
            proto.turbulence_specification_spalart_allmaras
        )
        self.turbulence.komega.method = enum.TurbulenceSpecificationKomega(
            proto.turbulence_specification_komega
        )
