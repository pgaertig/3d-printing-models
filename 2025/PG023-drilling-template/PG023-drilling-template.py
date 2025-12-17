#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from build123d import RectangleRounded, GridLocations

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

PLATE_T = 1.2

HOLE_R = 2.2
HOLE_SPACING = 32

PLATE_W = 120 + HOLE_SPACING
PLATE_H = 120

plate_sk = RectangleRounded(PLATE_W, PLATE_H, 5)
plate_sk -= GridLocations(HOLE_SPACING, 0, 2, 1) * Circle(HOLE_R)

plate = extrude(plate_sk, -PLATE_T)

part = plate

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")