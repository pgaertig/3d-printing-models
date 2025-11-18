#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

DL = 102
DH = 100
DD = 29
T = 2

#part = Box(BL, BH, BD, align=(Align.MIN, Align.MIN, Align.MIN))
#part -= Pos(0,T,0) * Box(BL-T, BH-2*T,BD-T, align=(Align.MIN, Align.MIN, Align.MIN))
device_sk = Pos(0,0) * Rectangle(DL, DD)
device = extrude(device_sk, DH)
port1_sk = Circle(7)
port1 = extrude(port1_sk, -T*2)
port2_sk = Pos(30, 0) * Circle(11)
port2 = extrude(port2_sk, -T*2)
vent1_sk = Plane(device.faces().sort_by(Axis.X)[0]) * Rectangle(20,72)
vent1 = extrude(vent1_sk, T*2)
vent2_sk = Plane(device.faces().sort_by(Axis.X)[-1]) * Rectangle(20,72)
vent2 = extrude(vent2_sk, T*2)
front_sk = Plane(device.faces().sort_by(Axis.Y)[0]) * Rectangle(DL-20, DH-20)
front = extrude(front_sk, T*2)

slot_sk = Rectangle(DL+T*2, DD+T*2)
slot = Pos(0,0, -T) * extrude(slot_sk, DH/2)

part = slot - (device + port1 + port2 + vent1 + vent2 + front)


ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")