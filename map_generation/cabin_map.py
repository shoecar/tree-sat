# "borrowed" from https://stackoverflow.com/a/54164812/6465651

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from gmplot import GoogleMapPlotter

class CustomGoogleMapPlotter(GoogleMapPlotter):
    G_MAP_TYPES = ['roadmap', 'satellite', 'hybrid', 'terrain']
    DEFAULT_MAP_TYPE = 'roadmap'
    RANDOM_TO_COLOR_SCALAR = 20

    def __init__(self, focus_lat, focus_lng, zoom, apikey='', map_type='satellite'):
        if apikey == '':
            try:
                with open('apikey.txt', 'r') as apifile:
                    apikey = apifile.readline()
            except FileNotFoundError:
                pass
        super().__init__(focus_lat, focus_lng, zoom, apikey)

        self.map_type = map_type
        assert(self.map_type in self.G_MAP_TYPES)

    def color_scatter(self, tree_coordinates, colors=None, colormap='coolwarm',
                      size=None, marker=False, s=None, **kwargs):
        def rgb2hex(rgb):
            """ Convert RGBA or RGB to #RRGGBB """
            rgb = list(rgb[0:3]) # remove alpha if present
            rgb = [int(c * 255) for c in rgb]
            hexcolor = '#%02x%02x%02x' % tuple(rgb)
            return hexcolor

        if colors is None:
            color_values = list(range(len(tree_coordinates)))
            cmap = plt.get_cmap(colormap)
            norm = Normalize(vmin=min(color_values), vmax=max(color_values))
            scalar_map = ScalarMappable(norm=norm, cmap=cmap)
            colors = [rgb2hex(scalar_map.to_rgba(value)) for value in color_values]

        for coord, color in zip(tree_coordinates, colors):
            lat, lng = coord
            self.scatter(lats=[lat], lngs=[lng], c=color, size=size, marker=marker,
                         s=s, **kwargs)

def generate_html(map_type='roadmap'):
    initial_zoom = 19
    focus_lat = 45.06361149480215
    focus_lng = -92.87854103763274

    if map_type not in CustomGoogleMapPlotter.G_MAP_TYPES:
        map_type = CustomGoogleMapPlotter.DEFAULT_MAP_TYPE

    gmap = CustomGoogleMapPlotter(focus_lat, focus_lng, initial_zoom, map_type=map_type)

    tree_coordinates = [(45.0636269034886, -92.87760837466844), (45.06342513381125, -92.8782675678164), (45.0636269034886, -92.877), (45.06342513381125, -92.8788)]

    gmap.color_scatter(tree_coordinates, size=3)
    gmap.color_scatter([(focus_lat, focus_lng)], marker=True)

    return gmap.get()
