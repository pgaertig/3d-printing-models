#!/usr/bin/env python3
from build123d import *
from ocp_vscode import *

show_clear()
set_defaults(reset_camera=Camera.KEEP, ortho=True)

# %%
show_clear()
wall_h = 60 * MM   # 70 org
wall_w = 120 * MM
wall_t = 8 * MM
floor_w = 48 * MM
floor_t = 5 * MM
support_h = 20 * MM
limit_h = 20 * MM
limit_t = 5 * MM
support_w = wall_t + floor_w + limit_t
fillet_r = 2.5

cutout_bottom_w = 90 * MM
cutout_top_w = 55 * MM

screw_hole_r = 2.6 * MM



side_shape = make_face(Polyline(
        (0,0),
        (wall_h, 0),
        (wall_h, wall_t),
        (support_h, wall_t),
        (support_h, wall_t+floor_w),
        (support_h + limit_h, wall_t + floor_w),
        (support_h + limit_h, support_w),
        (support_h - floor_t, support_w),
        (0, wall_t), close= True
    ).edges())

side_shape = fillet(side_shape.vertices().group_by(Axis.Y)[1:], fillet_r)
part = extrude(side_shape, wall_w/2, both=True)


first_Y_e = part.edges().group_by(Axis.Y)[0] # Don't fillet wall side
part = fillet(part.edges() - first_Y_e, 1)

# Cut out the side hole
p1 = (support_h - floor_t, wall_t * 1.5)
p3 = (floor_t * 1.4, wall_t * 1.5)
side_hole_sk = make_face([
    Polyline(
        p1,
        (support_h - floor_t,  support_w - limit_t * 3),
        p3),
    ThreePointArc(
        p1, (support_h / 2, wall_t), p3
    )
])
side_hole = side_hole_sk
part -= extrude(side_hole, wall_w/2, both=True)

# Cut out front hole
cutout_lines = Curve() + [
    Polyline(
        (+limit_h / 2, cutout_bottom_w/2),
        (+limit_h/2, - cutout_bottom_w/2),
        (-limit_h/2, - cutout_top_w/2),
        (-limit_h/2, + cutout_top_w/2), close=True
    )
]
cutout_face =  make_face(cutout_lines)
cutout_sk = Plane.XZ * Pos(limit_h/2 + support_h,0, -support_w) * cutout_face

pre_cut_ed = part.edges()
part-=extrude(cutout_sk, amount=limit_t+fillet_r)

# Make a method which iterates n= from 0 to size of `ed` which is array, each time testing slice [0:n] with fillet, if it fails return failing edge
def fillet_test(edges, r):
    ignored_edges = []
    f = None
    for i, ed in enumerate(edges):
        try:
            if i>1:
                f=fillet(edges[0:i]-ignored_edges, r)
                show(f)
        except:
            #ed.color = (1.,0,0)
            ignored_edges.append(ed)
            #show_object(ed)
            #break
    return f

last = part.edges() - pre_cut_ed
part = fillet(last.sort_by(Axis.Y), 1)

part_back_fc = part.faces().filter_by(Axis.Y).group_by(Axis.Y)[1][0] #Wall element - inner
positioning = (Plane(part_back_fc) *
         GridLocations(0, wall_w/3, 1,3))


last = part.edges()
part -= (positioning *
         Hole(screw_hole_r, wall_t))

last = part.edges() - last


#part_back_fc = part.faces().filter_by(Axis.Y).group_by(Axis.Y)[1][0].edges() #Wall element - inner
#part_back_fc = part_back_fc.edges()
part = chamfer(last.group_by(Axis.Y)[-1], 3)

show(part)

# %%

file_name = os.path.splitext(os.path.basename(__file__))[0]
export_step(part, file_name + ".step")