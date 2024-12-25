#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

part = Cylinder(20,20)

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")