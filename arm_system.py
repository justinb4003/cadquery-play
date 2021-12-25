import cadquery as cq

mount_plate_h = 75
mount_plate_w = 75
mount_plate_d = 6

mount_plate = (
    cq.Workplane("XY")
      .rect(mount_plate_w, mount_plate_h)
      .extrude(mount_plate_d)
)

bracket_w = 50
bracket_h = 25
bracket_d = 10

mount_bracket = (
    cq.Workplane("YZ")
      .center(0, mount_plate_d)
      .lineTo(-bracket_w/2, 0)
      .lineTo(0, bracket_h)
      .lineTo(bracket_w/2, 0)
      .close()
      .extrude(bracket_d)
)

mount_plate = mount_plate.union(mount_bracket)

## Begin the arm
arm_w = 8
arm_h = 30 
arm_l = 150
hole_d = 22
hole_spacing = hole_d * 1.3
holes = [(-hole_spacing*2, 0),
         (-hole_spacing, 0),
         (0, 0),
         (hole_spacing, 0),
         (hole_spacing*2, 0)]

print(holes)
arm = (
    cq.Workplane("XY")
      .rect(arm_l, arm_w)
      .extrude(arm_h)
      .faces(">Y")
      .workplane(centerOption="CenterOfBoundBox")
      .pushPoints(holes)
      .circle(hole_d/2).cutThruAll()
      .edges("|Y").fillet(6)
      .edges("|X").fillet(2)
      # .edges("|Z").fillet(3)
)

screw_d = 6.2

arm_bushing = (
    cq.Workplane("XY")
      .circle((hole_d+5)/2).extrude(2)
      .circle(hole_d/2).extrude(arm_w-1)
      .circle(screw_d/2).cutThruAll()
      .edges(">Z").chamfer(1)
)

cq.exporters.export(mount_plate, 'output/mount_plate.stl')
cq.exporters.export(arm, 'output/arm.stl')
cq.exporters.export(arm_bushing, 'output/arm_bushing.stl')