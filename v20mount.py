import cadquery as cq

# Set some basic dimensions up
base_l = 58
base_w = 66
base_d = 10

# Create the first block of our object, this will be the piece that sits against
# the shelf we've screwed it to.
holder = (
    cq.Workplane("XY")
      .rect(base_l, base_w)
      .extrude(base_d)
)

# Next we create a neck or post for the final lip to sit on. This is where the
# tool slides into the holder.
post_l = base_l
post_w = 41
post_d = 7
holder = (
    holder.faces(">Z")  # Grab the top face of the block we created above and build from it.
    .rect(post_l, post_w)
    .extrude(post_d)
)

# Finally we create a lip on top of the stack that's mostly a rectangle with a
# trapezoid on top of it making a bit of a wedge to self-center the tool as you
# insert it.
lip_l = base_l
lip_w = 53
lip_extension = 14
lip_offset = 5
lip = (
    holder.faces(">Z")
    .workplane()
    .center(lip_l/2 - lip_extension, lip_w/2) # Top right corner
    .line(lip_extension, -lip_offset)
    .line(0, -(lip_w-(lip_offset*2)))
    .line(-lip_extension, -lip_offset)
    .line(-(lip_l-lip_extension), 0)
    .line(0, lip_w)
    .close()
    .extrude(5.2, combine=False)
)

# Next fillet the edges where needed; We don't want to do the front or back of
# the lip as that creates some weird interference points with the rest of the
# holder.
lip = lip.edges("not (<X or >X)").fillet(2)

holder = holder.union(lip)

# Finally put some holes in for mounting screws
holder = (
    holder.faces(">Z")
    .rect(base_l / 1.8, 0, forConstruction=True).vertices().cboreHole(5, 10, 3)
)

# Create an STL for 3d printing
cq.exporters.export(holder, 'output/v20mount.stl')
# Create a STEP file for use in other CAD packages
cq.exporters.export(holder, 'output/v20mount.step')