import cadquery as cq

label_width = 4

label = (
    cq.Workplane("XY")
      .rect(75, 30)
      .extrude(label_width)
)

hook = (
    label.faces("<Z").workplane(invert=True)
         .center(0, 20)
         .circle(7)
         .extrude(label_width, combine=True)
)

hole = (
    hook.faces("<Z").workplane(invert=True)
        .circle(4)
        .extrude(label_width, combine=False)
)



label = label.union(hook).cut(hole)

label = label.edges("|Z").fillet(1)
label = label.edges(">Z").fillet(1)


cq.exporters.export(label, 'output/binlabel.stl')