import cadquery as cq

marker_count = 2

md_min = 12.0
md_max = 20.0
block_height = 80.0
block_width = md_max*(marker_count+1)
block_depth = md_max*1.4


center_points = []
for i in range(marker_count):
    center_points.append((i*md_max, 0.0))


block = (
    cq.Workplane("XY")
      .rect(block_width, block_depth)
      .extrude(block_height)
)

slots = (
    block.faces(">Z")
         .workplane(invert=True)
         .pushPoints(center_points)
         .circle(md_max/2)
         .workplane(offset=block_height)
         .circle(md_min/2)
         .loft(combine=False)
)

block = block.cut(slots)
block = block.edges("|Z").fillet(12.0)
block = block.edges(">Z").fillet(2.0)

cq.exporters.export(block, 'marker_rack.stl')
