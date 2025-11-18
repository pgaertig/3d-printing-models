#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

# Device dimensions
DL = 172
DH = 74
DD = 53
#Thickness
T = 4

#part = Box(BL, BH, BD, align=(Align.MIN, Align.MIN, Align.MIN))
#part -= Pos(0,T,0) * Box(BL-T, BH-2*T,BD-T, align=(Align.MIN, Align.MIN, Align.MIN))
device_sk = Pos(0,0) * Rectangle(DL, DD)
device = extrude(device_sk, DH)
vent1_sk = Plane(device.faces().sort_by(Axis.X)[0]) * Rectangle(DD,45)
vent1 = extrude(vent1_sk, T*2)
vent2_sk = Plane(device.faces().sort_by(Axis.X)[-1]) * Rectangle(DD,45)
vent2 = extrude(vent2_sk, T*2)
bottom1_sk = Plane(device.faces().sort_by(Axis.Z)[0])  * Rectangle(20,20)
bottom1 = GridLocations(25, 25, 7, 2) * extrude(bottom1_sk, T)

#front1 = Pos(0, -T-DD/2, DH/3) * Rot(90) * GridLocations(25, 25, 7, 2) * extrude(bottom1_sk, T*2)

slot_sk = Rectangle(DL+T*2, DD+T*2)
slot = Pos(0,0, -T) * extrude(slot_sk, DH-20)

part = slot - (device + vent1 + vent2 + bottom1)


ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")