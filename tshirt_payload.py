from distutils.util import convert_path
import cadquery as cq

def build_cone(max_width, cone_height, base_height):
    spts = [
        (-max_width/2, 0),
        (-max_width/2, cone_height/3),
        (0, cone_height),
    ]

    cone = (
        cq.Workplane("YZ")
        .lineTo(spts[0][0], spts[0][1]).spline(spts).close()
        .revolve(360)
    )
    cone = (
        cone
        .faces("<Z")
        .workplane(centerOption='CenterOfBoundBox')
        .circle(max_width/2)
        .extrude(base_height)
    )
    return cone


pipe_id = 2.047*25.4

base_h = 30
cone_h = 40
shell = build_cone(pipe_id - 4, cone_h, base_h)
payload = build_cone(pipe_id - 10, 35, base_h)
shell = shell.cut(payload)
shell = shell.faces("<Z").chamfer(0.75)
shell = shell.translate((0, 0, base_h))

fins = (
    cq.Workplane("XY")
        .polygon(8, pipe_id-4, forConstruction=True)
        .vertices()
        .circle(2).twistExtrude(cone_h+base_h, -50)
)

shell = shell.cut(fins)
cq.exporters.export(shell, 'output/tshirt_payload.stl')