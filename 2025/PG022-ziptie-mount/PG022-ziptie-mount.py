#!/usr/bin/env python3
from build123d import *
import ocp_vscode as ocp
import os

from build123d import RectangleRounded, GridLocations

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

PLATE_T = 3
SPACE_H = 55
SPACE_W = 55
CH_CNT = int(SPACE_W/10)
CH_GT = 3
CH_T = CH_GT + PLATE_T
CH_H = 45
CH_W = 55
PLATE_H = SPACE_H * 1.5
PLATE_W = SPACE_W * 1.5

plate_sk = RectangleRounded(PLATE_W, PLATE_H, 5)
plate = extrude(plate_sk, -PLATE_T)


channel_sk =(RectangleRounded(CH_W, CH_T, 2)  -
             (GridLocations(12,0, 4, 1) * RectangleRounded(8, CH_T-CH_GT, 1)))
channel = Pos(0,CH_H/2,1) * Rot(90,0,0) * extrude(channel_sk, CH_H)
#channels = GridLocations(0, SPACE_H+CH_H, 1, 2) * channel

part = plate + channel

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")