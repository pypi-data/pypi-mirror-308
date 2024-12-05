# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from luminarycloud.params.materials.laminar_viscosity import LaminarViscosityModel


@dataclass(kw_only=True)
class LaminarConstantViscosity(LaminarViscosityModel):
    """
    Constant laminar viscosity model.
    """

    laminar_constant_viscosity_constant: float = 1.7894e-05
    "Value for dynamic viscosity."
