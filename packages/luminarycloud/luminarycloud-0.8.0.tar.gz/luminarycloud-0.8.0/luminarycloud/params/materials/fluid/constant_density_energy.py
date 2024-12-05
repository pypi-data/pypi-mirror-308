# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.materials import MaterialFluid


# TODO: Add boussinesq_approximation parameters.
@dataclass(kw_only=True)
class ConstantDensityEnergy(MaterialFluid):
    """Configuration for Constant Density Energy materials"""

    constant_density_value: float = 1.225
    "Constant density value."
    specific_heat_cp: float = 1004.703
    "Specific heat at constant pressure."

    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = super()._to_proto()
        _proto.material_fluid.density_relationship = (
            enum.DensityRelationship.CONSTANT_DENSITY_ENERGY
        )
        _proto.material_fluid.constant_density_value.value = self.constant_density_value
        _proto.material_fluid.specific_heat_cp.value = self.specific_heat_cp
        return _proto

    def _from_proto(self, proto: clientpb.MaterialEntity):
        super()._from_proto(proto)
        self.constant_density_value = proto.material_fluid.constant_density_value.value
        self.specific_heat_cp = proto.material_fluid.specific_heat_cp.value
