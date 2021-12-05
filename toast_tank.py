import cadquery as cq

drive_train_height = 100
drive_train_width = 300
drive_train_length = 450

wheel_axel_offset_from_center = drive_train_length/2 - 100

panel_width = 5

def build_drive_train():

    left_panel = (
        cq.Workplane("XZ")
        .workplane(offset=-drive_train_width/2)
        .rect(drive_train_length, drive_train_height)
        .extrude(panel_width)
    )

    right_panel = (
        cq.Workplane("XZ")
        .workplane(offset=drive_train_width/2)
        .rect(drive_train_length, drive_train_height)
        .extrude(panel_width)
    )

    left_panel = (
        left_panel.faces("<Y")
            .pushPoints([(-wheel_axel_offset_from_center, 0), (wheel_axel_offset_from_center, 0)])
            .polygon(6, 12).cutThruAll()
    )
    
    right_panel = (
        right_panel.faces(">Y")
            .pushPoints([(-wheel_axel_offset_from_center, 0), (wheel_axel_offset_from_center, 0)])
            .polygon(6, 12).cutThruAll()
    )
        
    front_panel = (
        cq.Workplane("YZ")
        .workplane(offset=drive_train_length/2)
        .rect(drive_train_width, drive_train_height)
        .extrude(panel_width)
    )

    rear_panel = (
        cq.Workplane("YZ")
        .workplane(offset=-drive_train_length/2)
        .rect(drive_train_width, drive_train_height)
        .extrude(panel_width)
    )

    dt = left_panel.union(right_panel)
    dt = dt.union(front_panel)
    dt = dt.union(rear_panel)
    return dt


body = build_drive_train()

cq.exporters.export(body, 'output/toast_tank.stl')