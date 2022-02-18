from tkinter import W
import cadquery as cq   

motor_width = 18.8
motor_depth = 22.2
motor_height = 40
shell_thickness = 3

leg_height = motor_height + 25
leg_hole_distance = 18.7
leg_hole_diamter = 3.2

mount_screw_diamter = 5


leg = (
    cq.Workplane("XY")
      .rect(motor_width+shell_thickness*2, motor_depth+shell_thickness*2)
      .extrude(leg_height)
)

leg = (
    leg.faces("<Z").workplane()
       .circle(mount_screw_diamter/2).cutThruAll()
)

motor_cut = (
    leg.faces(">Z")
       .workplane(invert=True)
       .rect(motor_width, motor_depth)
       .extrude(motor_height, combine=False)
)

leg = leg.cut(motor_cut)

leg = (
    leg.faces(">X").workplane()
    .center(leg_hole_distance/2, leg_height-8)
    .circle(leg_hole_diamter/2).cutThruAll()
    .center(-leg_hole_distance, 0)
    .circle(leg_hole_diamter/2).cutThruAll()

)

leg = (
    leg.faces(">Z")
       .edges("not(<X or >X or <Y or >Y)")
       .chamfer(0.5)
)


cq.exporters.export(leg, 'leg.stl')
