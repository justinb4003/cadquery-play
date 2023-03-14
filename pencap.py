import cadquery as cq

cap_od = 14.5
wider_cut_od = 12.28
inner_cut_od = 11
wider_cut_h = 8
inner_cut_h = 49
overall_h = 60

cap = (
    cq.Workplane("XY")
    .circle(cap_od/2)
    .extrude(overall_h)
)

captop = cap.faces(">Z").workplane(invert=True)

widecut = (
    captop.circle(wider_cut_od/2).extrude(wider_cut_h, combine=False)
)

innercut = (
    captop.circle(inner_cut_od/2).extrude(inner_cut_h, combine=False)
)

cap = cap.cut(widecut).cut(innercut)

cap = cap.faces(">Z").chamfer(0.5)

cq.exporters.export(cap, 'output/510cap.stl')
