# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.boundary_conditions import (
    BoundaryCondition,
)


@dataclass(kw_only=True)
class Inlet(BoundaryCondition):
    """Inlet boundary condition."""

    turbulence_specification_spalart_allmaras: enum.TurbulenceSpecificationSpalartAllmaras = (
        enum.TurbulenceSpecificationSpalartAllmaras.TURBULENT_VISCOSITY_RATIO_SA
    )
    "Condition applied to the Spalart-Allmaras turbulence equation at the boundary."
    turbulence_specification_komega: enum.TurbulenceSpecificationKomega = (
        enum.TurbulenceSpecificationKomega.BC_TURBULENT_VISCOSITY_RATIO_AND_INTENSITY_KOMEGA
    )
    "Condition applied to the k-ω turbulence variables at the boundary."

    @abstractmethod
    def _to_proto(self) -> clientpb.BoundaryConditionsFluid:
        _proto = super()._to_proto()
        _proto.physical_boundary = enum.PhysicalBoundary.INLET
        _proto.inlet_energy = enum.InletEnergy.TOTAL_TEMPERATURE_INLET
        _proto.total_temperature.value = 300.0
        _proto.turbulence_specification_spalart_allmaras = (
            self.turbulence_specification_spalart_allmaras
        )
        _proto.turbulence_specification_komega = self.turbulence_specification_komega
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.BoundaryConditionsFluid):
        super()._from_proto(proto)
        self.turbulence_specification_spalart_allmaras = (
            enum.TurbulenceSpecificationSpalartAllmaras(
                proto.turbulence_specification_spalart_allmaras
            )
        )
        self.turbulence_specification_komega = enum.TurbulenceSpecificationKomega(
            proto.turbulence_specification_komega
        )
