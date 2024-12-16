#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

TOP = (Align.CENTER, Align.CENTER, Align.MAX)

inner_d = 96.3 * MM
side_wall_t = 2 * MM
cover_d = inner_d + side_wall_t * 2

bottom_wall_t = 2.4 * MM
cover_h = 35 * MM
inner_h = cover_h - bottom_wall_t
bottom_chamfer_l = bottom_wall_t / 3

cable_hole_d = 10.2 * MM

slot_w = 8 * MM
slot_h = 3.5 * MM
slot_pos = 5.5

part = Cylinder(cover_d/2, cover_h, align=TOP) - Cylinder(inner_d/2, inner_h, align=TOP)
part = chamfer(part.edges().group_by(Axis.Z)[0], bottom_chamfer_l)
part -= Hole(cable_hole_d/2, cover_h)

slot = Plane.ZY * Pos(-slot_pos - slot_w/2) * extrude(SlotOverall(slot_w, slot_h), cover_d/2, both=True)

part -= slot


show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")