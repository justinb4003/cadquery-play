import sys
import cadquery as cq

case_depth = 25

outer_w = 47
outer_h = 58 # added 7 for new notch
inner_w = 39.5
inner_knock_w = 18.5
inner_knock_h = 7
inner_knock_top_w = 7
inner_knock_step_h = 2
inner_h = 37.1

board_thickness = 1.8
case_thickness = 3

case = (
    cq.Workplane("XY")
      .rect(outer_w, outer_h)
      .extrude(case_depth)
)

first_cut = (
    cq.Workplane("XY")
      .center(0, -case_thickness)
      .polyline([
            (0, 0),
      ])
      .rect(inner_w, inner_h)
      .workplane(offset=case_depth/2-board_thickness)
      .extrude(case_depth/2+board_thickness, combine=False)
)

cut_h = 50.0
second_cut = (
    cq.Workplane("XY")
      .center(0, (cut_h-inner_h)/2-8)
      .rect(19.5, cut_h)
      .workplane(offset=case_depth/2-board_thickness)
      .extrude(case_depth/2+board_thickness, combine=False)
)

case = case.cut(first_cut).cut(second_cut)

case = (
    case.edges("|Z")
        .edges("not(<X or >X or <Y or >Y)")
        .edges("not(<X or >X or <Y or >Y)")
        .edges("not(<Y)")
        .chamfer(1)
)

"""
case = (
    case.edges("|Z").edges("<X or >X").fillet(4)
)
"""

w = inner_w
h = inner_h
third_cut = (
    cq.Workplane("XY")
      .center(0, -case_thickness)
      .polyline([
          (-w/2, -h/2),
          (-w/2, h/2),
          (10, h/2),
          (10, h/2-8), # Create a little jog around the 3rd mounting screw
          (w/2, h/2-8),
          (w/2, -h/2),
      ]).close()
      .extrude(case_depth-3, combine=False)
)

case = case.cut(third_cut)

# Make camera hole
camera_offset = 15.5
camera_d = 16
lens_sq_side = 14.8
lens_sq_screws = 4.8
case = (
    case.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .center(0, camera_offset) 
        .circle(camera_d/2).cutThruAll()
)

# Make lense mounting bracket depression
lmb_cut_square = (
    case.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .center(0, camera_offset) 
        .workplane(offset=-(case_depth/2+board_thickness))
        .rect(lens_sq_side, lens_sq_side).extrude(-4, combine=False)
)

lmb_cut_screw_gaps = (
    case.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .center(0, camera_offset) 
        .rect(lens_sq_screws, lens_sq_side+(lens_sq_screws*2))
        .extrude(-(case_depth/2+board_thickness)-4, combine=False)
)

case = case.cut(lmb_cut_square).cut(lmb_cut_screw_gaps)


# Make screw holes
screw_od = 3.2
case = (
    case.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .center(-3.2, -18.4)
        .circle(screw_od/2).cutThruAll()
        .center(6.4, 0)
        .circle(screw_od/2).cutThruAll()
        .center(11.0, 7.5)
        .circle(screw_od/2).cutThruAll()
)

# USB Port access
usb_port = (
    case.faces("<X").workplane(centerOption="CenterOfBoundBox")
        .center(10, -2)
        .rect(10, 6.25).extrude(-(case_thickness+2), combine=False)
)

# Slot for SPI cables to come in 
spi_port = (
    case.faces(">X").workplane(centerOption="CenterOfBoundBox")
        .center(-10, -9)
        .rect(22, 17).extrude(-(case_thickness+2), combine=False)
)

# Config button access
config_button_port = (
    case.faces("<Y").workplane(centerOption="CenterOfBoundBox")
        .center(-13, -11)
        .rect(6, 17).extrude(-(case_thickness+8), combine=False)
)
case = case.cut(usb_port)
case = case.cut(spi_port)
case = case.cut(config_button_port)

# Robot mounting holes
inch = 25.4
hole_spacing = (3/8)*inch
top_hole_distance = hole_spacing*3
vert_hole_distance = hole_spacing*7
mount_block_w = 12.5
mount_block_h = 10
ten_screw_d = 5


case = (
    case.faces(">Z")
        .workplane(centerOption="CenterOfBoundBox")
        .rect(top_hole_distance, vert_hole_distance, forConstruction=True)
        .vertices("not(<X and <Y)") # Skip one vertex else it covers the config button
        .rect(mount_block_w, mount_block_h).extrude(-case_depth)
)

case = (
    case.faces(">Z")
        .workplane(centerOption="CenterOfBoundBox")
        .rect(top_hole_distance, vert_hole_distance, forConstruction=True)
        .vertices("not(<X and <Y)") # Skip one vertex else it covers the config button
        .circle(ten_screw_d/2).cutThruAll()
)

case = (
    case.edges("|Z")
        .edges(">X or <X or >Y or <Y")
        .fillet(2)
)

cq.exporters.export(case, 'output/pixy2_case.stl')
