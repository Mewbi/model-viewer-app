import numpy as np
from math import atan2, sqrt

def medir_per(mesh):
	x,y,z = np.array_split(mesh,3,axis = 1) #split mesh into x, y, z
	#x,z = zip(*mesh)
	perim_x = sum(x)/len(x)
	perim_z = sum(z)/len(z)

	slice = np.concatenate((x,z), axis = 1)
	theta = [atan2(i[1]-perim_z, i[0]-perim_x) for i in slice]

	xztheta = np.column_stack((slice, theta))

	xztheta = xztheta[xztheta[:, -1].argsort()][::-1]

	perims = xztheta[0:3]

	print "perims: {}".format(len(perims))
	j = 0
	for i in xztheta[3:]:
		while not orientation(perims[-2], perims[-1], i):
			if len(perims) < 3:
				print ">>orientation>> BREAK perims: {}".format(len(perims))
				break;
			perims = np.delete(perims, -1, 0)
			print ">>orientation>> {} just removed >> perims: {} / {}".format(j, len(perims), len(perims) < 2)
		perims = np.insert(perims, 0, [i], axis=0)
		j +=1
		print ">>for {} perims: {}".format(j, len(perims))


	dist = np.sqrt(np.sum(np.diff(perims, axis=0)**2, axis=1)) # distancia entre puntos

	a = perims[-1][0] - perims[0][0]
	b = perims[-1][1] - perims[0][1]

	dist_ = sqrt(pow(a, 2) + pow(b, 2))

	return np.sum(dist) + dist_


def orientation(p, q, r):
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


	print ">>>>>>>>>>>> orientation >>> val: {}".format(val)

	if val >= 0:
		return False
	else:
		return True 


# xztheta_o = np.argsort(xztheta[:-1])
# xztheta_o = [xztheta_o[i] for i in xztheta]
# or
# xzt[xzt[:, -1].argsort()]


