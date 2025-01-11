#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

back_s = 1600
back_r = 100
back_d = 50

sign_d = 20

#logo = import_svg("2025/PG015-door-logo-emblem/20250106-logo.v1-3dprint.svg", label_by="label", is_inkscape_label=True)
logo = import_svg("./20250106-logo.v1-3dprint.svg", label_by="label", is_inkscape_label=True)
print("Done SVG read")

# %%

sk = Sketch()
parts= []
for face_or_wire in logo:
    parts.append(Solid.extrude(face_or_wire, (0, 0, sign_d)))

print("Done part A")

#ocp.show(part)
# %%

back_d = 70
part2 = Pos(back_s/2, back_s/2, 0) * extrude(RectangleRounded(back_s, back_s, back_r), -back_d)

parts.append(part2)
shape = ShapeList(parts)
part =  scale(Part(shape), 0.1)
ocp.show(part)



# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_stl(part, file_name + ".stl")