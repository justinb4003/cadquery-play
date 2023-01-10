import cadquery as cq

filter_width = 20
fan_width = 120
fan_holes = 105

fan_plate = (
    cq.Workplane("XY")
        .rect(fan_width, fan_width + filter_width*2)
        .extrude(8)
        .rect(fan_holes, fan_holes, forConstruction=True)
        .vertices().circle(2).cutThruAll()
)

topface = fan_plate.faces(">Z")
fan_plate = fan_plate.faces(">Z").edges("not (<X or >X or <Y or >Y)").chamfer(3)


slot_width = 4
total_y = fan_width + filter_width*2
fan_plate = (
    topface
    .center(0, total_y/2)
    .rect(120, slot_width).extrude(20)
    .center(0, -filter_width)
    .rect(120, slot_width).extrude(20)
    .center(0, -fan_width)
    .rect(120, slot_width).extrude(20)
    .center(0, -filter_width)
    .rect(120, slot_width).extrude(20)
)


fan_plate = fan_plate.faces("<Z").edges("|X").fillet(1.5)
fan_plate = fan_plate.faces(">Z").edges("|X").fillet(1.5)

fan_plate = fan_plate.faces("<Z").circle(55).cutThruAll()
cq.exporters.export(fan_plate, 'output/cr_fanplate.stl')