import cadquery as cq

# Set some basic dimensions up
base_l = 58 + 13
base_w = 66
base_d = 10

# Create the first block of our object, this will be the piece that sits against
# the shelf we've screwed it to.
holder = (
    cq.Workplane("XY")  # Create a workplane on the X and Y axis of a 3d space
      .rect(base_l, base_w) # Create a rectangle centered on 0,0 of the workplane
      .extrude(base_d)  # Extrude it up, or extend it this far
)

# Next we create a neck or post for the final lip to sit on. This is where the
# tool slides into the holder.
post_l = base_l
post_w = 41
post_d = 6
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
lip = lip.edges(">Z").edges("not <X").fillet(2)

# Merge the lip we just made with the square bases we built
holder = holder.union(lip)

# Finally put some holes in for mounting screws Creating a rectangle with
# 'forConstruction=True' and grabbing the verticies lets you make something
# happen at each point in the rect. In thise case we have a rectangle with 0 on
# one dimension so it is really only two points and we use them to "drill holes"
# in our object for mounting screws.
holder = (
    holder.faces(">Z")
    .rect((base_l / 1.8) - 13, 0, forConstruction=True).vertices().cboreHole(5, 10, 3)
)


bpost_oc = 9.00
bpost_d = 14
bpost_w = 3.5

blade_slots = []
for slot_x in [-bpost_oc*0.5, -bpost_oc*1.5, bpost_oc*0.5, bpost_oc*1.5]:
    blade_slots.append(
        holder.faces(">X")
        .workplane(centerOption="CenterOfBoundBox")
        .center(slot_x, 4.75)
        .rect(bpost_w, bpost_d).extrude(-bpost_d, combine=False)
    )

for b in blade_slots:
    holder = holder.cut(b)


# Create an STL for 3d printing
cq.exporters.export(holder, 'output/v20mount.stl')
# Create a STEP file for use in other CAD packages
cq.exporters.export(holder, 'output/v20mount.step')