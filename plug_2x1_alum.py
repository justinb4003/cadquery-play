import cadquery as cq

# All dimensions in mm.
inner_w = 18
inner_h = 31
inner_d = 12.5
outer_w = 25
outer_h = 38
outer_d = 2

hole_diameter = 10

plug = (
    cq.Workplane("XY")  # start draading in the XY plane
      .rect(inner_w, inner_h)  # draw a rectangle
      .extrude(inner_d) # extrude it into a box, this is the inner part that goes into the aluminum hole  
      .faces(">Z") # Now make a workplane on the top of that box
      .rect(outer_w, outer_h) # make a new retangle the size of the outer 2x1" aluminum tube
      .extrude(outer_d) # extrude up a bit for the outer lip
)

plug = plug.edges("|Z").fillet(2) # round all edges parallel to the Z axis
# Grab the top face and cut a hole through everything from the center of it
plug = plug.faces(">Z").circle(hole_diameter/2).cutThruAll()
# Slight chamfer on all top edges
plug = plug.edges(">Z").chamfer(0.5)
# Slightly larger chamfer on the bottom edges
plug = plug.edges("<Z").chamfer(1)

cq.exporters.export(plug, 'output/plug_2x1_alum.stl')
cq.exporters.export(plug, 'output/plug_2x1_alum.step')