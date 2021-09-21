
import cadquery as cq

inch = 25.4

motor_od = 1.5 * inch
motor_depth = 2.5 * inch
mount_spacing = 1.25 * inch
mount_screw_od = (10/64) * inch
motor_tiedown_od = (1/8) * inch  # Yeah I know
nub_od = 0.5 * inch
nub_depth = 0.25 * inch
wall_thickness = 0.25 * inch
wall_height = motor_od+inch
wall_length = motor_od + 2*inch

mount = (
    cq.Workplane("YZ")
      .rect(wall_height, wall_length)
      .extrude(wall_thickness)
)

mount = (
  mount.faces(">X")
       .polygon(6, mount_spacing, forConstruction=True)
       .vertices()
       .circle(mount_screw_od / 2)
       .cutThruAll()
)

base_width = motor_od + 2*inch

motor_cut = (
  mount.faces(">X")
       .circle(motor_od / 2)
       .extrude(motor_depth, combine=False)
)

nub_cut = (
  mount.faces(">X")
       .circle(nub_od / 2)
       .extrude(-wall_thickness, combine=False)
)

base = (
  mount.faces(">X")
       .workplane()
       .center(wall_height/4, 0)
       .rect(wall_height/2, wall_length)
       .extrude(motor_depth, combine=False)
)

motor_strap_holes = (
  base.faces("<Y")
      .workplane()
      .center(inch, 0)
      #rect(uppy-down, lefty-right)
      .rect(1.25*inch, motor_od+inch, forConstruction=True)
      .vertices()
      .circle(motor_tiedown_od / 2)
      .extrude(-0.5*inch, combine=False)
)

mount = mount.union(base)
mount = mount.cut(motor_strap_holes)
mount = mount.cut(nub_cut)
mount = mount.cut(motor_cut)

cq.exporters.export(mount, 'output/toast_motor.stl')