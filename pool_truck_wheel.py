import cadquery as cq

wheel_height = 4

wheel = cq.Workplane("XY")
wheel_id = 128
wheel_od = wheel_id + 4

spokes = 4
spoke_width = 6
spoke_length = wheel_od + 25*2
deg_per_spoke = 360 / spokes;


for i in range(spokes):
    print(i)
    spoke = (
        cq.Workplane("XY")
            .rect(spoke_width, spoke_length)
            .extrude(wheel_height)
            .edges("|Z").fillet((spoke_width/2)*0.9)
            .rotate((0, 0, 0), (0, 0, 1), i*deg_per_spoke)
    )
    wheel = wheel.union(spoke)

hub = (
    cq.Workplane("XY")
        .circle(wheel_od/2).extrude(wheel_height)
)

wheel = wheel.union(hub)

wheel = (
    wheel.faces(">Z")
         .circle(wheel_id/2).cutThruAll()

)

cq.exporters.export(wheel, 'output/pool_truck_wheel.stl')