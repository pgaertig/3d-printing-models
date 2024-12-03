#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

pipe_d = 125 * MM
wall_size = 2 * MM
insert_d = pipe_d * 0.999
insert_h = 30 * MM
cap_d = 128 * MM
cap_h = 0.4 * MM
hole_d = pipe_d - wall_size * 2
hole_h = insert_h - wall_size

TOP = (Align.CENTER, Align.CENTER, Align.MAX)
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

insert = Cylinder(radius=insert_d / 2, height=insert_h, align=BOTTOM)
insert -= Pos(0,0, insert_h - hole_h) * Cylinder(radius=hole_d/2, height=hole_h, align=BOTTOM)
cap = Cylinder(radius=cap_d / 2, height=cap_h, align=TOP)
#plane = Plane(Rotation((0,180,0)) * cap.faces().sort_by().last)
#text = plane * Text(txt="Kitchen vent", font_size=25)
#cap -= extrude(text, amount= 5)
part = insert  + cap

show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_stl(part, file_name + ".stl", angular_tolerance=0.01)