import json
from pyproj import Transformer
with open(r"C:\\Users\\Asus\\OneDrive\\du03\\du03_vaclavtham\\adresy.geojson", "r", encoding= "utf-8") as infile,\
    open ("output.geojson", "w") as outfile:
    data = json.load(infile)
    print("Type:", type(data))
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    jtsk2wgs = Transformer.from_crs(5514, 4326, always_xy=True)
    polohy = data['features']
    print("Type:", type(data))
    for coordinate_values in polohy:
        geometrie = coordinate_values["geometry"]
        from_x,from_y = geometrie["coordinates"]
        to_x, to_y= wgs2jtsk.transform(from_x, from_y)
        geometrie['coordinates_jtsk'] = to_x, to_y
        json_objekt = json.dumps(coordinate_values)
        outfile.write(json_objekt)