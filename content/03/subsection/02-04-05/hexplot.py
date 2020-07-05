import matplotlib.pyplot as plt
import numpy as np

def get_hexbin_attributes(hexbin):
    paths = hexbin.get_paths()
    points_codes = list(paths[0].iter_segments())#path[0].iter_segments() is a generator 
    prototypical_hexagon = [item[0] for item in points_codes]
    return prototypical_hexagon, hexbin.get_offsets(), hexbin.get_facecolors(), hexbin.get_array()



def pl_cell_color(mpl_facecolors):
    return [ f'rgb({int(R*255)}, {int(G*255)}, {int(B*255)})' for (R, G, B, A) in mpl_facecolors]



def make_hexagon(prototypical_hex, offset, fillcolor, linecolor=None):
    new_hex_vertices = [vertex + offset for vertex in prototypical_hex]
    vertices = np.asarray(new_hex_vertices[:-1])
    # hexagon center
    center=np.mean(vertices, axis=0)
    if linecolor is None:
        linecolor = fillcolor
    #define the SVG-type path:    
    path = 'M '
    for vert in new_hex_vertices:
        path +=  f'{vert[0]}, {vert[1]} L' 
    return  dict(type='path',
                 line=dict(color=linecolor, 
                           width=0.5),
                 path=  path[:-2],
                 fillcolor=fillcolor, 
                ), center 


def mpl_to_plotly(cmap, N):
    h = 1.0/(N-1)
    pl_colorscale = []
    for k in range(N):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([round(k*h,2), f'rgb({C[0]}, {C[1]}, {C[2]})'])
    return pl_colorscale