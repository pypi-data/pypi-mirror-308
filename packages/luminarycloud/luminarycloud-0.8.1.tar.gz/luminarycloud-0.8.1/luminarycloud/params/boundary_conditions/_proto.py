# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum
from luminarycloud.params.boundary_conditions import (
    Wall,
    Outlet,
    FarField,
    Symmetry,
)
from luminarycloud.params.boundary_conditions.inlets import (
    FanCurveInlet,
    MachInlet,
    MassFlowInlet,
    TotalPressureInlet,
    VelocityInlet,
    VelocityComponentsInlet,
)


def _bc_from_proto(proto: clientpb.BoundaryConditionsFluid | clientpb.BoundaryConditionsHeat):
    if isinstance(proto, clientpb.BoundaryConditionsFluid):
        if proto.physical_boundary == enum.PhysicalBoundary.WALL:
            return Wall.from_proto(proto)
        elif proto.physical_boundary == enum.PhysicalBoundary.OUTLET:
            return Outlet.from_proto(proto)
        elif proto.physical_boundary == enum.PhysicalBoundary.FARFIELD:
            return FarField.from_proto(proto)
        elif proto.physical_boundary == enum.PhysicalBoundary.SYMMETRY:
            return Symmetry.from_proto(proto)
        elif proto.physical_boundary == enum.PhysicalBoundary.INLET:
            if proto.inlet_momentum == enum.InletMomentum.VELOCITY_INLET:
                return VelocityInlet.from_proto(proto)
            elif proto.inlet_momentum == enum.InletMomentum.VELOCITY_COMPONENTS_INLET:
                return VelocityComponentsInlet.from_proto(proto)
            elif proto.inlet_momentum == enum.InletMomentum.TOTAL_PRESSURE_INLET:
                return TotalPressureInlet.from_proto(proto)
            elif proto.inlet_momentum == enum.InletMomentum.FAN_CURVE_INLET:
                return FanCurveInlet.from_proto(proto)
            elif proto.inlet_momentum == enum.InletMomentum.MACH_INLET:
                return MachInlet.from_proto(proto)
            elif proto.inlet_momentum == enum.InletMomentum.MASS_FLOW_INLET:
                return MassFlowInlet.from_proto(proto)
            else:
                raise ValueError(f"Unknown inlet type: {proto}")
        else:
            raise ValueError(f"Unknown physical boundary type: {proto.physical_boundary}")
    elif isinstance(proto, clientpb.BoundaryConditionsHeat):
        raise NotImplementedError("Heat boundary conditions not implemented")
    raise ValueError(f"Unknown boundary condition type: {proto}")
