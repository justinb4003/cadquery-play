import cadquery as cq

top_hanger_id = 12.5
bottom_hanger_id = 30.0
thickness = 4.0
width = 8
drop_height = 25 

def make_half_circle(wp, r):
  hc = (
    wp.lineTo(-r, 0)
      .threePointArc((0, r), (r, 0))
      .close()
  )
  return hc


top_cut = make_half_circle(cq.Workplane("XY"), top_hanger_id/2).extrude(width)
top_hanger = make_half_circle(cq.Workplane("XY"), top_hanger_id/2+(thickness)).extrude(width)
hook = top_hanger.cut(top_cut)
hook = (
  hook.faces("<Y")
  .workplane(centerOption="CenterOfBoundBox")
  .center(top_hanger_id/2+thickness/2, 0)
  .rect(thickness, width)
  .extrude(5)
  .center(-(top_hanger_id+thickness), 0)
  .rect(thickness, width)
  .extrude(drop_height)
)

d = 30
bottom_hanger = make_half_circle(cq.Workplane("XY").center(4.75, -drop_height), 
                                 -(d/2)).extrude(width)

bottom_cut = make_half_circle(cq.Workplane("XY").center(4.75, -drop_height), 
                              -(d/2-thickness)).extrude(width)

bottom_hanger = bottom_hanger.cut(bottom_cut)
hook = hook.union(bottom_hanger)
hook = hook.edges("|Z").fillet(1.5)

cq.exporters.export(hook, 'output/light_hook.stl')