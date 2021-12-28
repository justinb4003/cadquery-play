import cadquery as cq

mount_plate_h = 75
mount_plate_w = 75
mount_plate_d = 6
screw_offset = 18

hole_d = 22
screw_d = 6.2

mount_plate = (
    cq.Workplane("XY")
      .rect(mount_plate_w, mount_plate_h)
      .extrude(mount_plate_d)
      .edges(">Z").chamfer(2)
      #.rect(mount_plate_w-screw_offset, mount_plate_h-screw_offset, forConstruction=True)
      .rect(mount_plate_w-screw_offset, 0, forConstruction=True)
      .vertices().circle(screw_d/2).cutThruAll()
)

bracket_w = 50
bracket_h = 25
bracket_d = 7

bracket_offset = 15
for o in [-bracket_offset, bracket_offset]:
  mount_bracket = (
      cq.Workplane("YZ")
        .workplane(offset=o)
        .center(0, mount_plate_d)
        .lineTo(-bracket_w/2, 0)
        .lineTo(0, bracket_h)
        .lineTo(bracket_w/2, 0)
        .close()
        .center(0, bracket_h)
        .circle(hole_d/2+3)
        .extrude(bracket_d * o/bracket_offset)
        .center(0, 0)
        .circle(hole_d/2).cutThruAll()
  )
  mount_plate = mount_plate.union(mount_bracket)

## Make a sleeve to fit between the gaps
sleeve_arm_length = 50
sleeve_arm_width = 8
sleeve_height = 2*bracket_offset-2*bracket_d
sleeve_hole_offset = 9
sleeve = (
  cq.Workplane("YZ")
    .workplane(offset=-bracket_offset)
    .center(0, bracket_h+mount_plate_d)
    .circle(hole_d/2+3).extrude(2*bracket_offset)
    .circle(hole_d/2).cutThruAll()
    .faces(">Z").vertices("<XY").workplane()
    .center(-bracket_offset, 0)
    .rect(2*bracket_offset, sleeve_arm_width).extrude(sleeve_arm_length)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(0, sleeve_hole_offset)
    .circle(hole_d/2).cutThruAll()
    .edges("|Z").fillet(6)
    .edges("|Y").fillet(2)
)

# Make an outer sleeve to fit around the
# this can be used to fit to the final
# presentation piece (book holder/tablet holder)
osleeve = (
  cq.Workplane("YZ")
    .workplane(offset=-(bracket_offset+bracket_d))
    .center(0, bracket_h+mount_plate_d)
    .circle(hole_d/2+3).extrude(2*(bracket_d+bracket_offset))
    .circle(hole_d/2).cutThruAll()
    .faces(">Z").vertices("<XY").workplane()
    .center(-(bracket_offset+bracket_d), 0)
    .rect(2*(bracket_offset+bracket_d), sleeve_arm_width).extrude(sleeve_arm_length)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(0, sleeve_hole_offset)
    .circle(hole_d/2).cutThruAll()
)

osleeve_cut = (
  cq.Workplane("YZ")
    .workplane(offset=-(bracket_offset))
    .center(0, bracket_h+mount_plate_d)
    .circle(hole_d/2+3).extrude(2*bracket_offset, combine=False)
)

osleeve = osleeve.cut(osleeve_cut)
osleeve = osleeve.edges("|Z").fillet(6).edges("|Y").fillet(2)

# Leave a 4.5mm gap between bushing in case somebody wants to
# mush a 608 bearing in there with some spacers to make it smooth
bushing_h_wiggle = 4.5
sleeve_bushing = (
  cq.Workplane("YZ")
    .workplane(offset=bushing_h_wiggle)
    .center(0, bracket_h+mount_plate_d)
    .circle((hole_d-1)/2).extrude(bracket_offset+bracket_d-bushing_h_wiggle)
    .faces(">X")
    .circle(hole_d/2+3).extrude(2)
    .edges("<X").chamfer(1)
    .edges(">X").chamfer(1)
    .circle(screw_d/2).cutThruAll()
)

cq.exporters.export(sleeve_bushing, 'output/sleeve_bushing.stl')
print('sleeve bushing out')

from math import floor

## Begin the arm
arm_w = 8
arm_h = 30 
# Variable number of holes are supported as long as it is an odd number
arm_holes = 3
hole_spacing = hole_d * 1.3
arm_l = (hole_spacing+1)*arm_holes
holes = []
for x in range(-floor(arm_holes/2), floor(arm_holes/2)+1):
  holes.append((hole_spacing*x, 0))

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
)


# Now create a bushing to fit in the arm's holes
arm_bushing = (
    cq.Workplane("XY")
      .circle((hole_d+5)/2).extrude(2)
      .circle(hole_d/2).extrude(arm_w-1)
      .circle(screw_d/2).cutThruAll()
      .edges(">Z").chamfer(1)
)

# Now make a bushing with a section cut out for parts
# that sagged horribly in 3d printing but you don't
# want to throw away. This works well for me.
arm_bushing_slop = (
    cq.Workplane("XY")
      .circle((hole_d+5)/2).extrude(2)
      .circle((hole_d-3)/2).extrude(arm_w-1)
      .circle(screw_d/2).cutThruAll()
      .edges(">Z").chamfer(1)
)

arm_bushing_cut = (
  arm_bushing_slop
      .faces(">Z").workplane(centerOption="CenterOfBoundBox")
      .center(0, -11).rect(23, 10).extrude(-arm_w+2, combine=False)
)

arm_bushing_slop = arm_bushing_slop.cut(arm_bushing_cut)

# Now create the plate to hold a book/tablet
plate_w = 200
plate_h = 125
plate_d = 7
plate_lip_h = 25
plate_lip_d = 45

book_hook = (
    cq.Workplane("XY")
      .rect(arm_w, arm_h)
      .extrude(hole_spacing*2)
      .faces(">X").workplane(centerOption="CenterOfBoundBox")
      .center(0, -hole_spacing/2)
      .circle(hole_d/2).cutThruAll()
      .faces("<Z").edges("|X").fillet(6)
      .edges("|Z").fillet(2)
)

book_plate = (
    book_hook
      .faces(">Z").workplane(centerOption="CenterOfBoundBox")
      .center(0, plate_h/2-arm_h/2)
      .rect(plate_w, plate_h).extrude(plate_d)  # Create the back plate
      .faces("<Y").center(0, -plate_h/2+plate_d/2)
      .rect(plate_w, plate_d).extrude(plate_lip_d)  # Make bottom lip
      .faces(">Z").workplane(centerOption="CenterOfBoundBox")
      .center(0, plate_lip_h/2-plate_d/2)
      .rect(plate_w, plate_lip_h).extrude(plate_d)  # Make front lip
      .faces("+Y").edges("|X").fillet(2)
      .faces(">X").edges("|Y").fillet(2)
      .faces("<X").edges("|Y").fillet(2)
)

book_plate = book_plate.union(book_hook)

cq.exporters.export(mount_plate, 'output/mount_plate.stl')
cq.exporters.export(arm, 'output/arm.stl')
cq.exporters.export(arm_bushing, 'output/arm_bushing.stl')
cq.exporters.export(arm_bushing_slop, 'output/arm_bushing_slop.stl')
cq.exporters.export(sleeve, 'output/sleeve.stl')
cq.exporters.export(osleeve, 'output/osleeve.stl')
cq.exporters.export(book_plate, 'output/book_plate.stl')
