#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

part = Cylinder(20,20)

show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")