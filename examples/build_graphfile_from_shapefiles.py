import pyvisgraph as vg
import shapefile

# In this example a visibility graph will be created from the GSHHS shorelines
# available at: https://www.ngdc.noaa.gov/mgg/shorelines/gshhs.html
# 1. Download the shorelines as shape files and select the wanted resolution 
#    and level (in this example we use Crude, L1). 
# 2. Copy all the related files (shx, shp, prj, dbf) to the folder that contains
#    this script.

input_shapefile = shapefile.Reader('GSHHS_c_L1')
output_graphfile = 'GSHHS_c_L1.graph'
# Number of CPU cores on host computer. If you don't know how many cores you
# have, use 'cat /proc/cpuinfo | grep processor | wc -l' on Linux. On Windows,
# press Ctrl + Shift + Esc, press Performance tab. Look for 'logical processors'.
workers = 4 

# Get the shoreline shapes from the shape file. Broadly speaking the GSHHS
# shapes correspond to the shorelines of continents, countries and islands.
shapes = input_shapefile.shapes()
print('The shapefile contains {} shapes.'.format(len(shapes)))

# Create a list of polygons, where each polygon corresponds to a shape
polygons = []
for shape in shapes:
    polygon = []
    for point in shape.points:
        polygon.append(vg.Point(point[0], point[1]))
    polygons.append(polygon)

# Start building the visibility graph 
graph = vg.VisGraph()
print('Starting building visibility graph')
graph.build(polygons, workers=workers)
print('Finished building visibility graph')

# Save the visibility graph to a file 
graph.save(output_graphfile)
print('Saved visibility graph to file: {}'.format(output_graphfile))
