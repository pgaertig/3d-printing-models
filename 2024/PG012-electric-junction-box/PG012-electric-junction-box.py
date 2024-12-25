#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from build123d import GridLocations

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

box_w = 250 * MM
box_h = 80 * MM
box_t = 20 * MM  # inner thickness
box_r = 5 * MM
box_wall_t = 2.5
screw_hole_d = 2.5 * MM
bottom_t = 2 * MM
top_t = 2 * MM
lid_t = 8 * MM # inner thickness of lid
lid_screw_hole_d = 3.8 * MM
chamfer_s = 1.3 * MM
side_hole_d = 8 * MM

# basics
loc_tuples = ((box_w/2-box_r, box_h/2-box_r),
    (-box_w/2+box_r, box_h/2-box_r),
    (-box_w/2+box_r, -box_h/2+box_r),
    (box_w/2-box_r, -box_h/2+box_r))

if box_w > 100 * MM:
    loc_tuples += ((0, box_h/2-box_r), (0, -box_h/2+box_r))

hole_locations =  Locations(loc_tuples)

outer_shape_sk = RectangleRounded(box_w, box_h, box_r)

# main part

walls_sk = (
                   outer_shape_sk - offset(outer_shape_sk,-box_wall_t)
                   + hole_locations * (Circle(box_r) - Circle(screw_hole_d/2)))

box = extrude(outer_shape_sk, bottom_t) + extrude(walls_sk, box_t + bottom_t)
box = chamfer(box.edges().group_by(Axis.Z)[0], chamfer_s)

# side hole on side plane
side_hole1 = Plane(box.faces().sort_by(Axis.X)[0]) * GridLocations(side_hole_d * 3, 0, 2, 1) * Hole(side_hole_d/2, box_wall_t)
side_hole2 = Plane(box.faces().sort_by(Axis.X)[-1]) * Hole(side_hole_d/2, box_wall_t)
box -= side_hole1
box -= side_hole2

# lid part
lid_walls_sk = (
                   outer_shape_sk - offset(outer_shape_sk,-box_wall_t)
                   + hole_locations * (Circle(box_r) - Circle(lid_screw_hole_d/2)))
lid_sk = outer_shape_sk - hole_locations * Circle(lid_screw_hole_d/2)
lid = extrude(lid_sk, top_t) + extrude(lid_walls_sk, -(lid_t + top_t))
lid = chamfer(lid.edges().group_by(Axis.Z)[-1], chamfer_s)

ocp.show(box, Pos(0,0, box_t*5) * lid)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(box, file_name + "-box.step")
export_step(lid, file_name + "-lid.step")