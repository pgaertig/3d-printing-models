#!/usr/bin/env python3
# %%

from build123d import *
from ocp_vscode import *
import os

# %%
radius1 = 10
height1 = 2.5
radius2t = 3.0
radius2b = 3.2
height2 = 15
smoothing_fillet = 0.5
cut_start_pct = 0.25

part = Part()
part += Cylinder(radius1, height1, align=[Align.CENTER, Align.CENTER, Align.MAX])
part += Cone(radius2b, radius2t, height2, align=[Align.CENTER, Align.CENTER, Align.MIN])
part -= Pos(0,0,height2*cut_start_pct) * Box(radius2b*2, 1, height2, align=[Align.CENTER, Align.CENTER, Align.MIN])
        
part = chamfer(part.edges().group_by(Axis.Z)[0:3], smoothing_fillet)

show(part)

# %%
file_name = os.path.splitext(os.path.basename(__file__))[0] + ".stl"
export_stl(part, file_name)