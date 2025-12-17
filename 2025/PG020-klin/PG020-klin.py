#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from ezdxf.addons.drawing.text import Alignment

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

el_l = 70
el_sw = 20
el_sh = 1
el_sr = 0.1
el_ew = 30
el_eh = 6
el_er = 3
handle_h = el_eh * 2
handle_l = el_eh


start_sc = fillet(Rectangle(el_sw, el_sh).vertices().group_by(Axis.Y)[-1], el_sr)
end_sc = Pos(Z=el_l, Y=el_eh/2) * fillet(Rectangle(el_ew, el_eh).vertices().group_by(Axis.Y)[-1], el_er)
slope = loft([start_sc, end_sc])
handle = Pos(Z=el_l+handle_l/2, Y=el_eh) * Box(el_ew, handle_h, el_eh)

pre_slope_e = slope.edges()
part = slope + handle
part = fillet((part.edges() - pre_slope_e).group_by(Axis.Y)[-1], el_er/2)
part = fillet((part.edges() - pre_slope_e).filter_by(Axis.Y).group_by(Axis.Z)[-1], el_er/4)

ocp.show(part)


# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")