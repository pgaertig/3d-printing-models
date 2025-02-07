#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%
A4_w = 210 * MM
A4_h = 297 * MM
A5_w = A4_h/2
A5_h = 210 * MM
corner_s = 5
offset = 30
slit_h = 1
aim_hole_r = 2.5
aim_hole_crosshair_r = 10
tool_h = 3

sk = Pos(0, offset/2) * RectangleRounded(A4_w + offset, A5_w + offset, corner_s, align=(Align.CENTER, Align.MAX))
#sk -= Pos(0, 0) * Rectangle(A4_w + offset/2, slit_h)
sk -= Pos(0, -offset/2) * Rectangle(A4_w, A5_w-offset/2, align=(Align.CENTER, Align.MAX))
#sk -= Pos(0, A4_h/2 + offset/4) * Rectangle(A4_w+offset, A4_h)

sk_aim_hole = Circle(aim_hole_r) + PolarLocations(aim_hole_r, 4) * Rectangle(aim_hole_crosshair_r, slit_h)

grid = GridLocations(A4_w, 0, 2, 1)
text_grid = GridLocations(A4_w + offset/2, 0, 2, 1)

# A4 halving
loc2 = Pos(0, -A4_h/2)
sk += loc2 * grid * Circle(aim_hole_crosshair_r)
sk -= loc2 * grid * sk_aim_hole
sk -= loc2 * text_grid * (Pos(0, 10) * Text("2", 10,rotation=270))

# A4 quartering
loc4 = Pos(0, -A4_h/4)
sk += loc4 * grid * Circle(aim_hole_crosshair_r)
sk -= loc4 * grid * sk_aim_hole
sk -= loc4 * text_grid * (Pos(0, 10) * Text("4", 10,rotation=270))

# A3 quartering
loc3 = Pos(0, -A4_h/3)
sk += loc3 * grid * Circle(aim_hole_crosshair_r)
sk -= loc3 * grid * sk_aim_hole
sk -= loc3 * text_grid * (Pos(0, 10) * Text("3", 10,rotation=270))

# extra guide
locX = Pos(0, -offset/2) * GridLocations(A4_w, A4_h, 2, 1)
sk += locX  * Circle(aim_hole_crosshair_r)
sk -= locX * sk_aim_hole


#sk = fillet(sk.vertices(), 5)


part = extrude(sk, tool_h)
part += Pos(0, offset/2) * Box(A4_w/3, offset/4, tool_h*3, align=(Align.CENTER, Align.CENTER, Align.MIN))
part = chamfer(part.edges().group_by(Axis.Z)[-1], tool_h/3)
last = part.edges()
part -= Pos(0, 0) * Box(A4_w + offset/2, slit_h, tool_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
part = chamfer((part.edges()-last).group_by(Axis.Z)[-1], tool_h/3)


ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")