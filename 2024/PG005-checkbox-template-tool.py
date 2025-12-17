#!/usr/bin/env python3
# %%

from build123d import *
from ocp_vscode import *
import timeit
import os
import logging

logging.basicConfig(level=logging.DEBUG)

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%

print("2D", timeit.timeit("chamfer(Rectangle(10,10).vertices(), 1)", globals=globals(), number=1))
print("3D", timeit.timeit("chamfer(Box(10,10,10).edges(), 1)", globals=globals(), number=1))

# %%

area_size = 5   # 0.5 cm dotted paper
box_size_v = 3
box_size_h = 3
boxes_no_v = 31  # number of box rows
boxes_no_h = 3   # number of box columns

thickness = 2
margin = 5

reces_thickness = thickness / 2
reces_margin = margin / 2
frame_w = boxes_no_v * area_size + margin
frame_h = boxes_no_h * area_size + margin

handle_w = (frame_w - margin) * 0.2  
handle_h = (frame_h - margin)
extra_areasize = area_size * 1.1  # Bigger size to see alignment dots in handle holes 
top_handle_loc = (-frame_w/4, -(frame_h-margin)/2-handle_h/2)
bottom_handle_loc = (frame_w/4, -(frame_h-margin)/2-handle_h/2)

frame_round_radius = 2

smooth = True
#smooth = False #Fast render

with BuildPart() as part:

    with BuildSketch() as boxes:
        Rectangle(frame_w - reces_margin,frame_h - reces_margin)
        with GridLocations(area_size, area_size, boxes_no_v, boxes_no_h):
            Rectangle(box_size_h, box_size_v, mode=Mode.SUBTRACT)
    extrude(amount=reces_thickness)
    if smooth: chamfer(faces().filter_by(Axis.Z).sort_by(Axis.Z)[1].inner_wires().edges(), length=0.5)

    with BuildSketch() as frame:
        RectangleRounded(frame_w, frame_h, frame_round_radius)
        with Locations(top_handle_loc): RectangleRounded(handle_w, handle_h, frame_round_radius)
        with Locations(bottom_handle_loc): RectangleRounded(handle_w, handle_h, frame_round_radius)
        RectangleRounded(frame_w - reces_margin*2,frame_h - reces_margin*2, frame_round_radius/2, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    #if smooth: fillet(part.edges(Select.LAST).filter_by(Axis.Z).()[0], radius=0.1)
    if smooth: chamfer(part.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.3)

    with BuildSketch() as guides:
        with Locations(top_handle_loc):
            with GridLocations(area_size, area_size, 3, 1):
               Rectangle(extra_areasize, extra_areasize)
        with Locations(bottom_handle_loc):
            with GridLocations(area_size, area_size, 3, 1):
               Rectangle(extra_areasize, extra_areasize)
    extrude(amount=thickness, mode=Mode.SUBTRACT)            
    if smooth: chamfer(part.edges(Select.LAST).group_by(Axis.Z)[-1], length=1)

show(part)

# %%
file_name = os.path.splitext(os.path.basename(__file__))[0] + ".stl"
export_stl(part.part, file_name)