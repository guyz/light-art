import svg.path
from svg.path import parse_path
from xml.dom import minidom

def get_cubic_benzier(curve, step):
	coords = []
	p0 = curve.start
	p1 = curve.control1
	p2 = curve.control2
	p3 = curve.end
	t = 0
	while t <= 1:
		bx = ((1-t)**3)*p0.real+3*((1-t)**2)*t*p1.real+3*((1-t)**2)*p2.real+(t**3)*p3.real
		by = ((1-t)**3)*p0.imag+3*((1-t)**2)*t*p1.imag+3*((1-t)**2)*p2.imag+(t**3)*p3.imag
		coords.append((bx, by))
		t+=step
	return coords

def get_line(line, step):
	return [(line.start.real, line.start.imag),(line.end.real, line.end.imag)]

def main():
	step = 0.1

	# results = []
	# with open('tear.svg') as inputfile:
	#     for line in inputfile:
	#         results.append(line.strip())

	# path = results[2].split("=")[1][:-2]
	svg_image = minidom.parse('house.svg')
	path_strings = str([path.getAttribute('d') for path in svg_image.getElementsByTagName('path')][0])
	svg_image.unlink()

	parsed_path = parse_path(path_strings)

	print parsed_path
	for element in parsed_path:
		# if type(element) is svg.path.path.CubicBezier:
		# 	print get_cubic_benzier(element, step)
		if type(element) is svg.path.path.Line:
			print get_line(element, step)

if __name__ == "__main__":
    main()