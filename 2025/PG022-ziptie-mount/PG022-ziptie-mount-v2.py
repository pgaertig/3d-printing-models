#!/usr/bin/env python3

import ocp_vscode as ocp
import os

from build123d import RectangleRounded, GridLocations, extrude, Circle, Pos, Rot, export_step

ocp.show_clear()
ocp.set_defaults(reset_camera=ocp.Camera.KEEP, ortho=True, black_edges=True)

# %%

LAYER_H = 0.2

BASE_T = 3
BASE_H = 55
BASE_W = 90
BASE_R = 2

PADDING_H = 0
PADDING_W = 10
PADDING_T = 3
PADDING_R = 5
PADDING_HOLE_R = 2

CH_SP_MIN = 12  # Minimal space between channel centers
CH_W = 8 # Channel width

CH_CNT = int((BASE_W - 2*(CH_SP_MIN-CH_W)) / CH_SP_MIN)
CH_SP = (BASE_W - 2*(CH_SP_MIN-CH_W)) / CH_CNT
print("Channel count:", CH_CNT, " Channel spacing:", CH_SP)

CH_GT = 3
CH_T = CH_GT + BASE_T
CH_R = 1

padding_sk = RectangleRounded(BASE_W + PADDING_W * 2, BASE_H + PADDING_H * 2, PADDING_R)
padding = extrude(padding_sk, -PADDING_T)

if PADDING_W >= 10:
    padding_hole = Circle(PADDING_HOLE_R)
    padding -= GridLocations(BASE_W + PADDING_W, BASE_H/1.5, 2, 2) * extrude(padding_hole, -PADDING_T + LAYER_H * 2)

channel_sk = RectangleRounded(CH_W, CH_T-CH_GT, CH_R)
base_sk = RectangleRounded(BASE_W, CH_T, BASE_R) - (GridLocations(CH_SP,0, CH_CNT, 1) * channel_sk)
base = Pos(0, BASE_H/2, CH_GT/3) * Rot(90,0,0) * extrude(base_sk, BASE_H)

part = padding + base

ocp.show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")