import cadquery as cq

wall_thickness = 5
inner_w = 32
inner_h = 32
outer_w = inner_w + wall_thickness*2
outer_h = inner_h + wall_thickness*2
case_depth = 15

post_w = 27.5
post_h = 27.5
post_d = 7
screw_d = 3.2

lens_diamter = 17


case = (
    cq.Workplane("XY")
      .rect(outer_w, outer_h)
      .extrude(case_depth)
)

# Robot mounting holes
inch = 25.4
hole_spacing = (3/8)*inch
top_hole_distance = hole_spacing*5
vert_hole_distance = 0
mount_block_w = 12.5
mount_block_h = 10
ten_screw_d = 5



case = case.edges("|Z").fillet(2)

posts = (
    cq.Workplane("XY")
      .rect(post_w, post_h, forConstruction=True).vertices()
      .circle(post_d/2).extrude(case_depth-7)
)

screw_mounts = (
    posts.faces(">Z")
         .workplane(centerOption='CenterOfBoundBox', invert=True)
      .rect(post_w, post_h, forConstruction=True).vertices()
      .circle(screw_d/2).extrude(10, combine=False)
)

inner_case = (
    case.faces(">Z")
        .workplane(invert=True)
        .rect(inner_w, inner_h).extrude(case_depth-wall_thickness, combine=False)
)

case = case.cut(inner_case)
case = case.union(posts).cut(screw_mounts)

lens_mount_w = 14.5
lens_mount_h = 14.5
screw_mount_w = 4.5
screw_mount_h = 22

lens_cut = (
    cq.Workplane("XY")
      .workplane(offset=3)
      .rect(lens_mount_w, lens_mount_h)
      .extrude(3, combine=False)
).union(
    cq.Workplane("XY")
      .workplane(offset=3)
      .rect(screw_mount_w, screw_mount_h)
      .extrude(3, combine=False)
)

case = (
    case.faces(">Z").circle(lens_diamter/2).cutThruAll()
)

case = case.cut(lens_cut)

case = (
    case.faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .center(0, -10)
        .rect(top_hole_distance, vert_hole_distance, forConstruction=True)
        .vertices()
        .rect(mount_block_w, mount_block_h).extrude(-case_depth)
)

case = (
    case.faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .center(0, -10)
        .rect(top_hole_distance, vert_hole_distance, forConstruction=True)
        .vertices()
        .circle(ten_screw_d/2).cutThruAll()
)

case = case.edges("|Z").edges(">X").fillet(2)
case = case.edges("|Z").edges("<X").fillet(2)




cq.exporters.export(case, 'output/robot_cam_case.stl')