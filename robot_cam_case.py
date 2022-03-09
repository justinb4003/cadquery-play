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

posts = (
    cq.Workplane("XY")
      .rect(post_w, post_h, forConstruction=True).vertices()
      .circle(post_d/2).extrude(case_depth-5)
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


cq.exporters.export(case, 'output/robot_cam_case.stl')