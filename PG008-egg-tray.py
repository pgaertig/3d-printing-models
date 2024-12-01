#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

rows = 2
cols = 5
egg_hole_d = 38.5 * MM
egg_space = 5 * MM
tray_t = 25 * MM
board_w = cols * (egg_hole_d + egg_space) + egg_space
board_h = rows * (egg_hole_d + egg_space) + egg_space
board_t = 5 * MM
board_rad = 5 * MM
support_d = egg_space

# Top board
outer_sk = RectangleRounded(width=board_w, height=board_h, radius= board_rad)
tray = extrude(outer_sk, amount=board_t)
tray -= (GridLocations(egg_hole_d + egg_space, egg_hole_d + egg_space, cols, rows)
         * extrude(Circle(egg_hole_d/2), amount=board_t))

# Frame
frame_sk = (outer_sk - offset(outer_sk, amount=-egg_space))
frame = extrude(frame_sk, amount=-board_t)
tray += frame

# Legs
legs_sk = (frame_sk
           - Rectangle(width=board_w, height=board_h - tray_t)
           - Rectangle(width=board_w - tray_t, height=board_h))
legs = extrude(legs_sk, amount=-(tray_t - board_t))
tray += legs

# Chamfer the shape
egg_hole_top_e = tray.edges().group_by(Axis.Z)[-1]
tray = chamfer(egg_hole_top_e, length=egg_hole_d/20 * MM) #chamfer the top
last_edges = tray.edges()

bottom_chamfer = tray.edges().group_by(Axis.Z)[0:-5]
#show(bottom_chamfer)
tray = chamfer(bottom_chamfer, length= 1 * MM) # chamfer the bottom

# Supporting pillars
if rows > 1 and cols > 1:
    last_edges = tray.edges()
    board_support_sk = GridLocations(egg_hole_d + egg_space, egg_hole_d + egg_space, cols - 1, rows - 1) * Circle(
        support_d / 2)
    board_support = (GridLocations(egg_hole_d + egg_space, egg_hole_d + egg_space, cols-1, rows-1) *
                      extrude(Circle(support_d/2),amount=-(tray_t - board_t)) )

    tray += board_support
    tray = fillet((tray.edges()-last_edges).group_by(Axis.Z)[-1], radius=egg_space)



print(f"Egg tray size {tray.volume/1000}")

show(tray)


# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_stl(tray, file_name + ".stl")