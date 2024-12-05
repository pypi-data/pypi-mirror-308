import dataclasses as _dc

import numpy as _np




@_dc.dataclass
class Refrigerant:
	"""
	Properties of refrigerants
	`S:` Saturated
	`T:` Saturation temperature (K)
	`P:` Saturation pressure (kPa)
	`vf, vg:` specific volume (m3/kg)
	`hf, hg:` enthalpy (kJ/kg)
	`sf, sg:` entropy (kJ/kgK)
	"""
	@_dc.dataclass
	class SR12:
		"""Dichlorodifluoromethane"""
		T = _np.array([183.15, 188.15, 193.15, 198.15, 203.15, 208.15, 213.15, 218.15,
		223.15, 228.15, 233.15, 238.15, 243.15, 248.15, 253.15, 258.15,
		263.15, 268.15, 273.15, 278.15, 283.15, 288.15, 293.15, 298.15,
		303.15, 308.15, 313.15, 318.15, 323.15, 328.15, 333.15, 338.15,
		343.15, 348.15, 353.15, 358.15, 363.15, 368.15, 373.15, 378.15,
		383.15, 385.15])
		
		P = _np.array([2.8, 4.2, 6.2, 8.8, 12.3, 16.8, 22.6, 30, 39.1, 50.4, 
		64.2, 80.7, 100.4, 123.7, 150.9, 182.6, 219.1, 261, 308.6, 362.6, 
		423.3, 419.4, 567.3, 651.6, 744.9, 847.7, 960.7, 1084.3, 
		1219.3, 1366.3, 1525.9, 1698.8, 1885.8, 2087.4, 2304.6, 2538, 2788.5, 
		3056.9, 3344, 3650.9, 3978.4, 4115.5])
		
		vf = _np.array([0.000608, 0.000612, 0.000617, 0.000622, 0.000627, 0.000632, 0.000637, 
		0.000642, 0.000648, 0.000654, 0.000659, 0.000666, 0.000672, 0.000679, 0.000685, 
		0.000693, 0.0007, 0.000708, 0.000716, 0.000724, 0.000733, 0.000743, 0.000752, 
		0.000763, 0.000774, 0.000786, 0.000798, 0.000811, 0.000826, 0.000841, 
		0.000858, 0.000877, 0.000897, 0.00092, 0.000946, 0.000976, 0.001012, 0.001056, 
		0.001113, 0.001197, 0.001364, 0.001792])
		
		vg = _np.array([4.415545, 3.037316, 2.138345, 1.537651, 1.12728, 0.841166, 0.63791, 
		0.491, 0.383105, 0.302682, 0.24191, 0.195398, 0.159375, 0.131166, 0.108847, 0.091018, 
		0.076646, 0.064963, 0.055389, 0.047485, 0.040914, 0.035413, 0.03078, 0.026854, 
		0.023508, 0.020641, 0.018171, 0.016032, 0.01417, 0.012542, 0.011111, 0.009847, 
		0.008725, 0.007723, 0.006821, 0.006005, 0.005258, 0.004563, 0.003903, 
		0.003242, 0.002462, 0.001797])
		
		hf =_np.array([-43.243, -38.968, -34.688, -30.401, -26.103, -21.793, -17.469, -13.129, 
		-8.772, -4.396, 0, 4.416, 8.854, 13.315, 17.8, 22.312, 26.851, 31.42, 36.022, 40.659, 
		45.337, 50.058, 54.828, 59.653, 64.539, 69.494, 74.527, 79.647, 84.868, 90.201, 
		95.665, 101.279, 107.067, 113.058, 119.291, 125.818, 132.708, 140.068, 148.076, 157.085, 
		168.059, 174.92])
		
		hg =_np.array([146.375, 148.64, 150.924, 153.224, 155.536, 157.857, 160.184, 162.512, 164.84, 
		167.163, 169.479, 171.784, 174.076, 176.352, 178.61, 180.846, 183.058, 185.243, 187.397, 
		189.518, 191.602, 193.644, 195.641, 197.586, 199.475, 201.299, 203.051, 204.722, 
		206.298, 207.776, 209.109, 210.303, 211.321, 212.126, 212.665, 212.865, 212.614, 211.726, 
		209.843, 206.099, 196.484, 175.071])
		
		sf = _np.array([-0.2084, -0.1854, -0.163, -0.1411, -0.1197, -0.0987, -0.0782, -0.0581, 
		-0.0384, -0.019, 0, 0.0187, 0.0371, 0.0552, 0.073, 0.0906, 0.1079, 0.125, 0.1418, 0.1585, 
		0.175, 0.1914, 0.2076, 0.2237, 0.2397, 0.2557, 0.2716, 0.2875, 0.3034, 0.3194, 0.3355, 
		0.3518, 0.3683, 0.3851, 0.4023, 0.4201, 0.4385, 0.4579, 0.4788, 0.5023, 0.5322, 0.5651])
		
		sg =_np.array([0.8268, 0.8116, 0.7979, 0.7855, 0.7744, 0.7643, 0.7552, 0.747, 0.7396, 0.7329, 
		0.7269, 0.7214, 0.7165, 0.7121, 0.7082, 0.7046, 0.7014, 0.6986, 0.696, 0.6937, 0.6916, 
		0.6897, 0.6879, 0.6863, 0.6848, 0.6834, 0.682, 0.6806, 0.6792, 0.6777, 0.676, 0.6742, 
		0.6721, 0.6697, 0.6667, 0.6631, 0.6585, 0.6526, 0.6444, 0.6319, 0.6064, 0.5655])

	

	@_dc.dataclass
	class SR22:
		"""Chlorodifluoromethane"""
		T = _np.array([173.15, 183.15, 193.15, 203.15, 213.15, 218.15, 223.15, 233.15, 238.15, 
		243.15, 248.15, 253.15, 258.15, 263.15, 268.15, 273.15, 278.15, 283.15, 288.15, 293.15, 
		298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15, 333.15, 338.15, 343.15, 348.15, 
		353.15, 358.15, 363.15, 368.15])
		
		P = _np.array([2, 4.8, 10.4, 20.5, 37.5, 49.6, 64.5, 105.2, 132, 163.9, 201.4, 245.3, 296.2, 
		354.2, 421.2, 498, 583.6, 680.5, 789, 909.7, 1043.7, 1191.7, 1354.6, 1533.3, 1728.8, 1942, 
		2174.2, 2426.3, 2699.6, 2995.6, 3315.7, 3661.9, 4036.4, 4442.1, 4882])
		
		vf = _np.array([0.0006, 0.0007, 0.0007, 0.0007, 0.0007, 0.0007, 0.0007, 0.000709, 0.000717, 
		0.000725, 0.000733, 0.000741, 0.0008, 0.0008, 0.000768, 0.000778, 0.000789, 0.0008, 0.000812,
		0.000824, 0.000838, 0.000852, 0.000867, 0.000884, 0.000902, 0.000922, 0.000944, 0.000969, 
		0.000997, 0.00103, 0.001069, 0.001118, 0.001183, 0.001282, 0.0015])
		
		vg = _np.array([8.266, 3.645, 1.778, 0.9434, 0.5368, 0.4142, 0.3238, 0.2052, 0.166474, 
		0.135901, 0.111904, 0.092879, 0.077654, 0.065363, 0.055358, 0.04715, 0.040368, 0.034724, 
		0.029996, 0.02601, 0.02263, 0.019747, 0.017273, 0.015139, 0.013287, 0.011672, 0.010254, 
		0.009002, 0.007889, 0.00689, 0.005984, 0.005149, 0.004359, 0.003564, 0.0026]) 
		
		hf = _np.array([90.7, 101.3, 111.9, 122.6, 133.3, 138.6, 144, 154.9, 160.7, 165.9, 171.5, 
		177.1, 182.7, 188.4, 194.2, 200, 205.9, 211.9, 218, 224.1, 230.4, 236.8, 243.2, 249.8, 
		256.5, 263.4, 270.5, 277.8, 285.4, 293.3, 301.7, 310.8, 320.9, 333, 349.6])
		
		hg = _np.array([359, 363.9, 368.8, 373.7, 378.6, 381, 383.4, 388.1, 390.4, 392.7, 394.9, 
		397.1, 399.2, 401.2, 403.2, 405, 406.8, 408.6, 410.2, 411.7, 413, 414.3, 415.3, 416.2, 417, 
		417.4, 417.7, 417.5, 417.1, 416.1, 414.5, 412, 408.2, 401.9, 387.3])
		
		sf = _np.array([0.505, 0.565, 0.621, 0.675, 0.726, 0.751, 0.775, 0.823, 0.847, 0.869, 0.892, 
		0.914, 0.935, 0.957, 0.979, 1, 1.021, 1.042, 1.063, 0.084, 0.105, 1.126, 1.146, 1.167, 
		1.188, 1.209, 1.23, 1.251, 1.273, 1.295, 1.319, 1.343, 1.371, 1.403, 1.446]), 
		
		sg = _np.array([2.054, 1.998, 1.951, 1.911, 1.877, 1.862, 1.848, 1.823, 1.814, 1.803, 1.793, 
		1.784, 1.775, 1.767, 1.759, 1.752, 1.745, 1.738, 1.731, 1.725, 1.719, 1.712, 1.706, 1.7, 1.694, 
		1.687, 1.68, 1.673, 1.665, 1.656, 1.646, 1.634, 1.618, 1.596, 1.549])
	

	@_dc.dataclass
	class SR23:
		"""Trifluoromethane (Fluoroform)"""
		T = _np.array([123.15, 129.15, 138.15, 142.15, 146.15, 150.15, 154.15, 158.15, 162.15, 166.15, 
		170.15, 174.15, 178.15, 182.15, 186.15, 190.15, 194.15, 198.15, 202.15, 206.15, 210.15, 214.15, 
		218.15, 222.15, 226.15, 230.15, 234.15, 238.15, 242.15, 246.15, 250.15, 254.15, 258.15, 262.15, 
		266.15, 270.15, 274.15, 278.15, 282.15, 286.15, 290.15, 294.15, 298.15]) 
		
		P = _np.array([0.133, 0.341, 1.155, 1.866, 2.919, 4.435, 6.565, 9.49, 13.427, 18.63, 25.392, 
		34.048, 44.975, 58.589, 75.351, 95.761, 120.357, 149.717, 184.447, 225.188, 272.604, 327.387, 
		390.245, 461.907, 543.118, 634.637, 737.244, 851.732, 978.925, 1119.672, 1274.866, 1445.452, 
		1632.442, 1836.94, 2060.156, 2303.444, 2568.325, 2856.535, 3170.062, 3511.203, 3882.626, 4287.443, 
		4729.293]) 
		
		vf = _np.array([0.00062, 0.00063, 0.00063, 0.00064, 0.00064, 0.00064, 0.00065, 0.00065, 
		0.00066, 0.00066, 0.00067, 0.00067, 0.00068, 0.00068, 0.00069, 0.00069, 0.0007, 0.00071, 
		0.00071, 0.00072, 0.00073, 0.00074, 0.00075, 0.00076, 0.00077, 0.00078, 0.00079, 
		0.0008, 0.00081, 0.00083, 0.00084, 0.00086, 0.00088, 0.0009, 0.00092, 0.00095, 0.00098, 
		0.00101, 0.00105, 0.0011, 0.00117, 0.00127, 0.00149])
		
		vg = _np.array([110.1256, 44.9332, 14.178, 9.0207, 5.9226, 3.9992, 2.7691, 1.9612, 1.4176, 
		1.0437, 0.7815, 0.5941, 0.458, 0.3576, 0.2825, 0.2256, 0.1819, 0.1481, 0.1216, 0.1006, 0.0838, 
		0.0704, 0.0594, 0.0505, 0.0431, 0.037, 0.0319, 0.0276, 0.0239, 0.0209, 0.0182, 0.016, 0.014, 
		0.0123, 0.0108, 0.0095, 0.0083, 0.0072, 0.0063, 0.0054, 0.0046, 0.0037, 0.0027]) 
		
		hf = _np.array([-6.5, 5.5, 21.2, 27.5, 33.4, 39, 44.3, 49.5, 54.4, 59.3, 64, 68.7, 73.3, 
		77.9, 82.6, 87.2, 91.9, 96.7, 101.5, 106.4, 111.4, 116.4, 121.5, 126.8, 132, 137.4, 142.8, 
		148.3, 153.9, 159.5, 165.2, 171, 176.9, 182.8, 188.9, 195.2, 201.7, 208.6, 216, 224.3, 233.8, 
		245.9, 265.4])
		
		hg = _np.array([294.9, 297.9, 302.4, 304.4, 306.4, 308.4, 310.4, 312.4, 314.3, 316.2, 318.1, 
		319.9, 321.7, 323.5, 325.2, 326.8, 328.4, 329.9, 331.3, 332.7, 334, 335.2, 336.3, 337.4, 
		338.4, 339.2, 340, 340.7, 341.3, 341.8, 342.2, 342.4, 342.4, 342.2, 341.9, 341.2, 340.2, 
		338.7, 336.6, 333.7, 329.3, 322.3, 306.1])
		
		sf = _np.array([0.1011, 0.0063, 0.1114, 0.1561, 0.1972, 0.2351, 0.2703, 0.3032, 0.3342, 
		0.3636, 0.3918, 0.4189, 0.4451, 0.4707, 0.4958, 0.5204, 0.5448, 0.5689, 0.5929, 0.6167, 
		0.6404, 0.664, 0.6876, 0.711, 0.7343, 0.7575, 0.7806, 0.8035, 0.8263, 0.8489, 0.8713, 
		0.8936, 0.9158, 0.938, 0.9603, 0.9828, 1.0059, 1.0298, 1.0552, 1.0829, 1.1146, 1.154, 1.218])
		
		sg = _np.array([2.3464, 2.2581, 2.1472, 2.1047, 2.0657, 2.0297, 1.9964, 1.9656, 1.9369, 1.9101, 
		1.8851, 1.8616, 1.8395, 1.8187, 1.799, 1.7804, 1.7627, 1.7458, 1.7298, 1.7144, 1.6997, 1.6857, 
		1.6722, 1.6592, 1.6466, 1.6345, 1.6228, 1.6114, 1.6002, 1.5893, 1.5785, 1.5678, 1.5571, 1.5462, 
		1.535, 1.5234, 1.511, 1.4976, 1.4826, 1.4652, 1.4437, 1.4141, 1.3545])

	
	@_dc.dataclass
	class SR32:
		"""Difluoromethane"""
		T = _np.array([136.34, 143.15, 153.15, 163.15, 173.15, 183.15, 193.15, 203.15, 213.15, 221.5, 
		223.15, 233.15, 237.15, 243.15, 249.15, 255.15, 261.15, 267.15, 273.15, 279.15, 285.15, 
		291.15, 297.15, 303.15, 309.15, 315.15, 321.15, 327.15, 333.15, 339.15, 348.15])
		
		P = _np.array([0.05, 0.13, 0.48, 1.45, 3.81, 8.87, 18.65, 36.07, 64.96, 101.33, 110.14, 
		177.41, 211.97, 273.44, 347.96, 437.28, 543.27, 667.86, 813.1, 981.13, 1174.2, 1394.6, 
		1644.8, 1927.5, 2245.4, 2601.4, 2998.9, 3441.5, 3933.2, 4479.3, 5416.8])
		
		vf = _np.array([0.00069964, 0.00070786, 0.00072025, 0.00073324, 0.00074682, 0.00076109, 
		0.00077615, 0.00079214, 0.00080925, 0.0008244, 0.0008275, 0.00084731, 0.00085572, 
		0.000868809, 0.00088269, 0.000897424, 0.000913075, 0.000929713, 0.000947597, 
		0.000966930, 0.000987947, 0.00101081, 0.00103605, 0.00106428, 0.00109601, 0.00113250, 0.00117536, 
		0.00122729, 0.00129315, 0.0013831, 0.00165043]), 
		
		vg = _np.array([0.00220337, 0.00573526, 0.0195373, 0.0558440, 0.13846, 0.305614, 0.612895, 
		1.13543, 1.96904, 2.98792, 3.23164, 5.06508, 5.99520, 7.63883, 9.62186, 11.9947, 14.8170, 
		18.1554, 22.0896, 26.7165, 32.133, 38.4911, 45.9770, 54.7645, 65.2315, 77.7000, 92.7643, 
		111.482, 135.135, 167.224, 255.754]) 
		
		hf = _np.array([-19.07, -8.26, 7.52, 23.2, 38.83, 54.42, 70.02, 85.66, 101.38, 114.59, 
		117.22, 133.23, 139.69, 149.45, 159.31, 169.28, 179.37, 189.6, 200, 210.58, 221.36, 232.39, 
		243.69, 255.32, 267.34, 279.84, 292.95, 306.87, 321.93, 338.78, 372.39]) 
		
		hg = _np.array([444.31, 448.77, 455.33, 461.86, 468.31, 474.61, 480.72, 486.57, 492.11, 496.45, 
		497.27, 502.02, 503.78, 506.27, 508.57, 510.64, 512.47, 514.03, 515.3, 516.24, 516.8, 516.95, 
		516.62, 515.72, 514.17, 511.82, 508.48, 503.86, 497.44, 488.26, 461.72])
		
		sf = _np.array([-0.105, -0.0276, 0.079, 0.1782, 0.2711, 0.3586, 0.4415, 0.5204, 0.5958, 0.6565, 
		0.6683, 0.7382, 0.7655, 0.806, 0.8458, 0.885, 0.9237, 0.962, 1, 1.0377, 1.0753, 1.1128, 1.1503, 
		1.1881, 1.2262, 1.265, 1.3048, 1.3461, 1.3898, 1.4377, 1.5314])
		
		sg = _np.array([3.2937, 3.1651, 3.003, 2.8668, 2.7515, 2.6529, 2.5679, 2.4939, 2.4289, 2.3805, 
		2.3714, 2.32, 2.3008, 2.2735, 2.2476, 2.2229, 2.1992, 2.1764, 2.1543, 2.1327, 2.1114, 2.0902, 
		2.0688, 2.0471, 2.0246, 2.0011, 1.9759, 1.9482, 1.9166, 1.8785, 1.788])


	@_dc.dataclass
	class SR125:
		"""Pentafluoroethane"""
		T = _np.array([172.52, 173.15, 183.15, 193.15, 203.15, 213.15, 219.15, 225.06, 229.15, 
		235.15, 241.15, 247.15, 253.15, 259.15, 265.15, 271.15, 277.15, 283.15, 289.15, 295.15, 
		301.15, 307.15, 313.15, 319.15, 325.15, 331.15, 337.15])
		
		P  = _np.array([2.91, 3.09, 7.29, 15.47, 30.08, 54.32, 75.11, 101.32, 123.32, 162.18, 
		209.94, 267.87, 337.33, 419.7, 516.46, 629.15, 759.35, 908.75, 1079.1, 1272.2, 1490.1, 
		1734.7, 2008.5, 2314, 2654.4, 3033.9, 3460.2])
		
		vf = _np.array([0.000591, 0.000592, 0.000604, 0.000616, 0.000629, 0.000643, 0.000652, 0.000661, 
		0.000667, 0.000677, 0.000688, 0.000699, 0.000711, 0.000724, 0.000738, 0.000752, 0.000769, 
		0.000786, 0.000806, 0.000829, 0.000854, 0.000883, 0.000919, 0.000963, 0.00102, 0.001106, 0.001286])
		
		vg = _np.array([0.2446, 0.2583, 0.5779, 1.1691, 2.1767, 3.7833, 5.1256, 6.7898, 8.1699, 10.5843, 
		13.5263, 17.0794, 21.3311, 26.3922, 32.3834, 39.4477, 47.7783, 57.5705, 69.1085, 82.7815, 
		99.0099, 118.624, 142.4501, 172.4138, 211.8644, 268.0965, 377.3585])
		
		hf = _np.array([87.13, 87.78, 98.18, 108.7, 119.36, 130.19, 136.78, 143.34, 147.92, 154.71, 
		161.59, 168.56, 175.62, 182.8, 190.08, 197.5, 205.05, 212.76, 220.65, 228.74, 237.07, 
		245.69, 254.67, 264.14, 274.33, 285.77, 300.86])
		
		hg = _np.array([277.39, 277.74, 283.36, 289.06, 294.83, 300.6, 304.06, 307.44, 309.77, 
		313.16, 316.51, 319.8, 323.03, 326.19, 329.25, 332.2, 335.02, 337.66, 340.1, 342.28, 
		344.16, 345.67, 346.69, 347.05, 346.38, 343.85, 335.77])
		
		sf = _np.array([0.4902, 0.494, 0.5524, 0.6082, 0.662, 0.714, 0.7444, 0.7739, 0.794, 0.8231, 
		0.8519, 0.8802, 0.9083, 0.9361, 0.9636, 0.9909, 1.0181, 1.0452, 1.0723, 1.0995, 1.1268, 
		1.1544, 1.1826, 1.2116, 1.2422, 1.2758, 1.3195])
		
		sg = _np.array([1.5931, 1.5911, 1.5634, 1.5421, 1.5257, 1.5135, 1.5077, 1.503, 1.5003, 
		1.4969, 1.4943, 1.4922, 1.4906, 1.4894, 1.4884, 1.4877, 1.487, 1.4863, 1.4854, 1.4842, 
		1.4824, 1.4799, 1.4764, 1.4714, 1.4638, 1.4512, 1.423])

	
	@_dc.dataclass
	class SR134A:
		"""1,1,1,2-Tetrafluoroethane"""
		T = _np.array([169.85, 173.15, 183.15, 193.15, 203.15, 213.15, 223.15, 233.15, 243.15, 
		247.15, 253.15, 259.15, 265.15, 271.15, 277.15, 283.15, 289.15, 295.15, 301.15, 307.15, 
		313.15, 319.15, 325.15, 331.15, 337.15, 343.15, 349.15, 358.15, 373.15]) 
		
		P = _np.array([0.39, 0.56, 1.52, 3.67, 7.98, 15.91, 29.45, 51.21, 84.38, 101.67, 132.73, 
		170.82, 216.93, 272.17, 337.66, 414.61, 504.25, 607.89, 726.88, 862.63, 1016.6, 1190.3, 
		1385.4, 1603.6, 1846.7, 2116.8, 2416.1, 2925.8, 3972.4])
		
		vf = _np.array([0.0006285, 0.000632, 0.0006428, 0.000654, 0.0006658, 0.0006783, 0.0006914, 
		0.0007054, 0.0007203, 0.0007265, 0.0007362, 0.0007464, 0.0007571, 0.0007684, 0.0007804, 0.000793, 
		0.0008066, 0.000821, 0.0008367, 0.0008535, 0.0008721, 0.0008924, 0.000915, 0.0009406, 0.0009697, 
		0.0010038, 0.0010446, 0.0011271, 0.0015356]) 
		
		vg = _np.array([0.02817, 0.03969, 0.10236, 0.23429, 0.48567, 0.92678, 1.64962, 2.76947, 
		4.42595, 5.27482, 6.78472, 8.61698, 10.82017, 13.44809, 16.55903, 20.22654, 24.52182, 
		29.5421, 35.3857, 42.1763, 50.07511, 59.27682, 70.02801, 82.71299, 97.65625, 115.60694, 
		137.55158, 181.81818, 373.13433])
		
		hf = _np.array([71.46, 75.36, 87.23, 99.16, 111.2, 123.36, 135.67, 148.14, 160.79, 165.9, 
		173.64, 181.44, 189.34, 197.32, 205.4, 213.58, 221.87, 230.29, 238.84, 247.54, 256.41, 265.47, 
		274.74, 284.27, 294.09, 304.28, 314.94, 332.22, 373.3])
		
		hg = _np.array([334.94, 336.85, 342.76, 348.83, 355.02, 361.31, 367.65, 374, 380.32, 382.82, 
		386.55, 390.24, 393.87, 397.43, 400.92, 404.32, 407.61, 410.79, 413.84, 416.72, 419.43, 421.92, 
		424.15, 426.07, 427.61, 428.65, 429.04, 427.76, 407.68])
		
		sf = _np.array([0.4126, 0.4354, 0.502, 0.5654, 0.6262, 0.6846, 0.741, 0.7956, 0.8486, 0.8694, 
		0.9002, 0.9306, 0.9606, 0.9902, 1.0195, 1.0485, 1.0772, 1.1057, 1.1341, 1.1623, 1.1905, 
		1.2186, 1.2469, 1.2753, 1.304, 1.3332, 1.3631, 1.4104, 1.5188])
		
		sg = _np.array([1.9639, 1.9456, 1.8972, 1.858, 1.8264, 1.801, 1.7806, 1.7643, 1.7515, 1.7471, 
		1.7413, 1.7363, 1.732, 1.7282, 1.725, 1.7221, 1.7196, 1.7173, 1.7152, 1.7131, 1.7111, 1.7089, 
		1.7064, 1.7035, 1.7, 1.6956, 1.6899, 1.6771, 1.6109])

	
	@_dc.dataclass
	class SR143A:
		"""1,1,1-Trifluoroethane"""
		T = _np.array([161.34, 163.15, 173.15, 183.15, 193.15, 203.15, 213.15, 223.15, 229.15, 235.15, 
		241.15, 247.15, 253.15, 259.15, 265.15, 271.15, 277.15, 283.15, 289.15, 295.15, 301.15, 307.15, 
		313.15, 319.15, 325.15, 331.15, 343.15])

		P = _np.array([1.07, 1.29, 3.33, 7.61, 15.72, 29.91, 53.07, 88.74, 117.86, 153.98, 198.16, 251.56, 
		315.35, 390.81, 479.23, 581.99, 700.51, 836.28, 990.85, 1165.9, 1363, 1584.2, 1831.4, 2106.8, 2413, 
		2753, 3552.7]) 
		
		vf = _np.array([0.000752, 0.000754, 0.000768, 0.000783, 0.000799, 0.000815, 0.000833, 0.000852, 
		0.000864, 0.000877, 0.00089, 0.000904, 0.000919, 0.000935, 0.000952, 0.00097, 0.00099, 0.001011, 
		0.001035, 0.001061, 0.00109, 0.001124, 0.001162, 0.001209, 0.001266, 0.001341, 0.001664])
		
		vg = _np.array([0.06754, 0.08045, 0.19559, 0.4238, 0.83535, 1.52265, 2.60105, 4.20982, 5.49722, 
		7.07564, 8.98957, 11.2905, 14.03509, 17.28907, 21.12825, 25.63445, 30.92146, 37.10575, 44.3459, 
		52.85412, 62.85355, 74.73842, 89.0472, 106.38298, 128.20513, 156.49452, 270.27027])
		
		hf = _np.array([52.52, 54.71, 66.87, 79.13, 91.55, 104.16, 116.99, 130.05, 138.01, 146.08, 154.25, 
		162.54, 170.95, 179.49, 188.18, 197.02, 206.03, 215.22, 224.63, 234.27, 244.18, 254.42, 265.04, 
		276.15, 287.9, 300.57, 333.19])
		
		hg = _np.array([319.59, 320.68, 326.81, 333.06, 339.4, 345.8, 352.21, 358.58, 362.37, 366.1, 
		369.78, 373.39, 376.91, 380.33, 383.63, 386.79, 389.79, 392.6, 395.18, 397.5, 399.49, 401.09, 
		402.19, 402.62, 402.15, 400.31, 385.42])
		
		sf = _np.array([0.3142, 0.3277, 0.4, 0.4688, 0.5348, 0.5984, 0.6599, 0.7197, 0.7548, 0.7894, 
		0.8236, 0.8573, 0.8907, 0.9238, 0.9566, 0.9892, 1.0216, 1.0539, 1.0863, 1.1186, 1.1512, 1.184, 
		1.2174, 1.2515, 1.2868, 1.324, 1.4172])
		
		sg = _np.array([1.9695, 1.9579, 1.9012, 1.8553, 1.818, 1.7879, 1.7635, 1.7438, 1.7339, 1.7251, 
		1.7173, 1.7104, 1.7043, 1.6987, 1.6937, 1.689, 1.6846, 1.6804, 1.6761, 1.6717, 1.6669, 1.6616, 
		1.6553, 1.6478, 1.6381, 1.6252, 1.5694])

	@_dc.dataclass
	class SR717:
		"""Ammonia"""
		T = _np.array([233.15, 239.15, 243.15, 249.15, 255.15, 261.15, 267.15, 273.15, 279.15, 285.15, 
		291.15, 297.15, 303.15, 309.15, 315.15, 321.15, 333.15, 348.15, 358.15, 363.15, 368.15, 373.15, 
		378.15, 383.15, 388.15, 393.15, 398.15, 403.15])
		
		P = _np.array([71.69, 97.95, 119.43, 158.64, 207.56, 267.82, 341.14, 429.38, 534.53, 658.66, 
		803.95, 972.68, 1167.2, 1390, 1643.5, 1930.5, 2615.6, 3710.5, 4610, 5116.7, 5664.3, 6255.3, 
		6892.3, 7578.3, 8317, 9112.5, 9970.02, 10897.7]) 
		
		vf = _np.array([0.001449, 0.001465, 0.001475, 0.001492, 0.001509, 0.001527, 0.001546, 0.001566, 
		0.001587, 0.001608, 0.001631, 0.001655, 0.00168, 0.001707, 0.001736, 0.001766, 0.001834, 0.001937, 
		0.002022, 0.002071, 0.002127, 0.00219, 0.002263, 0.00235, 0.002456, 0.002594, 0.002795, 0.003202])
		
		vg = _np.array([0.6438, 0.8618, 1.0374, 1.3533, 1.7413, 2.2128, 2.7801, 3.4566, 4.2573, 5.1983, 
		6.2976, 7.5752, 9.0531, 10.7573, 12.7178, 14.9656, 20.4918, 29.9222, 38.373, 43.4783, 49.334, 
		56.1167, 64.0615, 73.5294, 85.1789, 100.1001, 120.7729, 156.7398])
		
		hf = _np.array([19.17, 45.77, 63.6, 90.51, 117.6, 144.88, 172.34, 200, 227.87, 255.95, 284.28, 
		312.87, 341.76, 370.96, 400.54, 430.52, 491.97, 572.37, 629.04, 658.61, 689.19, 721, 754.35, 
		789.68, 827.74, 869.92, 919.68, 992.02])
		
		hg = _np.array([1407.76, 1417.23, 1423.31, 1432.08, 1440.39, 1448.21, 1455.51, 1462.24, 1468.37, 
		1473.88, 1478.7, 1482.82, 1486.17, 1488.7, 1490.36, 1491.06, 1489.27, 1479.72, 1467.53, 1459.19, 
		1449.01, 1436.63, 1421.57, 1403.08, 1379.99, 1350.23, 1309.12, 1239.32]) 
		
		sf = _np.array([0.2867, 0.3992, 0.473, 0.5821, 0.6893, 0.7946, 0.8981, 1, 1.1003, 1.1992, 1.2967, 
		1.3929, 1.4881, 1.5822, 1.6756, 1.7683, 1.9523, 2.1823, 2.3377, 2.4168, 2.4973, 2.5797, 2.6647, 
		2.7533, 2.8474, 2.9502, 3.0702, 3.2437])
		
		sg = _np.array([6.2425, 6.1339, 6.0651, 5.9667, 5.8736, 5.7853, 5.7013, 5.621, 5.5442, 5.4703, 
		5.3991, 5.3301, 5.2631, 5.1978, 5.1337, 5.0706, 4.9458, 4.7885, 4.6789, 4.6213, 4.5612, 4.4975, 
		4.4291, 4.3542, 4.2702, 4.1719, 4.0483, 3.8571])

	
	@_dc.dataclass
	class SR718:
		"""water"""
		T = _np.array([273.16, 278.15, 283.15, 288.15, 293.15, 298.15, 303.15, 308.15, 313.15, 318.15, 
		323.15, 328.15, 333.15, 338.15, 343.15, 348.15, 353.15, 358.15, 363.15, 368.15, 373.15, 378.15, 
		383.15, 388.15, 393.15, 398.15, 403.15, 408.15, 413.15, 418.15, 423.15, 428.15, 433.15, 438.15, 
		443.15, 448.15, 453.15, 458.15, 463.15, 468.15, 473.15, 478.15, 483.15, 488.15, 493.15, 498.15, 
		503.15, 508.15, 513.15, 518.15, 523.15, 528.15, 533.15, 538.15, 543.15, 548.15, 553.15, 558.15, 
		563.15, 568.15, 573.15, 578.15, 583.15, 588.15, 593.15, 603.15, 613.15, 623.15, 633.15, 643.15, 
		647.29])
		
		P = _np.array([0.6113, 0.8721, 1.2276, 1.7051, 2.339, 3.169, 4.246, 5.628, 7.384, 9.593, 12.349, 
		15.758, 19.94, 25.03, 31.19, 38.58, 47.39, 57.83, 70.14, 84.55, 101.35, 120.82, 143.27, 169.06, 
		198.53, 232.1, 270.1, 313, 361.3, 415.4, 475.8, 543.1, 617.8, 700.5, 791.7, 892, 1002.1, 1112.7, 
		1254.4, 1397.8, 1553.8, 1723, 1906.2, 2104, 2318, 2548, 2795, 3060, 3344, 3648, 3973, 4319, 4688, 
		5081, 5499, 5942, 6412, 6909, 7436, 7993, 8581, 9202, 9856, 10547, 11274, 12845, 14586, 16513, 
		18651, 21030, 22090])
		
		vf = _np.array([0.001, 0.001, 0.001, 0.001001, 0.001002, 0.001003, 0.001004, 0.001006, 0.001008, 
		0.00101, 0.001012, 0.001015, 0.001017, 0.00102, 0.001023, 0.001026, 0.001029, 0.001033, 0.001036, 
		0.00104, 0.001044, 0.001048, 0.001052, 0.001056, 0.00106, 0.001065, 0.00107, 0.001075, 0.00108, 
		0.001085, 0.001091, 0.001096, 0.001102, 0.001108, 0.001114, 0.001121, 0.001127, 0.001134, 0.001141, 
		0.001149, 0.001157, 0.001164, 0.001173, 0.001181, 0.00119, 0.001199, 0.001209, 0.001219, 0.001229, 
		0.00124, 0.001251, 0.001263, 0.001276, 0.001289, 0.001302, 0.001317, 0.001332, 0.001348, 0.001366, 
		0.001384, 0.001404, 0.001425, 0.001447, 0.001472, 0.001499, 0.001561, 0.001638, 0.00174, 0.001893, 
		0.002213, 0.003155])
		
		vg = _np.array([206.14, 147.12, 106.38, 77.93, 57.79, 43.36, 32.89, 25.22, 19.52, 15.26, 12.03, 
		9.568, 7.671, 6.197, 5.042, 4.131, 3.407, 2.828, 2.361, 1.982, 1.6729, 1.4194, 1.2102, 1.0366, 
		0.8919, 0.7706, 0.6685, 0.5822, 0.5089, 0.4463, 0.3928, 0.3468, 0.3071, 0.2727, 0.2428, 0.2168, 
		0.19405, 0.17409, 0.15654, 0.14105, 0.12736, 0.11521, 0.10441, 0.09479, 0.08619, 0.07849, 0.07158, 
		0.06357, 0.05976, 0.05471, 0.05013, 0.04598, 0.04221, 0.03877, 0.03564, 0.03279, 0.03017, 0.02777, 
		0.02557, 0.02354, 0.02167, 0.019948, 0.01835, 0.016867, 0.015488, 0.012996, 0.010797, 0.008813, 
		0.006945, 0.004925, 0.003155])
		
		hf = _np.array([0.01, 20.98, 42.01, 62.99, 83.96, 104.89, 125.79, 146.68, 167.57, 188.45, 209.33, 
		230.23, 251.13, 272.06, 292.98, 313.93, 334.91, 355.9, 376.92, 397.96, 419.04, 440.15, 461.3, 482.48, 
		503.71, 524.99, 546.31, 567.69, 589.13, 610.63, 632.2, 653.84, 675.55, 697.34, 719.21, 741.17, 
		763.12, 785.37, 807.62, 829.98, 852.45, 875.04, 897.76, 920.62, 943.62, 966.78, 990.12, 1013.62, 
		1037.32, 1061.23, 1085.36, 1109.73, 1134.37, 1159.28, 1184.51, 1210.07, 1235.99, 1262.31, 1289.07, 
		1316.3, 1344, 1372.4, 1401.3, 1431, 1461.5, 1525.3, 1594.2, 1670.6, 1760.5, 1890.5, 2099.3])
		
		hg = _np.array([2501.4, 2510.6, 2519.8, 2528.9, 2538.1, 2547.2, 2556.3, 2565.3, 2574.3, 2583.2, 
		2592.1, 2600.9, 2609.6, 2618.3, 2626.8, 2635.3, 2643.7, 2651.9, 2660.1, 2668.1, 2676.1, 2683.8, 
		2691.5, 2699, 2706.3, 2713.5, 2720.5, 2727.3, 2733.9, 2740.3, 2746.5, 2752.4, 2758.1, 2763.5, 
		2768.7, 2273.6, 2278.2, 2782.4, 2786.4, 2790, 2793.2, 2796, 2798.5, 2800.5, 2802.1, 2803.3, 2804, 
		2804.2, 2803.8, 2803, 2801.5, 2799.5, 2796.9, 2793.6, 2789.7, 2785, 2779.6, 2773.3, 2766.2, 2758.1, 
		2749, 2738.7, 2727.3, 2714.5, 2700.1, 2665.9, 2622, 2563.9, 2481, 2332.1, 2099.3])
		
		sf = _np.array([0, 0.0761, 0.151, 0.2245, 0.2966, 0.3674, 0.4369, 0.5053, 0.5725, 0.6387, 0.7038, 
		0.7679, 0.8312, 0.8935, 0.9549, 1.10155, 1.0753, 1.1343, 1.1925, 1.25, 1.3069, 1.363, 1.4185, 
		1.4734, 1.5276, 1.5813, 1.6344, 1.687, 1.7391, 1.7907, 1.8418, 1.8925, 1.9427, 1.9925, 2.0419, 
		2.0909, 2.1396, 2.1879, 2.2359, 2.2835, 2.3309, 2.378, 2.4248, 2.4714, 2.5178, 2.5639, 2.6099, 
		2.6558, 2.7015, 2.7472, 2.7927, 2.8383, 2.8838, 2.9294, 2.9751, 3.0208, 3.0668, 3.113, 3.1594, 
		3.2062, 3.2534, 3.301, 3.3493, 3.3982, 3.448, 3.5507, 3.6594, 3.7777, 3.9147, 4.1106, 4.4298])
		
		sg = _np.array([9.1562, 9.0257, 8.9008, 8.7814, 8.6672, 8.558, 8.4533, 8.3531, 8.257, 8.1648, 
		8.0763, 7.9913, 7.9096, 7.831, 7.7553, 7.6828, 7.6122, 7.5545, 7.4791, 7.4159, 7.3549, 7.2958, 
		7.2387, 7.1833, 7.1296, 7.0775, 7.0269, 6.9777, 6.9299, 6.8833, 6.8379, 6.7935, 6.7502, 6.7078, 
		6.6663, 6.6256, 6.5857, 6.5465, 6.5079, 6.4698, 6.4323, 6.3952, 6.3585, 6.3221, 6.2861, 6.2503, 
		6.2146, 6.1791, 6.1437, 6.1083, 6.073, 6.0375, 6.0019, 5.9662, 5.9301, 5.8938, 5.8571, 5.8199, 
		5.7821, 5.7437, 5.7045, 5.6643, 5.623, 5.5804, 5.5362, 5.4417, 5.3357, 5.2112, 5.0526, 
		4.7971, 4.4298])








