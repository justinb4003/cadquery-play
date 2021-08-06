import cadquery as cq

marker_count = 2

md_min = 17.0
md_max = 23.0
mspacing = 1.2
block_height = 80.0
block_width = (md_max*(marker_count+1)*mspacing)
block_depth = md_max*1.4

block = (
    cq.Workplane("XY")
      .rect(block_width, block_depth)
      .extrude(block_height)
)

slots = []
for i in range(marker_count):
    testing = False
    peg = (
        block.faces(">Z")
            .workplane(invert=not testing)
            .center(-block_width/2, 0)  # slam pointer to far side of block 
            .center((i+1)*md_max*mspacing, 0)
            .circle(md_max/2)
            .extrude(block_height*0.9, combine=False)
    )
    
    taper = (
        block.faces(">Z")
            .workplane(offset=block_height*.9, invert=not testing)
            .center(-block_width/2, 0)  # slam pointer to far side of block 
            .center((i+1)*md_max*mspacing, 0)
            .circle(md_max/2)
            .workplane(offset=block_height*.1)
            .circle(md_min/2)
            .loft(combine=False)
    )
    slot = peg.union(taper)
    print('chop chop')
    slots.append(slot)
for s in slots:
    if testing:
        block = block.union(s)
    else:
        block = block.cut(s)
block = block.edges("|Z").fillet(12.0)
block = block.edges(">Z").fillet(2.0)

cq.exporters.export(block, 'marker_rack.stl')
