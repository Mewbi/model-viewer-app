import pymesh

import numpy as np

import perimetry

brenda = pymesh.load_mesh("models/brenda_peq_bw.obj")

xv, yv, zv = np.array_split(brenda.vertices, 3, axis = 1)

x_range = (min(xv)[0], max(xv)[0])
y_range = (min(yv)[0], max(yv)[0])
z_range = (min(zv)[0], max(zv)[0])

y_height = (y_range[0]+y_range[1])/2

box_min = np.array([x_range[0], y_height-0.1, z_range[0]])
box_max = np.array([x_range[1], y_height, z_range[1]])

box_mesh = pymesh.generate_box_mesh(box_min, box_max)
pymesh.save_mesh("models/box_mesh.obj", box_mesh)

mesh = pymesh.boolean(brenda, box_mesh, operation="intersection", engine="igl")

#pymesh.save_mesh('models/intersection.obj', mesh)

print "Perimetro: {}".format(perimetry.calc_perimeter(mesh.vertices))

# brenda = pymesh.load_mesh('models/brenda_peq_bw.obj')
