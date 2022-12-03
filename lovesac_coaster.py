import cadquery as cq

insert_od = 90
insert_h = 15
coaster_od = 120
cup_od = 100
coaster_h = 9 

screw_head_d = 6  # Mostly really the expect screw driver OD 
# 2.54mm is the height of the head of a phillips pan head m3 screw
screw_head_h = 2.54 + 0.05  # A little fudge to ensure it is sunk
screw_d = 3 + 0.1  # Fudge again
screw_extra_h = 3  # Lip of the coaster to keep around for screw to bite

insert = (
    cq.Workplane("XZ")
    .circle(insert_od/2)
    .extrude(insert_h)
)

coaster = (
    insert.faces(">Y")
    .circle(coaster_od/2)
    .extrude(coaster_h + screw_extra_h, combine=False)
)

coaster_fillet = coaster.edges(">Y").fillet(coaster_h)

cupcut = (
    coaster.faces(">Y")
    .circle(cup_od/2)
    .extrude(coaster_h-screw_extra_h-screw_head_h, combine=False)
)

coaster = coaster.edges(">Y").chamfer(4)
coaster = coaster.edges(">Y").fillet(4.5)

capture_nut_d = 5 - 0.1  # Fudge it small because we will melt into it
capture_nut_h = 8 + 0.2  # Fudge deep for extra room
insert = (
    insert.faces(">Y")
    .workplane(invert=False)
    .cboreHole(screw_d, capture_nut_d, capture_nut_h)
)

coaster = (
    coaster.faces("<Y")
    .circle(screw_d/2).cutThruAll()
)

# coaster = coaster.union(insert)
coaster = coaster.cut(cupcut)
# coaster = coaster.edges(">Y").fillet(2)

screw_head_space = (
    coaster.faces("<Y")
    .workplane(offset=screw_extra_h, invert=True)
    .circle(screw_head_d/2).extrude(10, combine=False)
)
coaster = coaster.cut(screw_head_space)

cq.exporters.export(coaster, 'output/coaster.stl')
cq.exporters.export(insert, 'output/coaster_insert.stl')
