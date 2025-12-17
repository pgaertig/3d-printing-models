from build123d import *
from bd_warehouse.thread import *
from ocp_vscode import *

#import logging
#logging.basicConfig(level=logging.INFO)

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True, black_edges=True)

# %%
cover_d = 120
inner_ring_h = 20
floor_h = 5
cover_h = inner_ring_h*2 + floor_h
cover_chamfer = 5
cable_hole_d = 11

inner_ring_d = cover_d*0.95
ring_hole_ratio = 0.8
hole_d = inner_ring_d * ring_hole_ratio

tolerance = 0.99 # 3D printing tolerance

thread = IsoThread(
        major_diameter=inner_ring_d * tolerance,
        pitch=inner_ring_h/3,
        length=inner_ring_h,
        external=True,
        end_finishes=("chamfer", "fade"),
        hand="right",
        align=(Align.CENTER, Align.CENTER, Align.MIN),
)


print(thread.min_radius)
print(thread.length)

cylinder = Cylinder(radius=thread.min_radius+0.001,
                    height=inner_ring_h,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)
                    )
part = Compound([thread, cylinder])
hole = Circle(radius=hole_d/2)
part -= extrude(hole,inner_ring_h)
handle_size = hole_d/3

handle_sk = Pos(-hole_d/2+handle_size/2,0) * hole & Pos(hole_d/2-handle_size,0) * Circle(hole_d/4)
two_handles = PolarLocations(hole_d/2-handle_size/2, 2) * handle_sk
handle = extrude(two_handles, inner_ring_h/2)
last = handle.edges()
slot = Pos(handle_size/6, 0,0) * extrude(SlotOverall(handle_size * 0.5, 5), inner_ring_h)
handle -= PolarLocations(hole_d/2-handle_size/2, 2) * slot
handle = chamfer(handle.edges().group_by(Axis.Z)[-1] - last, 2)
part += handle

show(part.move(Pos(0,0,-cover_h*2)))

# %%

TOP = (Align.CENTER, Align.CENTER, Align.MAX)
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

part2 = Cylinder(radius=cover_d/2, height=cover_h, align = TOP)
part2 -= Pos(0,0,-floor_h) * Cylinder(radius=inner_ring_d/2, height=cover_h, align=TOP)

part2 = chamfer(part2.edges().group_by(Axis.Z)[-2], cover_chamfer/2) # inner chamfer
part2 = chamfer(part2.edges().group_by(Axis.Z)[-1], cover_chamfer) # outer chamfer

part2 -= Cylinder(radius=cable_hole_d/2, height=cover_h)

thread2 = IsoThread(
        major_diameter=inner_ring_d,
        pitch=inner_ring_h/3,
        length=inner_ring_h,
        external=False,
        end_finishes=("fade", "chamfer"),
        hand="right",
        align=BOTTOM,
)
part2 += Pos(0,0, -cover_h) * thread2
show(part, part2)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_stl(part, file_name + "-mount.stl")
export_stl(part2, file_name + "-cover.stl")