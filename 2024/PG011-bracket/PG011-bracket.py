#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

bracket_w = 200 * MM
bracket_h = 8 * MM
bracket_t = 5 * MM

stabilizer_h = 30 * MM
stabilizer_w = 12 * MM
stabilizer_shift = stabilizer_h/8
stabilizer_hole_r = 1.15 * MM
stabilizer_hole_h = stabilizer_h - stabilizer_shift

holder_r = 5 * MM
holder_h = 20 * MM
holder_shift = 1.5
holder_hole_d = 5 * MM
holder_hole_entry_w = holder_hole_d * 0.9

show_clear()


part = Pos(0,0, -bracket_h/2) * extrude(SlotOverall(bracket_w, bracket_t), bracket_h)

stabilizer = Cylinder(bracket_t/2, stabilizer_h)
part += Pos(0,0,stabilizer_shift) * PolarLocations((bracket_w-bracket_t)/2, 2) * stabilizer

stabilizer_hole = Cylinder(stabilizer_hole_r,stabilizer_hole_h)
part -= Pos(0,0,stabilizer_shift+stabilizer_h-stabilizer_hole_h) * PolarLocations((bracket_w-bracket_t)/2, 2) * stabilizer_hole

part += Pos(0, bracket_t/2, holder_shift) * Cylinder(holder_r, holder_h)
part -= Pos(0, bracket_t-1, holder_shift) * Cylinder(holder_hole_d/2, holder_h)
part -= Pos(0, bracket_t+1, holder_shift) * Box(holder_hole_entry_w, holder_hole_d, holder_h)

show(part)


# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")