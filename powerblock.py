import cadquery as cq

#parameter definitions

board_width = 128.0
board_height = 47.0
hole_id = 3.25
hole_offset = 5.5

corner_radius = 3.0

shell_thickness = 4.0
shell_height = 16.0
# Post is built from the "top" of the shell floor so it starts shell_thickness
# up in the air. 
# shell_height - (post_height + shell_thickness) = the room left for the board
# to sit in.  Leaving 2mm should let it nestle is nicely.
post_height = 10.0 

atx_port_width = 53.0

#outer shell
oshell = (cq.Workplane("XY")
            .rect(board_width+shell_thickness, board_height + shell_thickness)
            .extrude(shell_height)
)

oshell = oshell.edges("|Z").fillet(corner_radius)

#inner shell
ishell = (
    oshell.faces("<Z")
          .workplane(shell_thickness, True)
          .rect(board_width+0.5, board_height+0.5)
          .extrude(shell_height - shell_thickness, False)
)

# Make a 1mm deep "notch" on one side to let the ATX power cable fit.
power_hole = (
    oshell.faces(">Z")
          .workplane(-1, False)
          .center(0, (board_height+shell_thickness)/2)
          .rect(53.0, shell_thickness)
          .extrude(1, False)
)

# cut the inner box from the outer one
box = oshell.cut(ishell)
# now cut out the power hole
box = box.cut(power_hole)

#make the posts to hold up the board
box = (
    box.faces("<Z")
       .workplane(shell_thickness, True)
       .rect(board_width-hole_offset,
             board_height-hole_offset,
             forConstruction=True)
       .vertices()
       .circle(4)
       .extrude(post_height)
)

# Some more posts spaced a little closer
box = (
    box.faces("<Z")
       .workplane(shell_thickness, True)
       .rect(board_width/2.0,
             board_height-hole_offset,
             forConstruction=True)
       .vertices()
       .circle(4)
       .extrude(post_height)
)

# And now two posts right in the middle; technically we make 4 but they sit
# directly on top of each other
box = (
    box.faces("<Z")
       .workplane(shell_thickness, True)
       .rect(0,
             board_height-hole_offset,
             forConstruction=True)
       .vertices()
       .circle(4)
       .extrude(post_height)
)

#make the pegs for the board to sit on 
peg_width = board_width-hole_offset-1.0  # The extra constant is a fudge
peg_height = board_height-hole_offset
print(f'Pegs are {peg_width}x{peg_height}')
box = (
    box.faces("<Z")
       .workplane(shell_thickness, True)
       .rect(peg_width, peg_height, forConstruction=True)
       .vertices()
       .circle((hole_id-0.25)/2.0)
       .extrude(post_height + 8)
)


cq.exporters.export(box, 'powerbox.stl')
