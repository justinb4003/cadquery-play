# Whiteboard marker holder intended to sit on the sill of a whiteboard.
import cadquery as cq
from math import floor

marker_rows = 1
mmpr = 7  # max markers per row, gets used alot, so it's a short name

md_min = 17.0
md_max = 23.0
md_pad = 4.5
md_full = md_max+md_pad
block_height = 72.0
block_width = md_full*(mmpr+0.5)
block_depth = (md_max*1.4)*marker_rows + 16
# Sill is about 62cm wide, so make sure I keep it under that.
print(block_depth, block_width)

block = (
    cq.Workplane("XY")
      .rect(block_width, block_depth)
      .extrude(block_height)
)

block = block.edges("|Z").fillet(16.0)

base_padding = 4.0
base_height = 12.0
base_pocket = 8.0
base = (
    cq.Workplane("XY")
      .workplane(offset=base_pocket-base_height)
      .rect(block_width+base_padding*2, block_depth+base_padding*2)
      .extrude(base_height)
)
base = base.edges("|Z").fillet(12.0)
base = base.edges(">Z").fillet(4.0)

base = base.cut(block)


(slots, x, y) = ([], 0, 0)
for r in range(1, marker_rows+1):
    marker_count = mmpr-1 if r % 2 == 0 else mmpr
    
    for i in range(marker_count):
        testing = False 
        
        xoffset = md_full/4
        if marker_count == mmpr:
            xoffset *= -1
        newx = (i+1)*(md_full) + xoffset

        if r == 1 and marker_rows != 1:
            newy = -md_full
        elif r==2 or marker_rows == 1:
            newy = 0
        elif r==3:
            newy = md_full
        else:
            print('what?!')
        deltax = newx - x
        x = newx 
        y = newy
        # print(f'{x}x{y}, {deltax}')
        peg = (
            block.faces(">Z")
                .workplane(invert=not testing)
                .center(-block_width/2, 0)  # slam pointer to far side of block 
                .center(x, y)
                .circle(md_max/2)
                .extrude(block_height*0.9, combine=False)
        )
        
        taper = (
            block.faces(">Z")
                .workplane(offset=block_height*.9, invert=not testing)
                .center(-block_width/2, 0)  # slam pointer to far side of block 
                .center(x, y)
                .circle(md_max/2)
                .workplane(offset=block_height*.1)
                .circle(md_min/2)
                .loft(combine=False)
        )
        slot = peg.union(taper)
        slots.append(slot)
    for s in slots:
        if testing:
            block = block.union(s)
        else:
            block = block.cut(s)
block = block.edges(">Z").fillet(2.125)

cq.exporters.export(block, 'output/marker_wb.stl')
