import cadquery as cq

mask = cq.importers.importDXF('mask.dxf').wires()

cq.exporters.export(mask, 'tbfilter.stl')