import pyvisgraph as vg
import folium

# In this example we will calculate the shortest path between two points
# and plot this on a interactive map, using the folium package.

# Example points
start_point = vg.Point(12.568337, 55.676098) # Copenhagen
end_point = vg.Point(103.851959, 1.290270) # Singapore

# Load the visibility graph file If you do not have this, please run
# 1_build_graph_from_shapefiles.py first.
graph = vg.VisGraph()
graph.load('GSHHS_c_L1.graph')

# Calculate the shortest path
shortest_path  = graph.shortest_path(start_point, end_point)

# Plot of the path using folium
geopath = [[point.y, point.x] for point in shortest_path]
geomap  = folium.Map([0, 0], zoom_start=2)
for point in geopath:
    folium.Marker(point, popup=str(point)).add_to(geomap)
folium.PolyLine(geopath).add_to(geomap)

# Add a Mark on the start and positions in a different color
folium.Marker(geopath[0], popup=str(start_point), icon=folium.Icon(color='red')).add_to(geomap)
folium.Marker(geopath[-1], popup=str(end_point), icon=folium.Icon(color='red')).add_to(geomap)

# Save the interactive plot as a map
output_name = 'example_shortest_path_plot.html'
geomap.save(output_name)
print('Output saved to: {}'.format(output_name))
