
import cadquery as cq

inch = 25.4

motor_od = 1.5 * inch
motor_depth = 2.5 * inch
mount_spacing = 1.25 * inch
mount_screw_od = (10/64) * inch
nub_width = 0.5 * inch
nub_depth = 0.25 * inch

mount = (
    cq.Workplane("YZ")
      .rect(motor_od+inch, motor_od + 2*inch)
      .extrude(0.25 * inch)
)

mount = (
  mount.faces(">X")
       .polygon(6, mount_spacing, forConstruction=True)
       .vertices()
       .circle(mount_screw_od / 2)
       .cutThruAll()
)

mount = (
  mount.faces(">X")
       .circle(nub_width / 2)
       .cutThruAll()
)

base_width = motor_od + 2*inch

motor_cut = (
  mount.faces(">X")
       .circle(motor_od / 2)
       .extrude(motor_depth, combine=False)
)

base = (
    cq.Workplane("XZ")
      .workplane(offset=0, invert=True)
      .center((motor_od+inch)/2, 0)
      .rect(motor_depth + inch, base_width)
      .extrude(1 * inch)
)

mount = mount.union(base)
mount = mount.cut(motor_cut)

cq.exporters.export(mount, 'output/toast_motor.stl')