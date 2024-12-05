# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.materials import MaterialFluid


@dataclass(kw_only=True)
class IdealGas(MaterialFluid):
    """Configuration for Ideal Gas materials"""

    molecular_weight: float = 28.96
    "Molecular weight of the gas used to compute its specific gas constant. Air is 28.96 g/mol."
    specific_heat_cp: float = 1004.703
    "Specific heat at constant pressure."
    laminar_thermal_conductivity: enum.LaminarThermalConductivity = (
        enum.LaminarThermalConductivity.LAMINAR_CONSTANT_THERMAL_PRANDTL
    )
    "Model for the laminar thermal conductivity of a fluid."

    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = super()._to_proto()
        _proto.material_fluid.density_relationship = enum.DensityRelationship.IDEAL_GAS
        _proto.material_fluid.molecular_weight.value = self.molecular_weight
        _proto.material_fluid.specific_heat_cp.value = self.specific_heat_cp
        return _proto

    def _from_proto(self, proto: clientpb.MaterialEntity):
        super()._from_proto(proto)
        self.molecular_weight = proto.material_fluid.molecular_weight.value
        self.specific_heat_cp = proto.material_fluid.specific_heat_cp.value
