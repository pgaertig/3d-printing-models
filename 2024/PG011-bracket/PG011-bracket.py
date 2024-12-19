#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

BOTTOM = (Align.CENTER, Align.CENTER, Align.MAX)

part = Pos(0,0, -2.5) * extrude(SlotOverall(200, 5), 8)
part += Pos(-(200-5)/2) * Cylinder(5/2,13)
part += Pos(+(200-5)/2) * Cylinder(5/2,13)
part -= Pos(-(200-5)/2,0,2.5) * Cylinder(1,10)
part -= Pos(+(200-5)/2,0,2.5) * Cylinder(1,10)

part += (Pos(0,2.5,1.5) * Cylinder(10/2, 20))
part -= (Pos(0,4,1.5) * Cylinder(6/2, 20))
part -= (Pos(0,6,1.5) * Box(5.5,5, 20))

show(part)


# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")