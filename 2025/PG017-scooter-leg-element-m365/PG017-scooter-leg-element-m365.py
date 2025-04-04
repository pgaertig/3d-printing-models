#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from ezdxf.addons.drawing.text import Alignment

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

cylinder_r = 10
hole_r = 5
wider_hole_r = 7
cylinder_h = 29
hole_h = 3
guide_h = 6
guide_w = 10
guide_shift = 2

part = Cylinder(cylinder_r, cylinder_h, align=[Align.CENTER, Align.CENTER, Align.MIN])
part -= Pos(0,0, hole_h) * Cylinder(wider_hole_r, cylinder_h, align=[Align.CENTER, Align.CENTER, Align.MIN])

box = Box(guide_h, guide_w, guide_h, align=[Align.CENTER, Align.CENTER, Align.MAX])
filleted_box = fillet(box.edges().filter_by(Axis.Z).group_by(Axis.X)[-1],2)

guide = PolarLocations(cylinder_r-guide_h/2-guide_shift, 2) * filleted_box

        #Po((-guide_h/2)-guide_shift, 0, 2, 1) * box)

part += guide
part -= Cylinder(hole_r, hole_h*5)

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")