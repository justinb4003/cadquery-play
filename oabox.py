import cadquery as cq

height = 40.0
width = 95.0
depth = 75.0

# make the base
result = (
    cq.Workplane('XY')
    .box(width, depth, height)
    .faces('+Z')
    .shell(4)
    # .edges('|X').fillet(4.0)
)

# Render the solid
cq.exporters.export(result, 'result.stl')

