#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from ezdxf.addons.drawing.text import Alignment

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

foot_s = 50
foot_top_s = 30
foot_r = 5
foot_h = 30
foot_c = 3

hole_s = 16.2
hole_h = foot_h/5
hole_angle = 7.125


bottom = RectangleRounded(foot_s, foot_s, foot_r)
top = Pos(Z=foot_h) * RectangleRounded(foot_top_s, foot_top_s, foot_r)

foot = loft([bottom, top])

part = chamfer((foot.edges().group_by(Axis.Z)[-1], foot.edges().group_by(Axis.Z)[0]), foot_c)

hole_sc = Rectangle(hole_s, hole_s)
hole = Pos(Z=hole_h, Y=2) * Rot(X=hole_angle) * hole_sc

part -= extrude(hole, foot_h)

ocp.show(part)


# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")