#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

inner_d = 20.1 * MM
part_w = 98 * MM

neck_inner_d = 26*MM
neck_w = 6 * MM

wall_t = 3 * MM
antislip_r = 1
antislip_w = 80 * MM # antislip placement along part_w
antislip_count = 7

screw_hole_pos = 35.5 * MM
screw_hole_d = 3.7 * MM
screw_head_hole_d = 6 * MM
chamfer_r = 1.5

wall_ln = Polyline(
    (wall_t,0),
                (0,0),
                   (0, part_w-neck_w),
                   ((neck_inner_d-inner_d)/2,part_w),
                   ((neck_inner_d-inner_d)/2 + wall_t,part_w),
                   close=True)
wall_sk = Pos(X=inner_d/2) * wall_ln

fc = make_face(wall_sk.edges())

outside_edge = fc.edges()[-1].reversed()

#antislip = Rectangle(antislip_r, antislip_r, rotation=45)
antislip = Circle(antislip_r)


for i in range(antislip_count):
    loc = outside_edge @ ((i / (antislip_count - 1)) * (antislip_w/part_w))
#    print(loc)
    fc += Pos(X=loc.X, Y=loc.Y+antislip_r) * antislip


fc = fillet(fc.vertices().group_by(Axis.Y)[1:], chamfer_r)

part = revolve(fc, Axis.Y)

screw_hole_sk = Plane.XY * Pos(Z=inner_d/2 - wall_t, Y=screw_hole_pos) * Circle(screw_hole_d/2)
screw_hole_sk2 = Plane.XY * Pos(Z=inner_d/2 + wall_t, Y=screw_hole_pos) * Circle(screw_head_hole_d/2)
part = part - extrude(screw_hole_sk, wall_t * 3) - extrude(screw_hole_sk2, wall_t * 2 )

circle = Circle(1)

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")